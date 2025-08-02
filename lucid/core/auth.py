"""
# Lucid User Authentication

* Description:

    This is, at present, an overly simplistic authentication services that
    checks for user data within a department file.
"""


import enum
import json
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from lucid.core import const
from lucid.core import exceptions
from lucid.core import io_utils
from lucid.core import work


def _get_user_details_path(user: str = const.USERNAME) -> Path:
    """Gets the user details file for the given user.
    Defaults to current active user.
    """
    return Path(const.USER_DETAILS_DIR, f'{user}.json')


@enum.unique
class Permissions(enum.Enum):
    """What level of features are available to the user. The higher the
    permissions level, the more destructive workflows are available.

    Ideally only supervisors and systems level users can delete or permanently
    edit a file in-place. These functionality is mainly reserved to fixed
    mistakes.
    """
    VIEWER = 0
    """Has no real authority or permissions to do any form of work in
    the project or pipeline. This level is mainly for production, those who
    need visibility on the project but shouldn't be writing to it.
    """

    ARTIST = 1
    """Can do units of work."""

    LEAD = 2
    """Can review / kick-back units of work to artists."""

    SUPERVISOR = 3
    """Can invoke destructive work flows like deleting or editing files
    in place.
    """

    SYSTEM = 4
    """Pipeline and systems developers who need the most control to make sure
    the pipeline is working.
    """


@dataclass
class UserData(object):
    """The details for the current user tracked by the auth service."""
    user: str = const.USERNAME
    projects: list[str] = field(default_factory=lambda: [])
    roles: list[const.Role] = field(default_factory=lambda: [])
    permissions: Permissions = Permissions.VIEWER

    integrity_token: str = field(default=const.DEFAULT_META_TOKEN, repr=False)

    def to_dict(self) -> dict:
        """Convert values to json-legal dict. UserData.user does not get
        added because it is gotten from const and is also the key in
        the user details facility file for details lookup.
        """
        return {
            'user': self.user,
            'projects': self.projects,
            'roles': [r.value for r in self.roles],
            'permissions': self.permissions.value,
            '_meta': self.integrity_token
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'UserData':
        """Populates values from the given dict."""
        # if 'user' not in d or d['user'] != const.USERNAME:
        #     raise exceptions.MismatchedUserException(d['user'])

        if 'roles' not in d or const.UNASSIGNED in d['roles']:
            raise exceptions.RoleContainsUnassignedException()

        return cls(
            projects=d['projects'],
            roles=[const.Role(i) for i in d['roles']],
            permissions=Permissions(d['permissions']),
            integrity_token=d.get('_meta', const.DEFAULT_META_TOKEN)
        )


_SYSTEM_TOKEN = io_utils.import_data_from_json(
    Path(const.FACILITY_SYSTEMS_DIR, '_integrity.json')
)['SYSTEM_TOKEN']
_sys_user = '_sys'


class _AuthService(object):
    """Simple auth service to identify and authorize users."""

    _instance: '_AuthService' = None

    def __new__(cls) -> '_AuthService':
        """Singleton handling."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.user_data: UserData = UserData()
        self.load_data()

    # --------Load + Save Data-------------------------------------------------

    def load_data(self, user: str = const.USERNAME) -> None:
        """Loads user data from user details file then creates and stores a
        user data object containing all values.
        """
        self.user_data = UserData()
        self.user_data.user = user

        user_file = _get_user_details_path(user)
        if not user_file.exists():
            io_utils.export_data_to_json(user_file, self.user_data.to_dict())
        else:
            data = io_utils.import_data_from_json(user_file)
            self.user_data = UserData().from_dict(data)

    def save_data(self) -> None:
        """Serializes the tracked user data object and adds/overwrites it in
        the user details file.
        """
        data = self.user_data.to_dict()
        file = _get_user_details_path(self.user_data.user)
        io_utils.export_data_to_json(file, data, True)

    def reset_to_active_user(self) -> None:
        """This is mainly for code clarity."""
        self.load_data()

    # --------"adders"---------------------------------------------------------

    def set_user_permissions(self, user: str, perm: Permissions) -> None:
        """Sets the user to the given permission.
        Can only be done by active users of SYSTEMS level or higher.
        """
        if not self.systems_or_higher():
            raise exceptions.InvalidPermissionLevelException()

        self.load_data(user)
        self.user_data.permissions = perm
        self.save_data()

        self.reset_to_active_user()

    def add_user_to_project(self, user: str, project: str) -> None:
        """Adds the given user to the given project."""
        if not self.systems_or_higher():
            raise exceptions.InvalidPermissionLevelException()

        self.load_data(user)
        if not self.on_project(project):
            self.user_data.projects.append(project)
            self.save_data()

        self.reset_to_active_user()

    def remove_user_from_project(self, user: str, project: str) -> None:
        """Removes the given user from the given project."""
        if not self.systems_or_higher():
            raise exceptions.InvalidPermissionLevelException()

        self.load_data(user)
        if not self.on_project(project):
            self.reset_to_active_user()
            return

        self.user_data.projects.remove(project)
        self.save_data()
        self.reset_to_active_user()

    def add_role_to_user(self, user: str, role: const.Role) -> None:
        """Adds the given role to the given user."""
        self.load_data(user)
        if not self.has_role(role):
            self.user_data.roles.append(role)
            self.save_data()

        self.reset_to_active_user()

    def remove_role_from_user(self, user: str, role: const.Role) -> None:
        """Removes the given role from teh given user."""
        if not self.systems_or_higher():
            raise exceptions.InvalidPermissionLevelException()

        self.load_data(user)
        if not self.has_role(role):
            self.reset_to_active_user()
            return

        self.user_data.roles.remove(role)
        self.save_data()
        self.reset_to_active_user()

    # --------Checks-----------------------------------------------------------

    def on_project(self, project: str) -> bool:
        return project in self.user_data.projects

    def has_role(self, role: const.Role) -> bool:
        return role in self.user_data.roles

    def is_eg_level(self, level: Permissions) -> bool:
        """Is the user equal to or greater than the given permission level?"""
        return self.user_data.permissions.value >= level.value

    def lead_or_higher(self) -> bool:
        """Does the user have permission level lead or higher?"""
        return self.is_eg_level(Permissions.LEAD)

    def super_or_higher(self) -> bool:
        """Does the user have permission level supervisor or higher?"""
        return self.is_eg_level(Permissions.SUPERVISOR)

    def systems_or_higher(self) -> bool:
        """Does the user have system permission level?"""
        return (
                self.is_eg_level(Permissions.SYSTEM) and
                self.user_data.integrity_token == _SYSTEM_TOKEN
        )

    def valid_work_unit(self, wu: work.WorkUnit) -> bool:
        """Returns True if work unit is able to be processed by user.
        Only validates top level work unit, not nested work units.
        """
        if wu.project not in self.user_data.projects:
            return False
        if wu.role not in self.user_data.roles:
            return False

        return True


# --------Auth Service Singleton-----------------------------------------------

Auth = _AuthService()
"""The singleton authentication service."""


# --------Misc-----------------------------------------------------------------


def get_users() -> list[str]:
    """Returns a list of all currently authenticated users."""
    return io_utils.list_folder_contents(const.USER_DETAILS_DIR)


def setup_user_default() -> None:
    """Setup first default user."""
    if _sys_user in get_users():
        return

    Auth.load_data(_sys_user)
    Auth.user_data.integrity_token = _SYSTEM_TOKEN
    Auth.user_data.permissions = Permissions.SYSTEM
    Auth.save_data()
    Auth.reset_to_active_user()


def _indent_print(s: str = '', _in: int = 0) -> None:
    prefix = '    ' * _in
    print(f'{prefix}{s}')


def print_user_data(user: str = const.USERNAME) -> None:
    """Simple way to visualize user data."""
    user_details_file = Path(const.USER_DETAILS_DIR, f'{user}.json')
    data = io_utils.import_data_from_json(user_details_file)
    if data is None:
        io_utils.print_error_msg(f'No user data found for {user}!')
        return

    io_utils.print_center_header('User Data')
    print(json.dumps(data, indent=4))
    io_utils.print_center_header('-')


if __name__ == '__main__':
    print_user_data()

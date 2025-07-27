"""
# Lucid User Authentication

* Description:

    This is, at present, an overly simplistic authentication services that
    checks for user data within a department file.
"""


import enum
from dataclasses import dataclass
from dataclasses import field

from lucid.core import const
from lucid.core import exceptions
from lucid.core import io_utils


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
    the project or pipeline. This level is mainly for someone who stumbled into
    a project that they should not be in.
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

    def to_dict(self) -> dict:
        """Convert values to json-legal dict. UserData.user does not get
        added because it is gotten from const and is also the key in
        the user details facility file for details lookup.
        """
        return {
            'user': self.user,
            'projects': self.projects,
            'roles': [r.value for r in self.roles],
            'permissions': self.permissions.value
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'UserData':
        """Populates values from the given dict."""
        if 'user' not in d or d['user'] != const.USERNAME:
            raise exceptions.MismatchedUserException(d['user'])

        if 'roles' not in d or const.UNASSIGNED in d['roles']:
            raise exceptions.RoleContainsUnassignedException()

        user_data = UserData()
        user_data.projects = d['projects']
        user_data.roles = [const.Role(i) for i in d['roles']]
        user_data.permissions = Permissions(d['permissions'])
        return user_data


class AuthService(object):
    """Simple auth service to identify and authorize users."""

    def __init__(self):
        self.user_data: UserData = UserData()
        self.load_data()

    def load_data(self) -> None:
        """Loads user data from user details file then creates and stores a
        user data object containing all values.
        """
        if not const.USER_DETAILS_FILE.exists():
            self.user_data = UserData()
            io_utils.export_data_to_json(const.USER_DETAILS_FILE, self.user_data.to_dict())
        else:
            _data = io_utils.import_data_from_json(const.USER_DETAILS_FILE)
            self.user_data = UserData().from_dict(_data)

    def save_data(self) -> None:
        """Serializes the tracked user data object and adds/overwrites it in
        the user details file.
        """
        _data = self.user_data.to_dict()
        io_utils.export_data_to_json(const.USER_DETAILS_FILE, _data, True)

    def has_role(self, role: const.Role) -> bool:
        return role in self.user_data.roles

    def is_eg_level(self, level: Permissions) -> bool:
        """Is the user equal to or greater than the given permission level?"""
        return self.user_data.permissions.value >= level.value

    def is_lead_level(self) -> bool:
        return Permissions.LEAD == self.user_data.permissions

    def is_supervisor_level(self) -> bool:
        return Permissions.SUPERVISOR == self.user_data.permissions

    def is_system_level(self) -> bool:
        return Permissions.SYSTEM == self.user_data.permissions


auth = AuthService()

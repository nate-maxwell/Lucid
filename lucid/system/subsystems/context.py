"""
# Context Subsystem

* Description:

    A 'context' is an image of what kind of data the artist is currently
    producing, or how they are producing it. It is main a token + value
    map with some path builders.
"""


import os
from typing import Optional

from lucid import const
from lucid import exceptions
from lucid.system.messaging import router
from lucid.system.subsystems import context_messages
from lucid.system.subsystems import context_object


class Context(object):
    def __init__(self) -> None:
        self._custom_variables: dict[str, str] = {}

    @staticmethod
    def reset_context() -> None:
        # -----General-----
        os.environ[const.ENV_ROLE] = const.UNASSIGNED
        os.environ[const.ENV_FILETYPE] = const.UNASSIGNED
        os.environ[const.ENV_FILENAME] = const.UNASSIGNED

        # -----Asset-----
        os.environ[const.ENV_CATEGORY] = const.UNASSIGNED
        os.environ[const.ENV_SUBCATEGORY] = const.UNASSIGNED

        # -----Anim-----
        os.environ[const.ENV_DIRECTIONAL_ANIM] = '0'
        os.environ[const.ENV_ROOT_MOTION] = '0'

        # -----Texture-----
        os.environ[const.ENV_POWER_OF_TWO] = '0'
        os.environ[const.ENV_COLORSPACE] = const.UNASSIGNED
        os.environ[const.ENV_CHANNEL_PACKED] = '0'

        router.route_message(context_messages.RoleChanged(const.UNASSIGNED))
        router.route_message(context_messages.ContextChanged())

    # ----------Context Tokens---------------------------------------------------------------------

    @property
    def project(self) -> str:
        val = os.getenv(const.ENV_PROJECT, const.UNASSIGNED)
        if val == const.UNASSIGNED:
            raise exceptions.ContextError('No project loaded!')
        return val.replace(';', '')

    @property
    def dcc(self) -> str:
        val = os.getenv(const.ENV_DCC, const.UNASSIGNED)
        if val == const.UNASSIGNED:
            raise exceptions.ContextError('DCC environ var not set on launch!')
        return val.replace(';', '')

    @dcc.setter
    def dcc(self, new_dcc: str) -> None:
        os.environ[const.ENV_DCC] = new_dcc.replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def role(self) -> str:
        val = os.getenv(const.ENV_ROLE, const.UNASSIGNED)
        return val.replace(';', '')

    @role.setter
    def role(self, new_role: str) -> None:
        self.reset_context()
        router.route_message(context_messages.RoleChanged(new_role))
        os.environ[const.ENV_ROLE] = new_role.replace(';', '')

    @property
    def filetype(self) -> str:
        val = os.getenv(const.ENV_FILETYPE, const.UNASSIGNED)
        return val.replace(';', '')

    @filetype.setter
    def filetype(self, new_filetype: str) -> None:
        os.environ[const.ENV_FILETYPE] = new_filetype.replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def filename(self) -> str:
        val = os.getenv(const.ENV_FILENAME, const.UNASSIGNED)
        return val.replace(';', '')

    @filename.setter
    def filename(self, new_filename: str) -> None:
        os.environ[const.ENV_FILENAME] = new_filename.replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def category(self) -> str:
        val = os.getenv(const.ENV_CATEGORY, const.UNASSIGNED)
        return val.replace(';', '')

    @category.setter
    def category(self, new_category: str) -> None:
        os.environ[const.ENV_CATEGORY] = new_category.replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def subcategory(self) -> str:
        val = os.getenv(const.ENV_SUBCATEGORY, const.UNASSIGNED)
        return val.replace(';', '')

    @subcategory.setter
    def subcategory(self, new_subcategory: str) -> None:
        os.environ[const.ENV_SUBCATEGORY] = new_subcategory.replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def directional(self) -> bool:
        val = os.getenv(const.ENV_DIRECTIONAL_ANIM, const.UNASSIGNED)
        return bool(int(val.replace(';', '')))

    @directional.setter
    def directional(self, is_directional: bool) -> None:
        os.environ[const.ENV_SUBCATEGORY] = str(int(is_directional)).replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def root_motion(self) -> bool:
        val = os.getenv(const.ENV_ROOT_MOTION, const.UNASSIGNED)
        return bool(int(val.replace(';', '')))

    @root_motion.setter
    def root_motion(self, is_root_motion: bool) -> None:
        os.environ[const.ENV_ROOT_MOTION] = str(int(is_root_motion)).replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def power_of_two(self) -> bool:
        val = os.getenv(const.ENV_POWER_OF_TWO, const.UNASSIGNED)
        return bool(int(val.replace(';', '')))

    @power_of_two.setter
    def power_of_two(self, is_power_of_two: bool) -> None:
        os.environ[const.ENV_POWER_OF_TWO] = str(int(is_power_of_two)).replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def colorspace(self) -> str:
        val = os.getenv(const.ENV_COLORSPACE, const.UNASSIGNED)
        return val.replace(';', '')

    @colorspace.setter
    def colorspace(self, new_colorspace: str) -> None:
        os.environ[const.ENV_COLORSPACE] = new_colorspace.replace(';', '')
        router.route_message(context_messages.ContextChanged())

    @property
    def channel_packed(self) -> bool:
        val = os.getenv(const.ENV_CHANNEL_PACKED, const.UNASSIGNED)
        return bool(int(val.replace(';', '')))

    @channel_packed.setter
    def channel_packed(self, is_channel_packed: bool) -> None:
        os.environ[const.ENV_CHANNEL_PACKED] = str(int(is_channel_packed)).replace(';', '')
        router.route_message(context_messages.ContextChanged())

    # ----------Custom Tokens----------------------------------------------------------------------

    # Occasionally we have a tool that needs to track the value on the environment level that isn't listed
    # in the normal context. For example, we may need to track a value when importing legacy pipeline data
    # that we don't want to officially track, but need to temporarily store it while the user moves from
    # tool to tool.

    # You can add those values here -> they will get !removed! on opening a new file.

    def remove_custom_vars(self) -> None:
        """Removes all currently tracked custom variables from the current environment.
        Gets called when opening a new file.
        """
        for k, _ in self._custom_variables.items():
            if k in os.environ:
                del os.environ[k]
        self._custom_variables = {}

    def set_custom_var(self, var: str, val: str) -> None:
        """Set a custom variable and value. Var name will get upper-cased."""
        self._custom_variables[var.upper()] = val
        os.environ[var.upper()] = val

    @staticmethod
    def get_custom_var(var: str) -> Optional[str]:
        """Get a custom variable's value, if it can be found, otherwise returns None.
        Var name will get upper-cased.
        """
        if var.upper() in os.environ:
            return os.environ[var.upper()].replace(';', '')
        return None

    @property
    def custom_vars(self) -> dict[str, str]:
        """A dict of all custom variable names + values."""
        return self._custom_variables

    # ----------Helpers----------------------------------------------------------------------------

    @property
    def blank_context(self) -> context_object.LucidContext:
        """A LucidContext object with unassigned values."""
        return context_object.LucidContext()

    @property
    def current_context(self) -> context_object.LucidContext:
        """A snapshot of the current context packaged in a LucidContext object.
        Only the tokens, no path building.
        """
        ctx = self.blank_context
        ctx.project = self.project
        ctx.dcc = self.dcc
        ctx.role = self.role
        ctx.filetype = self.filetype
        ctx.filename = self.filename
        ctx.category = self.category
        ctx.subcategory = self.subcategory
        ctx.directional = self.directional
        ctx.root_motion = self.root_motion
        ctx.power_of_two = self.power_of_two
        ctx.colorspace = self.colorspace
        ctx.channel_packed = self.channel_packed

        return ctx

    @staticmethod
    def verify_tokens(*args) -> bool:
        """Loops through the given tokens and returns True if none of them are unassigned."""
        for t in args:
            if t == const.UNASSIGNED:
                return False
        return True


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


project: str
dcc: str
role: str
filetype: str
filename: str
category: str
subcategory: str
directional: bool
root_motion: bool
power_of_two: bool
colorspace: str
channel_packed: bool

blank_context: context_object.LucidContext
"""A LucidContext object with unassigned values."""


current_context: context_object.LucidContext
"""A snapshot of the current context packaged in a LucidContext object.
Only the tokens, no path building.
"""


def remove_custom_vars() -> None:
    """Removes all currently tracked custom variables from the current environment.
    Gets called when opening a new file.
    """


def set_custom_var(var: str, val: str) -> None:
    """Set a custom variable and value. Var name will get upper-cased."""


def get_custom_var(var: str) -> Optional[str]:
    """Get a custom variable's value, if it can be found, otherwise returns None.
    Var name will get upper-cased.
    """


def custom_vars() -> dict[str, str]:
    """A dict of all custom variable names + values."""


def verify_tokens(*args) -> bool:
    """Loops through the given tokens and returns True if none of them are unassigned."""


def reset_context() -> None:
    """Resets all dynamic vars to unassigned."""

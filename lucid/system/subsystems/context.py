"""
# Context Subsystem

* Description:

    A 'context' is an image of what kind of data the artist is currently
    producing, or how they are producing it. It is main a token + value
    map with some path builders.
"""


import os
import enum
import types
import typing
import sys
from typing import Optional
from typing import Type

from lucid import const
from lucid import exceptions
from lucid import io_utils
from lucid.system.messaging import router
from lucid.system.subsystems import context_messages
from lucid.system.subsystems import context_object


@enum.unique
class AssetType(enum.Enum):
    UNASSIGNED = const.UNASSIGNED
    SM = 'SM'
    SK = 'SK'
    MAT = 'M'
    TEX = 'T'
    ANIM = 'ANIM'


@enum.unique
class TextureType(enum.Enum):
    UNASSIGNED = const.UNASSIGNED
    BC = 'BC'
    """Basecolor"""
    ORM = 'ORM'
    """Occlusion(r), roughness(g), metallic(b) channel packed."""
    N = 'N'
    """Normal"""
    A = 'A'
    """Alpha"""


class _ModuleType(types.ModuleType):
    """Context Service Singleton"""

    # -----Closures-----
    AssetType = AssetType
    TextureType = TextureType

    def __init__(self) -> None:
        super().__init__(sys.modules[__name__].__name__)
        io_utils.print_lucid_msg('Enabling Subsystem: Context')
        self._custom_variables: dict[str, str] = {}
        self._ctx_types = {
            const.ROLE_MODEL: context_object.ModelContext,
            const.ROLE_RIG: context_object.RigContext,
            const.ROLE_TEXTURE: context_object.TextureContext,
            const.ROLE_ANIM: context_object.AnimContext,
            const.ROLE_COMP: context_object.CompContext
        }
        self.subcontext: Optional[context_object.ContextType] = None

    @staticmethod
    def reset_context() -> None:
        # -----General-----
        os.environ[const.ENV_ROLE] = const.UNASSIGNED
        os.environ[const.ENV_FILE_SUFFIX] = const.UNASSIGNED
        os.environ[const.ENV_FILE_BASE_NAME] = const.UNASSIGNED

        # -----Asset-----
        os.environ[const.ENV_CATEGORY] = const.UNASSIGNED
        os.environ[const.ENV_SUBCATEGORY] = const.UNASSIGNED

        # -----Anim-----
        os.environ[const.ENV_DIRECTIONAL_ANIM] = '0'
        os.environ[const.ENV_ROOT_MOTION] = '0'

        # -----Texture-----
        os.environ[const.ENV_TEXTURE_TYPE] = const.UNASSIGNED
        os.environ[const.ENV_POWER_OF_TWO] = '0'
        os.environ[const.ENV_COLORSPACE] = const.UNASSIGNED

        router.route_message(context_messages.RoleChanged(const.UNASSIGNED))
        router.route_message(context_messages.ContextChanged())

    @staticmethod
    def verify_subcontext(
            ctx_type: Type[context_object.T_CTX_TYPE],
            sub_ctx: context_object.ContextType
    ) -> context_object.T_CTX_TYPE:
        """Verifies if the given sub_ctx is of the type ctx_type, cast to the
        given type for type checking.
        """
        if not isinstance(sub_ctx, ctx_type):
            raise exceptions.SubContextError(f'Got {type(sub_ctx)}, expected {ctx_type}.')
        subcon = typing.cast(ctx_type, sub_ctx)
        return subcon

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
        os.environ[const.ENV_ROLE] = new_role.replace(';', '')
        self.subcontext = self._ctx_types[new_role]()

    @property
    def file_suffix(self) -> str:
        val = os.getenv(const.ENV_FILE_SUFFIX, const.UNASSIGNED)
        return val.replace(';', '')

    @file_suffix.setter
    def file_suffix(self, new_suffix: str) -> None:
        suffix = new_suffix
        if not suffix.startswith('.'):
            suffix = f'.{suffix}'
        os.environ[const.ENV_FILE_SUFFIX] = suffix.replace(';', '')
        self.subcontext.ext = suffix.lstrip('.')
        router.route_message(context_messages.ContextChanged())

    @property
    def file_base_name(self) -> str:
        """The base name for the asset.
        e.g. T_BrickWall_01_BC.png would have a base name of 'BrickWall'.
        """
        val = os.getenv(const.ENV_FILE_BASE_NAME, const.UNASSIGNED)
        return val.replace(';', '')

    @file_base_name.setter
    def file_base_name(self, new_base_name: str) -> None:
        """The base name for the asset.
        e.g. T_BrickWall_01_BC.png would have a base name of 'BrickWall'.
        """
        os.environ[const.ENV_FILE_BASE_NAME] = new_base_name.replace(';', '')
        subcon = self.verify_subcontext(context_object.AssetContext, self.subcontext)
        subcon.name = new_base_name
        router.route_message(context_messages.ContextChanged())

    @property
    def texture_type(self) -> str:
        """The type of texture: BC, N, ORM, etc."""
        val = os.getenv(const.ENV_TEXTURE_TYPE, const.UNASSIGNED)
        return val.replace(';', '')

    @texture_type.setter
    def texture_type(self, new_type: str) -> None:
        """The type of texture: BC, N, ORM, etc."""
        os.environ[const.ENV_TEXTURE_TYPE] = new_type.replace(';', '')
        subcon = self.verify_subcontext(context_object.TextureContext, self.subcontext)
        subcon.texture_type = new_type
        router.route_message(context_messages.ContextChanged())

    @property
    def category(self) -> str:
        val = os.getenv(const.ENV_CATEGORY, const.UNASSIGNED)
        return val.replace(';', '')

    @category.setter
    def category(self, new_category: str) -> None:
        os.environ[const.ENV_CATEGORY] = new_category.replace(';', '')
        subcon = self.verify_subcontext(context_object.AssetContext, self.subcontext)
        subcon.category = new_category
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
        subcon = self.verify_subcontext(context_object.AnimContext, self.subcontext)
        subcon.directional = is_directional
        router.route_message(context_messages.ContextChanged())

    @property
    def root_motion(self) -> bool:
        val = os.getenv(const.ENV_ROOT_MOTION, const.UNASSIGNED)
        return bool(int(val.replace(';', '')))

    @root_motion.setter
    def root_motion(self, is_root_motion: bool) -> None:
        os.environ[const.ENV_ROOT_MOTION] = str(int(is_root_motion)).replace(';', '')
        subcon = self.verify_subcontext(context_object.AnimContext, self.subcontext)
        subcon.root_motion = is_root_motion
        router.route_message(context_messages.ContextChanged())

    @property
    def power_of_two(self) -> bool:
        val = os.getenv(const.ENV_POWER_OF_TWO, const.UNASSIGNED)
        return bool(int(val.replace(';', '')))

    @power_of_two.setter
    def power_of_two(self, is_power_of_two: bool) -> None:
        os.environ[const.ENV_POWER_OF_TWO] = str(int(is_power_of_two)).replace(';', '')
        subcon = self.verify_subcontext(context_object.TextureContext, self.subcontext)
        subcon.power_of_two = is_power_of_two
        router.route_message(context_messages.ContextChanged())

    @property
    def colorspace(self) -> str:
        val = os.getenv(const.ENV_COLORSPACE, const.UNASSIGNED)
        return val.replace(';', '')

    @colorspace.setter
    def colorspace(self, new_colorspace: str) -> None:
        os.environ[const.ENV_COLORSPACE] = new_colorspace.replace(';', '')
        subcon = self.verify_subcontext(context_object.TextureContext, self.subcontext)
        subcon.colorspace = new_colorspace
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
        ctx = context_object.LucidContext()
        ctx.subcontext = self._ctx_types[self.role]
        return ctx

    @property
    def current_context(self) -> context_object.LucidContext:
        """A snapshot of the current context packaged in a LucidContext object.
        Only the tokens, no path building.
        """
        ctx = self.blank_context
        ctx.project = self.project
        ctx.dcc = self.dcc
        ctx.role = self.role
        ctx.subcontext = self.subcontext

        return ctx

    @staticmethod
    def verify_tokens(*args) -> bool:
        """Loops through the given tokens and returns True if none of them are unassigned."""
        for t in args:
            if t == const.UNASSIGNED:
                return False
        return True


# Binds all class properties to the module namespace in singleton fashion.
sys.modules[__name__] = _ModuleType()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

project: str
dcc: str
role: str
subcontext: context_object.T_CTX_TYPE
file_suffix: str
file_base_name: str
category: str
subcategory: str
directional: bool
root_motion: bool
power_of_two: bool
colorspace: str
texture_type: str

blank_context: context_object.LucidContext
"""A LucidContext object with unassigned values."""

current_context: context_object.LucidContext
"""A snapshot of the current context packaged in a LucidContext object.
Only the tokens, no path building.
"""


def reset_context() -> None:
    """Resets all dynamic vars to unassigned."""


def verify_subcontext(
        ctx_type: Type[context_object.T_CTX_TYPE],
        sub_ctx: context_object.ContextType
) -> context_object.T_CTX_TYPE:
    """Verifies if the given sub_ctx is of the type ctx_type, cast to the
    given type for type checking.
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

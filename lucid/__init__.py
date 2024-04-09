"""
Lucid Unreal Games Pipeline.
"""


import sys
import types
from typing import Callable
from typing import Union

import lucid.config_paths
import lucid.io_utils


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Exceptions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


"""
Exceptions have an integer value for easy front loading of information.
Exception topics are given an integer range of 100 for easy categorization.

0-99    - Debug related exceptions
100-199 - Show related exceptions
200-299 - File IO related exceptions
300-399 - Headless operation related exceptions
400-499 - Unreal related exceptions
"""


class LucidException(Exception):
    """Base Lucid exception. All other exception should be derived from this class."""
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__()
        elif len(args) == 1:
            super().__init__('[Lucid] ' + str(args[0]))
        else:
            super().__init__('[Lucid]', *args)


class LucidDebugError(LucidException):
    """Exception for debug functions that do not specify a valid debug level."""
    def __init__(self, func: Callable, level: int):
        args = f'Debug decorator level {level} is not between 1 and 5 for {func.__name__}.'
        super().__init__(0, args)


class InvalidProjectError(LucidException):
    """Exception for invalid projects or no project selection."""
    def __init__(self, message: str = 'No or invalid project selected.'):
        super().__init__(100, message)


class SaveFileError(LucidException):
    def __init__(self):
        super().__init__(200, 'Save Unsuccessful')


class MissingTokenError(LucidException):
    def __init__(self, token: str = 'Unspecified Token'):
        msg = f'Filename or string missing [{token}] token.'
        super().__init__(210, msg)


class InvalidHeadlessCaseError(LucidException):
    def __init__(self, case: str):
        super().__init__(300, f'Invalid case selected :: {case}')


class UECategoryImportError(LucidException):
    def __init__(self, *args):
        super().__init__(400, args)


class UEStaticMeshImportError(LucidException):
    def __init__(self):
        msg = 'Something went wrong with the import, is it not a static mesh?'
        super().__init__(405, msg)


class UESkeletalMeshImportError(LucidException):
    def __init__(self, *args):
        msg = 'Something went wrong with the import, is it not a skeletal mesh?'
        super().__init__(410, msg)


class UEMaterialConversionError(LucidException):
    def __init__(self):
        msg = 'Could not locate "standard" material in project configs.'
        super().__init__(420, msg)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Dynamic module vars
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class _ModuleType(types.ModuleType):
    """
    A module class for refreshable variables.
    For example, the list of shows could change after the module is imported.
    Therefore, it has been made a property bound to the module, so it refreshes
    when called.
    """
    @property
    def projects(self) -> Union[list[str], None]:
        return lucid.io_utils.list_folder_contents(lucid.config_paths.PROJECTS_PATH)


sys.modules[__name__].__class__ = _ModuleType

# Required for static type checkers to accept the following names as a member of the module
projects: Union[list[str], None]
"""The current list of show names in the shows directory."""

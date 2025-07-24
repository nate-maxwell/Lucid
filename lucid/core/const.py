"""
# Global constants and paths.

* Description:

    All non-dynamic, or fixed, values and paths for the core pipeline.
"""


import enum
import getpass
import sys
from pathlib import Path

import lucid


# ----------Repo---------------------------------------------------------------

PYTHON_EXEC = Path(sys.executable)
VENV_SITE_PACKAGES_PATH = Path(PYTHON_EXEC.parent.parent, 'Lib/site-packages')

try:
    LUCID_PATH = Path(lucid.__file__).parent.parent
except TypeError:
    # Local editable installations return None for module.__file__
    # noinspection PyUnresolvedReferences
    LUCID_PATH = Path(lucid.__spec__.submodule_search_locations._path[0])

NETWORK_DRIVE_ROOT = Path('T:/')

VERSION_PADDING = 3

UNASSIGNED = 'UNASSIGNED'
"""A None-like value for when None is not a good idea to use, or semantically
it would be better to specify unassigned values rather than uninitialized
values.
"""


# ----------User---------------------------------------------------------------

USERNAME = getpass.getuser()
USER_SETTINGS_DIR = Path(LUCID_PATH, 'lucid/user')


# ----------Environment--------------------------------------------------------

ENV_PROJECT = 'ENV_PROJECT'


# ----------Project------------------------------------------------------------

PROJECTS_PATH = Path(NETWORK_DRIVE_ROOT, 'projects')
"""The 'root' projects path to where all projects are stored."""


# ----------Applications-------------------------------------------------------

@enum.unique
class DCCs(enum.Enum):
    MAYA = 'MAYA'
    PAINTER = 'PAINTER'
    DESIGNER = 'DESIGNER'
    UNREAL = 'UNREAL'

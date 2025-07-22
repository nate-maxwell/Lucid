"""
# Global constants and paths.

* Description:

    All non-dynamic, or fixed, values and paths for the core.
"""


import enum
import getpass
import sys
from pathlib import Path

import lucid


# ----------Pipe---------------------------------------------------------------

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


# ----------Environment--------------------------------------------------------

ENV_PROJECT = 'ENV_PROJECT'


# ----------Project------------------------------------------------------------

PROJECTS_PATH = Path(NETWORK_DRIVE_ROOT, 'projects')
"""The 'root' projects path to where all projects are stored."""


# ----------Messages-----------------------------------------------------------

# -----Subsystem Domains-----

@enum.unique
class SystemChannels(enum.Enum):
    SUBSYSTEM = 'SUBSYSTEM'
    INVALID = 'INVALID_CHAN'


# -----Work Domains-----

@enum.unique
class DomainChannels(enum.Enum):
    MODEL = 'MODEL_CHAN'
    ANIM = 'ANIM_CHAN'
    RIG = 'RIG_CHAN'
    RENDER = 'RENDER_CHAN'
    TEXTURE = 'TEXTURE_CHAN'
    SCENE = 'SCENE_CHAN'
    COMP = 'COMP_CHAN'
    CAMERA = 'CAMERA_CHAN'
    MEDIA = 'MEDIA_CHAN'
    QA = 'QA_CHAN'

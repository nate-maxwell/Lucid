"""
# Global constants and paths.

* Description:

    All non-dynamic, or fixed, values and paths for the pipeline.
"""


import getpass
import sys
from pathlib import Path

import lucid


# ----------Pipe-----------------------------------------------------------------------------------

PYTHON_EXEC = Path(sys.executable)
VENV_SITE_PACKAGES_PATH = Path(PYTHON_EXEC.parent.parent, 'Lib/site-packages')

try:
    LUCID_PATH = Path(lucid.__file__).parent.parent
except TypeError:
    # Local editable installations return None for module.__file__
    # noinspection PyUnresolvedReferences
    LUCID_PATH = Path(lucid.__spec__.submodule_search_locations._path[0])

VERSION_PADDING = 3

NETWORK_DRIVE_ROOT = Path('T:/')
PROJ_PATH = Path(NETWORK_DRIVE_ROOT, 'projects')


# ----------User-----------------------------------------------------------------------------------

USERNAME = getpass.getuser()


# ----------Context--------------------------------------------------------------------------------

ROLE_MODEL = 'ROLE_MODEL'
ROLE_RIG = 'ROLE_RIG'
ROLE_TEXTURE = 'ROLE_TEXTURE'
ROLE_ANIM = 'ROLE_ANIM'
ROLE_COMP = 'ROLE_COMP'


# ----------Environ--------------------------------------------------------------------------------

UNASSIGNED = 'unassigned'

ENV_PROJECT = 'LUCID_PROJECT'

ENV_DCC = 'LUCID_DCC'
ENV_ROLE = 'LUCID_ROLE'

ENV_FILE_SUFFIX = 'LUCID_FILE_SUFFIX'
ENV_FILE_BASE_NAME = 'LUCID_FILE_BASE_NAME'
ENV_ASSET_TYPE = 'LUCID_ASSET_TYPE'
ENV_TEXTURE_TYPE = 'LUCID_TEXTURE_TYPE'
ENV_CATEGORY = 'LUCID_CATEGORY'
ENV_SUBCATEGORY = 'LUCID_SUBCATEGORY'
ENV_DIRECTIONAL_ANIM = 'LUCID_DIRECTIONAL_ANIM'
ENV_ROOT_MOTION = 'LUCID_ROOT_MOTION'
ENV_POWER_OF_TWO = 'LUCID_POWER_OF_TWO'
ENV_COLORSPACE = 'LUCID_COLORSPACE'


# ----------Messages-------------------------------------------------------------------------------

# -----Subsystem Domains-----

SUBSYSTEM_CHAN = 'SUBSYSTEM'
INVALID_CHAN = 'INVALID_CHAN'

# -----Work Domains-----

MODEL_CHAN = 'MODEL_CHAN'
ANIM_CHAN = 'ANIM_CHAN'
RIG_CHAN = 'RIG_CHAN'
RENDER_CHAN = 'RENDER_CHAN'
TEXTURE_CHAN = 'TEXTURE_CHAN'
SCENE_CHAN = 'SCENE_CHAN'
COMP_CHAN = 'COMP_CHAN'
CAMERA_CHAN = 'CAMERA_CHAN'
MEDIA_CHAN = 'MEDIA_CHAN'
QA_CHAN = 'QA_CHAN'


# ----------Naming Conventions---------------------------------------------------------------------

# -----AssetTypes-----

PREFIX_TEXTURE = 'T'
PREFIX_SM = 'SM'
PREFIX_SK = 'SK'
PREFIX_ANIM = 'ANIM'
PREFIX_SCENE = 'SCN'

# -----Texture Types-----

SUFFIX_BASECOLOR = 'BC'
SUFFIX_CHANNEL_PACKED = 'ORM'
SUFFIX_NORMAL = 'N'

# -----Directional Anim Types-----

ANIM_DIR_FORWARD = 'FWD'
ANIM_DIR_FORWARD_LEFT = 'FWDL'
ANIM_DIR_FORWARD_RIGHT = 'FWDR'

ANIM_DIR_BACKWARD = 'BWD'
ANIM_DIR_BACKWARD_LEFT = 'BWDL'
ANIM_DIR_BACKWARD_RIGHT = 'BWDR'

ANIM_DIR_LEFT = 'LFT'
ANIM_DIR_RIGHT = 'RGT'

"""
# Global constants and paths.

* Description:

    All non-dynamic, or fixed, values and paths for the pipeline.
"""


import enum
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

NETWORK_DRIVE_ROOT = Path('T:/')
PROJ_PATH = Path(NETWORK_DRIVE_ROOT, 'projects')

VERSION_PADDING = 3

UNASSIGNED = 'unassigned'


# ----------User-----------------------------------------------------------------------------------

USERNAME = getpass.getuser()


# ----------Context--------------------------------------------------------------------------------

@enum.unique
class Role(enum.Enum):
    MODEL = 'ROLE_MODEL'
    RIG = 'ROLE_RIG'
    TEXTURE = 'ROLE_TEXTURE'
    ANIM = 'ROLE_ANIM'
    COMP = 'ROLE_COMP'


# ----------Environ--------------------------------------------------------------------------------

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


# ----------Asset Attributes-----------------------------------------------------------------------

# -----AssetTypes-----

@enum.unique
class AssetType(enum.Enum):
    TEXTURE = 'T'
    SM = 'SM'
    SK = 'SK'
    ANIM = 'ANIM'
    SCENE = 'SCN'


@enum.unique
class AssetCategory(enum.Enum):
    VEH = 'VEH'
    CHAR = 'CHAR'
    PROP = 'PROP'
    CREATURE = 'CREA'
    ENV = 'ENV'
    PLANT = 'PLANT'


@enum.unique
class AssetSubcategory(enum.Enum):
    RIG = 'RIG'
    MODEL = 'MODEL'
    UV = 'UV'
    SCULPT = 'SCULPT'


# -----Texture Types-----

@enum.unique
class TextureType(enum.Enum):
    BASECOLOR = 'BC'
    NORMAL = 'N'
    ALPHA = 'A'
    CHANNEL_PACKED = 'ORM'
    """Occlusion(r), roughness(g), metallic(b) channel packed."""


# -----Directional Anim Types-----

@enum.unique
class AnimDirection(enum.Enum):
    FORWARD = 'FWD'
    FORWARD_LEFT = 'FWDL'
    FORWARD_RIGHT = 'FWDR'

    BACKWARD = 'BWD'
    BACKWARD_LEFT = 'BWDL'
    BACKWARD_RIGHT = 'BWDR'

    LEFT = 'LFT'
    RIGHT = 'RGT'

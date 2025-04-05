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
    LUCID_PATH = Path(lucid.__spec__.submodule_search_locations._path[0])

VERSION_PADDING = 3

# ----------User-----------------------------------------------------------------------------------

USERNAME = getpass.getuser()

# ----------Environ--------------------------------------------------------------------------------

UNASSIGNED = 'unassigned'

ENV_PROJECT = 'LUCID_PROJECT'

ENV_DCC = 'LUCID_DCC'
ENV_ROLE = 'LUCID_ROLE'

ENV_FILETYPE = 'LUCID_FILETYPE'
ENV_FILENAME = 'LUCID_FILENAME'
ENV_CATEGORY = 'LUCID_CATEGORY'
ENV_SUBCATEGORY = 'LUCID_SUBCATEGORY'
ENV_DIRECTIONAL_ANIM = 'LUCID_DIRECTIONAL_ANIM'
ENV_ROOT_MOTION = 'LUCID_ROOT_MOTION'
ENV_POWER_OF_TWO = 'LUCID_POWER_OF_TWO'
ENV_COLORSPACE = 'LUCID_COLORSPACE'
ENV_CHANNEL_PACKED = 'LUCID_CHANNEL_PACKED'


# ----------Messages-------------------------------------------------------------------------------

# -----Subsystem Domains-----
SUBSYSTEM_CHAN = 'SUBSYSTEM'

# -----Work Domains-----
ASSET_CHAN = 'ASSET'
ANIM_CHAN = 'ANIM'
RENDER_CHAN = 'RENDER'
TEXTURE_CHAN = 'TEXTURE'
INVALID_CHAN = 'INVALID'

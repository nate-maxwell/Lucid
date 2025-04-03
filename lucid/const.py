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

ENV_ROLE = 'LUCID_ROLE'
ENV_DCC = 'DCC'

# ----------Messages-------------------------------------------------------------------------------

ASSET_CHAN = 'asset'
ANIM_CHAN = 'anim'
RENDER_CHAN = 'render'
TEXTURE_CHAN = 'texture'
INVALID_CHAN = 'invalid'

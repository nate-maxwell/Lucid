"""
# Lucid Global Variables and Constants

* Update History

    `2023-09-19` - Init
"""


import getpass
from pathlib import Path

import lucid.io_utils


# Lucid Pipeline Paths
LUCID_PATH = Path(__file__).parent
CONFIG_PATH = Path(LUCID_PATH, 'config')
PYTHON_EXEC_PATH = Path(LUCID_PATH.parent, 'venv', 'Scripts', 'python.exe')
VENV_SITE_PACKAGES = Path(LUCID_PATH.parent, 'venv/Lib/site-packages')


# User Details
USER = getpass.getuser()
USER_SETTINGS_DIR = lucid.io_utils.user_data_dir('lucid_settings')

# Configs
DEVELOPER_CONFIG_PATH = Path(CONFIG_PATH, 'developer.json')
NETWORK_CONFIG_PATH = Path(CONFIG_PATH, 'network.json')
NAMING_CONFIG_PATH = Path(CONFIG_PATH, 'naming_conventions.json')

if lucid.io_utils.import_data_from_json(NETWORK_CONFIG_PATH)['CONSISTENT']:
    PROGRAM_CONFIG_PATH = Path(CONFIG_PATH, 'program_paths.json')
else:
    PROGRAM_CONFIG_PATH = Path(USER_SETTINGS_DIR, 'program_paths.json')

PATHS_CONFIG = lucid.io_utils.import_data_from_json(PROGRAM_CONFIG_PATH)
PROJECTS_PATH = Path(PATHS_CONFIG['PROJECTS'])

# Launcher
LAUNCHER_PATH = Path(LUCID_PATH, 'launcher')


# UI Resources
RESOURCE_PATH = Path(LUCID_PATH, 'resources')
DEFAULT_TEX_PATH = Path(RESOURCE_PATH, 'default_textures')


# Maya
MAYA_EXEC = Path(PATHS_CONFIG['DCC']['MAYA'])
MAYA_BASE_PATH = MAYA_EXEC.parent.parent
MAYA_SITE_PACKAGES = Path(MAYA_BASE_PATH, 'Python', 'Lib', 'site-packages')
MAYA_USER_SETUP_PATH = Path(LUCID_PATH, 'maya', '_userSetup')

MAYA_RIG_COMP_PATH = Path(LUCID_PATH.parent, 'rigging', 'components', 'maya')


# Unreal
UNREAL_EXEC = PATHS_CONFIG['DCC']['UNREAL']
LUCID_UNREAL_PATH = Path(LUCID_PATH, 'unreal')


# Substance Painter
PAINTER_EXEC = PATHS_CONFIG['DCC']['SUBSTANCE_PAINTER']


# Substance Designer
DESIGNER_EXEC = PATHS_CONFIG['DCC']['SUBSTANCE_DESIGNER']

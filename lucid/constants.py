"""
# Lucid Global Variables and Constants

* Update History

    `2023-09-19` - Init
"""


import getpass
from pathlib import Path

import lucid.io_utils
import lucid.config


"""Lucid Pipeline Paths"""
LUCID_REPO = Path(__file__).parent.parent
LUCID_PATH = Path(LUCID_REPO, 'lucid')
CONFIG_PATH = Path(LUCID_PATH, 'config')
PYTHON_EXEC_PATH = Path(LUCID_PATH.parent, 'venv', 'Scripts', 'python.exe')
VENV_SITE_PACKAGES = Path(LUCID_PATH.parent, 'venv/Lib/site-packages')


"""User Details"""
USER = getpass.getuser()
USER_SETTINGS_DIR = lucid.io_utils.user_data_dir('lucid_settings')


"""Launcher"""
LAUNCHER_PATH = Path(LUCID_PATH, 'launcher')


"""UI Resources"""
RESOURCE_PATH = Path(LUCID_PATH, 'resources')
DEFAULT_TEX_PATH = Path(RESOURCE_PATH, 'default_textures')


"""Environment Variables"""
ENV_ROLE = 'LUCID_ROLE'
ENV_PROJECT = 'LUCID_PROJECT'
ENV_ASSET = 'LUCID_ASSET'
ENV_CATEGORY = 'LUCID_CATEGORY'
ENV_CONTEXT = 'LUCID_CONTEXT'
ENV_SUBCONTEXT = 'LUCID_SUBCONTEXT'
ENV_DEV_LEVEL = 'LUCID_DEV_LEVEL'


"""Industry Standards"""
FPS_TYPES = {
    'game': 15,
    'film': 24,
    'pal': 25,
    'ntsc': 30,
    'show': 48,
    'palf': 50,
    'ntscf': 60
}


"""Maya"""
MAYA_EXEC = Path(lucid.config.PATHS_CONFIG['DCC']['MAYA'])
MAYA_BASE_PATH = MAYA_EXEC.parent.parent
MAYA_SITE_PACKAGES = Path(MAYA_BASE_PATH, 'Python', 'Lib', 'site-packages')
MAYA_USER_SETUP_PATH = Path(LUCID_PATH, 'maya', '_userSetup')

MAYA_RIG_COMP_PATH = Path(LUCID_PATH.parent, 'rigging', 'components', 'maya')


"""Unreal"""
UNREAL_EXEC = lucid.config.PATHS_CONFIG['DCC']['UNREAL']
LUCID_UNREAL_PATH = Path(LUCID_PATH, 'unreal')


"""Substance Painter"""
PAINTER_EXEC = lucid.config.PATHS_CONFIG['DCC']['SUBSTANCE_PAINTER']


"""Substance Designer"""
DESIGNER_EXEC = lucid.config.PATHS_CONFIG['DCC']['SUBSTANCE_DESIGNER']

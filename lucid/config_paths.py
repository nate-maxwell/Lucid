"""
# Config file IO

* Description

    This file is primarily for obtaining the project configs independently of constants or io utils
    to prevent circular dependencies. Therefore, some functionality may be redundant.

* Update History

    `2023-12-25` - Init
"""


import os
import json
from pathlib import Path
from typing import Optional


def _import_config_data(filepath: Path) -> Optional[dict]:
    """Import data from a .json file."""
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    else:
        return None


def _user_data_dir(filename: str) -> Path:
    """
    Returns a windows full path to the user-specific data dir for this application.

    Args:
        filename(str): The name of the file to access the user data dir for.

    Returns:
        Path: The user data path for the specified folder.
    """
    base_path = Path(os.getenv('LOCALAPPDATA'))
    app_path = Path(base_path, filename)
    return app_path


# Base Paths
USER_SETTINGS_DIR = _user_data_dir('lucid_settings')
_CONFIG_PATH = Path(Path(__file__).parent, 'config')

# Configs
DEVELOPER_CONFIG_PATH = Path(_CONFIG_PATH, 'developer.json')
NETWORK_CONFIG_PATH = Path(_CONFIG_PATH, 'network.json')
NAMING_CONFIG_PATH = Path(_CONFIG_PATH, 'naming_conventions.json')

if _import_config_data(NETWORK_CONFIG_PATH)['CONSISTENT']:
    PROGRAM_CONFIG_PATH = Path(_CONFIG_PATH, 'program_paths.json')
else:
    PROGRAM_CONFIG_PATH = Path(USER_SETTINGS_DIR, 'program_paths.json')

PATHS_CONFIG = _import_config_data(PROGRAM_CONFIG_PATH)
PROJECTS_PATH = Path(PATHS_CONFIG['PROJECTS'])

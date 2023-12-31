"""
# Unreal Paths

* Description

    A library of common pipeline related paths for Unreal.

* Update History

    `2023-09-24` - Init
"""


from pathlib import Path

import unreal


# Project level directories
PROJECT_DIR = Path(unreal.SystemLibrary.get_project_directory())
CONTENT_DIR = Path(unreal.SystemLibrary.get_project_content_directory())
CONFIG_DIR = Path(PROJECT_DIR, 'config')
PIPELINE_CONFIG_DIR = Path(CONFIG_DIR, 'pipeline')

# Project level ini configs
INI_EDITOR = Path(CONFIG_DIR, 'DefaultEditor.ini')
INI_LIGHTMASS = Path(CONFIG_DIR, 'DefaultLightmass.ini')
INI_EDITOR_SETTINGS = Path(CONFIG_DIR, 'DefaultEditorSettings.ini')
INI_ENGINE = Path(CONFIG_DIR, 'DefaultEngine.ini')
INI_GAME = Path(CONFIG_DIR, 'DefaultGame.ini')
INI_INPUT = Path(CONFIG_DIR, 'DefaultInput.ini')

# Lucid configs
SKELETON_CONFIG = Path(PIPELINE_CONFIG_DIR, 'skeleton.json')
MATERIAL_TYPE_CONFIG = Path(PIPELINE_CONFIG_DIR, 'material_type.json')

"""
# Unreal Editor Pipeline Plugin Manager

* Description:

    Autoloads pipeline friendly plugins.
"""


import json
from pathlib import Path

from lucid.unreal import editor
import lucid.unreal.paths

import unreal


PLUGIN_NAME_K = 'plugin_name'
PLUGIN_CMD_K = 'startup_cmd'

SHELF_ICON = unreal.Name('EditorViewport.ShaderComplexityMode')
BUTTON_ICON = unreal.Name('WidgetDesigner.LayoutTransform')


def load_toolbar_plugins() -> None:
    menu = editor.create_toolbar_submenu(section_name='Lucid',
                                         dropdown_name='Plugins',
                                         section_label='plugins',
                                         small_style_name=SHELF_ICON)
    for p in lucid.unreal.paths.PLUGINS_DIR.glob('*'):
        ctx_file = Path(p, 'context.json')
        if not ctx_file.exists():
            continue  # Not a pipeline friendly plugin

        with open(ctx_file) as file:
            ctx_data = json.load(file)
        label = ctx_data[PLUGIN_NAME_K]
        command = ctx_data[PLUGIN_CMD_K]

        editor.add_dropdown_button(
            menu_id=menu,
            label=label,
            command=command,
            section_label='plugins',
            small_style_name=BUTTON_ICON
        )

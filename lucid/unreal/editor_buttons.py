"""
# Unreal Editor Buttons

* Description

    The editor pipeline buttons embedded into the unreal 5 slate.

* Update History

    `2023-10-23` - Init
"""


import unreal


def create_button(section_name: str, command: str, name: str, small_style_name: unreal.Name) -> None:
    """
    Creates a button on the editor play toolbar from the given args. The button command is created
    in the caller function.

    Args:
        section_name(str): The toolbar section name to place the button in.

        command(Str): The python command for the button to execute. This usually should import and
        call the main() func of a module.

        name(str): The name of the button.

        small_style_name(unreal.Name): The name of the icon to use  for the button. Icon names can
        be found at: https://github.com/EpicKiwi/unreal-engine-editor-icons
    """
    tool_menu = unreal.ToolMenus.get()
    level_menu_bar = tool_menu.find_menu(unreal.Name('LevelEditor.LevelEditorToolBar.PlayToolbar'))
    level_menu_bar.add_section(section_name=unreal.Name(section_name), label=unreal.Text(section_name))

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(unreal.Text(name))
    entry.set_tool_tip(unreal.Text(f'Lucid {name}'))
    entry.set_icon(unreal.Name('EditorStyle'), small_style_name)
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=command
    )
    level_menu_bar.add_menu_entry(unreal.Name(section_name), entry)
    tool_menu.refresh_all_widgets()


def create_asset_importer_button() -> None:
    """Creates the asset importer button."""
    command = (
        'from lucid.unreal.asset_browser import main;'
        'global editor;'
        'editor = main()'
    )
    create_button('Lucid', command, 'Asset Browser',
                  unreal.Name('InputBindingEditor.MainFrame'))


def create_anim_importer_button() -> None:
    """Creates the anim importer button."""
    command = (
        'from lucid.unreal.anim_browser import main;'
        'global editor;'
        'editor = main()'
    )
    create_button('Lucid', command, 'Anim Browser',
                  unreal.Name('InputBindingEditor.MainFrame'))


def create_envvar_menu_button() -> None:
    """Creates the envvar menu  button."""
    command = (
        'from lucid.unreal.envvar_menu import main;'
        'global editor;'
        'editor = main()'
    )
    create_button('Lucid', command, 'Env Var Menu',
                  unreal.Name('MessageLog.Tutorial'))


def create_pipeline_settings_button() -> None:
    """Creates the pipeline settings button."""
    command = (
        "settings_menu = unreal.load_asset('/Lucid/UI/PipelineSettings/Pipeline_Settings')\n"
        "unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem).spawn_and_register_tab(settings_menu)"
    )
    create_button('Lucid', command, 'Pipeline Settings',
                  unreal.Name('AutomationTools.MenuIcon'))


def main() -> None:
    create_asset_importer_button()
    create_anim_importer_button()
    create_envvar_menu_button()
    create_pipeline_settings_button()


if __name__ == '__main__':
    main()

import unreal


_DEFAULT_ICON = unreal.Name('Log.TabIcon')
_OWNING_MENU = 'LevelEditor.LevelEditorToolBar.PlayToolBar'


def _get_play_toolbar(menu_name: str = _OWNING_MENU) -> unreal.ToolMenu:
    tool_menus = unreal.ToolMenus.get()
    return tool_menus.find_menu(
        unreal.Name(menu_name)
    )


def create_toolbar_submenu(section_name: str,
                           dropdown_name: str,
                           section_label: str,
                           small_style_name: unreal.Name = _DEFAULT_ICON
                           ) -> unreal.Name:
    """Add a dropdown to the Play toolbar.

    Args:
        section_name (str): The toolbar section to group under (created if
         missing).
        dropdown_name (str): The visible name of the dropdown.
        section_label (str): What label to give the created section.
        small_style_name(unreal.Name): The name of the icon to use  for the
         button. Icon names can be found at:
         https://github.com/EpicKiwi/unreal-engine-editor-icons
         Defaults to 'Log.TabIcon'.
    Returns:
        unreal.Name: The submenu id.
    """
    tool_menus = unreal.ToolMenus.get()
    play_toolbar = _get_play_toolbar()

    play_toolbar.add_section(
        section_name=unreal.Name(section_name),
        label=unreal.Text(section_name)
    )

    entry_name = unreal.Name(f'{dropdown_name.replace(" ", "")}')
    combo = unreal.ToolMenuEntry(
        name=entry_name,
        type=unreal.MultiBlockType.TOOL_BAR_COMBO_BUTTON
    )
    combo.set_label(unreal.Text(dropdown_name))
    combo.set_tool_tip(unreal.Text(dropdown_name))
    combo.set_icon(unreal.Name('EditorStyle'), small_style_name)
    play_toolbar.add_menu_entry(unreal.Name(section_name), combo)

    popup_id = unreal.Name(f'{_OWNING_MENU}.{entry_name}')
    popup = tool_menus.find_menu(popup_id) or tool_menus.register_menu(
        popup_id)
    popup.add_section(
        unreal.Name(section_label.title()),
        unreal.Text(section_label.lower())
    )

    tool_menus.refresh_all_widgets()
    return popup_id


def add_dropdown_button(menu_id: unreal.Name,
                        label: str,
                        command: str,
                        section_label: str,
                        small_style_name: unreal.Name = _DEFAULT_ICON) -> None:
    """Add a menu item to an existing drop-down menu.
    Args:
        menu_id (unreal.Name): The submenu id to add to.
        label (str): The entry label.
        command (str): The string python command for the button to exec.
        section_label (str): The submenu section label.
        small_style_name(unreal.Name): The name of the icon to use  for the
         button. Icon names can be found at:
         https://github.com/EpicKiwi/unreal-engine-editor-icons
         Defaults to 'Log.TabIcon'.
    """
    tool_menus = unreal.ToolMenus.get()
    popup = tool_menus.find_menu(menu_id) or tool_menus.register_menu(menu_id)
    popup.add_section(
        unreal.Name(section_label.title()),
        unreal.Text(section_label.lower())
    )

    str_id = unreal.StringLibrary.conv_name_to_string(menu_id)
    entry = unreal.ToolMenuEntry(
        name=unreal.Name(
            f'Item_{hash((str_id, label)) & 0xffffffff:x}'),
        type=unreal.MultiBlockType.MENU_ENTRY
    )
    entry.set_label(unreal.Text(label))
    entry.set_tool_tip(unreal.Text(label))
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=command
    )
    entry.set_icon(unreal.Name('EditorStyle'), small_style_name)

    popup.add_menu_entry(unreal.Name('actions'), entry)
    tool_menus.refresh_menu_widget(menu_id)


def create_toolbar_button(section_name: str,
                          label: str,
                          command: str,
                          small_style_name: unreal.Name = _DEFAULT_ICON
                          ) -> None:
    """
    Creates a button on the editor play toolbar from the given args. The button
    command is created in the caller function.

    Args:
        section_name(str): The toolbar section name to place the button in.
        command(Str): The python command for the button to execute.
         This usually should import and call the main() func of a module.
        label(str): The name of the button.
        small_style_name(unreal.Name): The name of the icon to use  for the
         button. Icon names can be found at:
         https://github.com/EpicKiwi/unreal-engine-editor-icons
         Defaults to 'Log.TabIcon'.
    """
    tool_menus = unreal.ToolMenus.get()

    play_toolbar = _get_play_toolbar()
    play_toolbar.add_section(
        section_name=unreal.Name(section_name),
        label=unreal.Text(section_name)
    )
    entry = unreal.ToolMenuEntry(
        name=unreal.Name(label),
        type=unreal.MultiBlockType.MENU_ENTRY
    )
    entry.set_label(unreal.Text(label))
    entry.set_tool_tip(unreal.Text(label))
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=command
    )
    entry.set_icon(unreal.Name('EditorStyle'), small_style_name)
    play_toolbar.add_menu_entry(unreal.Name(section_name), entry)

    tool_menus.refresh_all_widgets()

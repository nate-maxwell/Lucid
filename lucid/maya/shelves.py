"""
# Maya Custom Shelf Lib

* Description

    Lucid's shelf library and shelf manager.

* Update History

    `2023-09-21` - Init
"""

from pathlib import Path

import maya.cmds as cmds

import lucid.constants
import lucid.debug
import lucid.maya.developer
import lucid.maya.asset_publisher
import lucid.maya.asset_browser
import lucid.maya.anim_publisher
import lucid.maya.anim_browser
import lucid.maya.common_actions
import lucid.maya.environ_menu

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Base Class
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def _null(*args):
    pass


class LucidMayaShelf:
    """
    A simple class to build shelves in Maya.

    Args:
        name(str): The shelf name in Maya.

        icon_path(str): The path containing the icon files.
    """

    def __init__(self, name: str = 'customShelf', icon_path: str = lucid.constants.DEFAULT_TEX_PATH):
        self.name = name
        self.icon_path = icon_path

        self.label_background = (0, 0, 0, 0.5)
        self.label_color = (0.9, 0.9, 0.9)

        self._clean_old_shelf()
        cmds.setParent(self.name)
        self.build()
        self._last_item_alignment()

    def build(self) -> None:
        """
        This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.
        """

    def _clean_old_shelf(self) -> None:
        if cmds.shelfLayout(self.name, ex=1):
            if children := (cmds.shelfLayout(self.name, q=1, ca=1)):
                for child in children:
                    cmds.deleteUI(child)
        else:
            cmds.shelfLayout(self.name, p='ShelfLayout')

    def _last_item_alignment(self) -> None:
        """Last item is misaligned for some reason so another button is created and destroyed."""
        self.add_button('delete_me')
        items = cmds.shelfLayout(self.name, q=1, ca=1)
        cmds.deleteUI(items[-1])

    def add_button(self, label: str, icon: str = 'commandButton.png', command=_null, double_command=_null) -> None:
        """Adds a shelf button with the specified label, command, double click command, and image."""
        cmds.setParent(self.name)
        image = Path(self.icon_path, icon)
        if not image.exists():
            image = 'commandButton.png'

        cmds.shelfButton(width=40, height=40, image=image, l=label, command=command, dcc=double_command,
                         imageOverlayLabel=label, olb=self.label_background, olc=self.label_color,
                         fn='tinyBoldLabelFont')

    def add_menu_item(self, parent, label, icon: str = '', command=_null):
        """Adds a shelf menu item with the specified label, command, double click command, and image."""
        image = Path(self.icon_path, icon)
        if not image.exists():
            image = 'commandButton.png'

        return cmds.menuItem(p=parent, l=label, c=command, i=image)

    def add_sub_menu(self, parent: str, label: str, icon: str = ''):
        """Adds a sub menu item with the specified label, and optional image, to the specified parent popup menu."""
        image = Path(self.icon_path, icon).as_posix()
        return cmds.menuItem(p=parent, l=label, i=image, subMenu=1)

    @staticmethod
    def add_separator(style: str = 'none', height: int = 40, width: int = 16):
        """Adds a separator to space sections of the shelf apart."""
        return cmds.separator(style=style, h=height, w=width)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Custom Shelves
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

"""
Leaving this here for debugging. It allows the button on the shelf to update when I change code
without having to restart Maya.
"""


# def temp():
#     import importlib
#     importlib.reload(lucid.maya.asset_publisher)
#     lucid.maya.asset_publisher.main()


class LucidPrimaryShelf(LucidMayaShelf):
    """
    The main shelf for Lucid's actions.
    This may be separated into different shelves in the future.
    """

    def __init__(self):
        super().__init__('Lucid')

    def build(self) -> None:
        # Asset Browser
        self.add_button('Asset\nBrowsr', 'ICON_Default_Blue_40x40.png', lucid.maya.asset_browser.main)
        # Asset Publisher
        self.add_button('Asset\nPub', 'ICON_Default_Blue_40x40.png', lucid.maya.asset_publisher.main)

        self.add_separator()

        # Anim Browser
        self.add_button('Anim\nBrowsr', 'ICON_Default_Red_40x40.png', lucid.maya.anim_browser.main)
        # Anim Publisher
        self.add_button('Anim\nPub', 'ICON_Default_Red_40x40.png', lucid.maya.anim_publisher.main)


class LucidCommonActionShelf(LucidMayaShelf):
    """A shelf of common actions I use, put into convenient shelf button form."""

    def __init__(self):
        super().__init__('Common Actions')

    def build(self) -> None:
        self.add_button('Center\nPivot', 'ICON_Default_Blue_40x40.png', lucid.maya.common_actions.center_pivot)
        self.add_button('Freeze\nXforms', 'ICON_Default_Blue_40x40.png', lucid.maya.common_actions.freeze_transforms)
        self.add_button('Delete\nHistry', 'ICON_Default_Blue_40x40.png', lucid.maya.common_actions.delete_history)


class LucidDeveloper(LucidMayaShelf):
    """
    A shelf for pipeline based utilities and helper menus.
    This is primarily used for pipeline development, verifying, debugging, and troubleshooting,
    on artist pipeline problems by the pipeline team.
    """

    def __init__(self):
        super().__init__('Lucid_Dev')

    def build(self) -> None:
        # Environment Utils
        self.add_button(label='Edit\nEnv', icon='ICON_Default_Cyan_40x40.png',
                        command=lucid.maya.environ_menu.main)
        self.add_button(label='Print\nEnv', icon='ICON_Default_Cyan_40x40.png',
                        command=lucid.debug.print_environ_vars)
        self.add_button(label='Save\nEnv', icon='ICON_Default_Cyan_40x40.png',
                        command=lucid.debug.save_environment_log_to_drive)

        self.add_separator()

        # Module Reimporting
        self.add_button(label='Re\nImport', icon='ICON_Default_Yellow_40x40.png',
                        command=lucid.maya.developer.show_reimport_window)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Main block
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main() -> None:
    LucidPrimaryShelf()
    LucidDeveloper()


if __name__ == '__main__':
    main()

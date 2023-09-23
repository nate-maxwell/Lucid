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


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Base Class
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def _null(*args):
    pass


class LucidMayaShelf:
    """
    A simple class to build shelves in Maya.
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

    def build(self):
        """
        This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.
        """

    def _clean_old_shelf(self):
        if cmds.shelfLayout(self.name, ex=1):
            if children := (cmds.shelfLayout(self.name, q=1, ca=1)):
                for child in children:
                    cmds.deleteUI(child)
        else:
            cmds.shelfLayout(self.name, p='ShelfLayout')

    def _last_item_alignment(self):
        """Last item is misaligned for some reason so another button is created and destroyed."""
        self.add_button('delete_me')
        items = cmds.shelfLayout(self.name, q=1, ca=1)
        cmds.deleteUI(items[-1])

    def add_button(self, label: str, icon: str = 'commandButton.png', command=_null, double_command=_null):
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

    @staticmethod
    def add_separator(style: str = 'none', height: int = 40, width: int = 16):
        """Adds a separator to space sections of the shelf apart."""
        return cmds.separator(style=style, h=height, w=width)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Custom Shelves
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class LucidPrimaryShelf(LucidMayaShelf):
    """
    The main shelf for Lucid's actions.
    This may be separated into different shelves in the future.
    """
    def __init__(self):
        super().__init__('Lucid')

    def build(self):
        # Static Mesh Browser
        self.add_button('SM\nBrowsr', 'ICON_Default_Blue_40x40.png', _null)
        # Skeletal Messh Browser
        self.add_button('SK\nBrowsr', 'ICON_Default_Blue_40x40.png', _null)
        # Asset Publisher
        self.add_button('Asset\nPub', 'ICON_Default_Blue_40x40.png', _null)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Main block
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def main():
    LucidPrimaryShelf()


if __name__ == '__main__':
    main()

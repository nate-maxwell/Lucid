"""
# Lucid Toolbar

* Description:

    This is a maya shelf-like toolbar for use in various applications.
"""


from pathlib import Path
from typing import Callable
from typing import Optional

from PySide2 import QtCore
from PySide2 import QtWidgets

from lucid.core import gui_paths


def null(*args) -> None:
    """Dummy func that does nothing. A placeholder for menu items not yet
    assigned a connected function.
    """
    pass


DEFAULT_ICON = gui_paths.BUTTON_40X40_BLACK


class Toolbar(QtWidgets.QToolBar):
    def __init__(self, toolbar_name: str, parent=None) -> None:
        super().__init__(parent=parent)
        self.default_button_resolution: list[int] = [40, 40]
        self.icon_brightness: float = 0.2

        self.setObjectName(toolbar_name.replace(' ', '_'))
        self.setWindowTitle(toolbar_name)
        self.setMovable(False)
        self.build()

    def _make_toolbar_button(self,
                             button_image: Optional[Path] = DEFAULT_ICON
                             ) -> QtWidgets.QToolButton:
        """
        Boilerplate for making a toolbar button with an icon. If button_image is set to None,
        a blank item is added.

        Button w/h are set based on self.default_button_resolution.
        """
        tool_button = QtWidgets.QToolButton()
        tool_button.setContentsMargins(0, 0, 0, 0)
        tool_button.setFixedSize(self.default_button_resolution[0],
                                 self.default_button_resolution[1])
        if button_image is None:
            return tool_button

        tool_button.setStyleSheet(f"""
            QToolButton {{
                background: url('{button_image.as_posix()}');
                background-position: center;                /* Center the image */
                background-repeat: no-repeat;               /* Prevent tiling */
                background-size: cover;                     /* Scale the image to fill the button */
                background-color: rgba(0, 0, 0, 0.1);       /* Add a semi-transparent black overlay */
                font-size: 10px;
            }}
        """)

        return tool_button

    def add_toolbar_command(self, label: str, command: Callable = null,
                            image_path: Optional[Path] = DEFAULT_ICON) -> None:
        """Adds a toolbar button that is connected to the given command.

        Args:
            label(str): The button label.
            command(Callable): The function to connect to the button press, defaults to pass.
            image_path(Optional[Path]): The path to the button icon, if set to None: a blank item is added.
                Defaults to BUTTON_40X40_BLACK.
        """
        action = QtWidgets.QAction(label, self)
        action.triggered.connect(command)

        tool_button = self._make_toolbar_button(image_path)
        tool_button.setDefaultAction(action)
        self.addWidget(tool_button)

    def add_toolbar_submenu(self,
                            label: str,
                            image_path: Optional[Path] = DEFAULT_ICON
                            ) -> QtWidgets.QMenu:
        """Adds a submenu, a collapsable list of options, to the toolbar.

        Args:
            label(str): The menu label.
            image_path(Optional[Path]): The path to the menu icon, if set to None: a blank item is added.
                Defaults to BUTTON_40X40_BLACK.

        Returns:
            QtWidgets.QMenu: The created submenu, incase further submenus need to be added to the created
                submenu.
        """
        submenu = QtWidgets.QMenu(f'{label}_submenu', self)

        action = QtWidgets.QAction(label, self)  # The actual label on the dropdown
        action.setMenu(submenu)

        tool_button = self._make_toolbar_button(image_path)
        tool_button.setDefaultAction(action)
        tool_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        tool_button.setArrowType(QtCore.Qt.NoArrow)
        self.addWidget(tool_button)

        return submenu

    def add_submenu_submenu(self,
                            label: str,
                            parent: QtWidgets.QMenu) -> QtWidgets.QMenu:
        """Adds a nested submenu to the given submenu parent.

        Args:
            label(str): The submenu text label.
            parent(QtWidgets.QMenu): The menu to add the submenu to.

        Returns:
            QtWidgets.QMenu: The created submenu, incase further submenus need to be added to the created
                submenu.
        """
        submenu = QtWidgets.QMenu(f'{label}_submenu', self)
        action = QtWidgets.QAction(label, self)  # The actual label on the dropdown
        action.setMenu(submenu)
        parent.addMenu(submenu)

        return submenu

    @staticmethod
    def add_submenu_command(submenu: QtWidgets.QMenu,
                            cmd_name: str,
                            cmd: Callable = null) -> None:
        """Adds an item to the given submenu connected to the given command.

        Args:
            submenu(QtWidgets.QMenu): The submenu to add the item to.
            cmd_name(str): The text label for the added item.
            cmd(Callable): The function to connect the item selection to.
        """
        item = submenu.addAction(cmd_name)
        # noinspection PyUnresolvedReferences
        item.triggered.connect(cmd)

    sep_str: str = '---------------'

    def add_submenu_separator(self,
                              submenu: QtWidgets.QMenu,
                              label: str = sep_str) -> None:
        """Adds a dummy item to the given submenu, with the given label.
        Label defaults to ---------------.
        """
        self.add_submenu_command(submenu, label, null)

    def add_toolbar_separator(self,
                              width: int = 10) -> None:
        """Adds a horizontal spacer to the toolbar of the given width.
        Width defaults to 10.
        """
        wid = QtWidgets.QWidget()
        wid.setFixedWidth(width)
        self.addWidget(wid)

    def build(self) -> None:
        """The derived class's constructor.
        This will build the toolbar widgets/layout.
        """
        raise NotImplemented

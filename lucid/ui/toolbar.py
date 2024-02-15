"""
# Lucid Pipeline Toolbar

* Description:

    Lucid toolbar for DCCs. Small, effective, encompassing. This
    is meant to be the primary interface for users to begin
    using tools within the Mythos pipeline in Nuke and meant to
    look and feel like the maya shelf system.

* Update History:

    `2024-02-13` - Init
"""

from typing import Callable

import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtWidgets as QtGui


def _null(*args):
    pass


class Toolbar(QtWidgets.QWidget):
    """Base shelf class for the NukeShelves widget."""
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        expandingPolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(expandingPolicy)

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch()
        self.build()

    def build(self):
        """
        This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.
        """
        pass

    def add_button(self, label: str, command: Callable = _null):
        """
        Adds a button to the next space on the shelf.

        Args:
            label(str): The label to put on the button.
            Label will be 7pt Arial font.

            command(Callable): The function object tied
            to the button.
        """
        button = QtWidgets.QPushButton(label)
        button.setStyleSheet('font: 7pt Arial')
        button.setFixedSize(30, 30)
        button.clicked.connect(command)
        if self.layout.count() > 0:
            self.layout.insertWidget(self.layout.count() - 1, button)
        else:
            self.layout.insertWidget(0, button)

    def add_spacer(self):
        """Adds a 10px space to the end of the shelf."""
        spacer = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.layout.insertItem(self.layout.count() - 1, spacer)

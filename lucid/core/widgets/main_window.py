"""
# Main Window Wrapper

* Description:

    Boilerplate handler for Qt main windows.
"""


from typing import Optional

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import lucid.core.qt


class LMainWindow(QtWidgets.QMainWindow):
    def __init__(self,
                 window_title: str,
                 window_icon: Optional[QtGui.QIcon] = None,
                 parent_window: Optional[QtWidgets.QWidget] = None) -> None:
        """A simple wrapper for QMainWindow that eliminates some attribute
        and stylesheet setting.
        """
        if parent_window is not None:
            super(LMainWindow, self).__init__(parent_window)
        else:
            super().__init__()

        self.setWindowTitle(window_title)
        self.setObjectName(f'Lucid_{window_title.replace(" ", "")}')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        if window_icon:
            self.setWindowIcon(window_icon)

        self.widget_main = QtWidgets.QWidget()
        self.setCentralWidget(self.widget_main)
        self.layout_main = QtWidgets.QVBoxLayout()

        lucid.core.qt.set_pipeline_qss(self)

    def set_layout(self, layout: QtWidgets.QLayout) -> None:
        self.layout_main = layout
        self.widget_main.setLayout(self.layout_main)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        self.layout_main.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout) -> None:
        self.layout_main.addLayout(layout)

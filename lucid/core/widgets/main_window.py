"""
# Main Window Wrapper

* Description:

    Boilerplate handler for Qt main windows.
"""


from typing import cast
from typing import Optional

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import lucid.core.qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,
                 window_title: str,
                 window_icon: Optional[QtGui.QIcon] = None,
                 parent_window: Optional[QtWidgets.QWidget] = None) -> None:
        """A simple wrapper for QMainWindow that eliminates some attribute
        and stylesheet setting.
        """
        if parent_window is not None:
            super(MainWindow, self).__init__(parent_window)
        else:
            super().__init__()

        self.setWindowTitle(window_title)
        self.setObjectName(f'Lucid_{window_title.replace(" ", "")}')
        self.settings = QtCore.QSettings('Lucid', self.windowTitle())

        if window_icon:
            self.setWindowIcon(window_icon)

        self.widget_main = QtWidgets.QWidget()
        self.setCentralWidget(self.widget_main)
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.setStretch(0, 0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        lucid.core.qt.set_pipeline_qss(self)
        self._reload_geo()

    def closeEvent(self, event: QtCore.QEvent) -> None:
        """Save window geo before closing."""
        self.settings.setValue('window_geometry', self.saveGeometry())
        event.accept()

    def _reload_geo(self) -> None:
        saved_geo_val = self.settings.value('window_geometry')
        geometry = cast(QtCore.QByteArray, saved_geo_val)
        if geometry is not None:
            self.restoreGeometry(geometry)

    def set_layout(self, layout: QtWidgets.QLayout) -> None:
        self.layout_main = layout
        self.widget_main.setLayout(self.layout_main)
        self.layout_main.setStretch(0, 0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        self.layout_main.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout) -> None:
        self.layout_main.addLayout(layout)

    def add_stretch(self) -> None:
        self.layout_main.addStretch()

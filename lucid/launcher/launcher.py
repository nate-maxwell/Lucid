"""
# Lucid Pipeline Launcher GUI

* Description

    The main entry point for users into the Lucid Pipeline ecosystem.
"""


import sys
from pathlib import Path

from PySide2 import QtGui
from PySide2 import QtWidgets

# Outside (maybe) testing, this should be the only sys path management.
sys.path.append(Path(__file__).parent.parent.parent.as_posix())

from lucid.core import gui_paths
from lucid.core.widgets.main_window import LMainWindow
from lucid.core.widgets.labeled_combobox import LabeledComboBox


class LucidLauncherWindow(LMainWindow):
    def __init__(self) -> None:
        icon = QtGui.QIcon(gui_paths.launcher_icon.as_posix())
        super().__init__('Lucid Pipeline Launcher', icon)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self) -> None:
        self.cmb_projects = LabeledComboBox('Project:')

        self.hlayout_buttons = QtWidgets.QHBoxLayout()

        _btn_size = 100
        self.btn_launch_maya = QtWidgets.QPushButton('Maya')
        self.btn_launch_maya.setFixedSize(_btn_size, _btn_size)

        self.btn_launch_painter = QtWidgets.QPushButton('Substance\nPainter')
        self.btn_launch_painter.setFixedSize(_btn_size, _btn_size)

        self.btn_launch_designer = QtWidgets.QPushButton('Substance\nDesigner')
        self.btn_launch_designer.setFixedSize(_btn_size, _btn_size)

        self.btn_launch_unreal = QtWidgets.QPushButton('Unreal\nEngine')
        self.btn_launch_unreal.setFixedSize(_btn_size, _btn_size)

    def create_layouts(self) -> None:
        self.hlayout_buttons.addWidget(QtWidgets.QLabel('    '))
        self.hlayout_buttons.addWidget(self.btn_launch_maya)
        self.hlayout_buttons.addWidget(self.btn_launch_painter)
        self.hlayout_buttons.addWidget(self.btn_launch_designer)
        self.hlayout_buttons.addWidget(self.btn_launch_unreal)
        self.hlayout_buttons.addWidget(QtWidgets.QLabel('    '))

        self.set_layout(QtWidgets.QVBoxLayout())
        self.add_widget(self.cmb_projects)
        self.add_layout(self.hlayout_buttons)

    def create_connections(self) -> None:
        self.btn_launch_maya.clicked.connect(self.on_launch_maya)
        self.btn_launch_painter.clicked.connect(self.on_launch_painter)
        self.btn_launch_designer.clicked.connect(self.on_launch_designer)
        self.btn_launch_unreal.clicked.connect(self.on_launch_unreal)

    def on_launch_maya(self) -> None:
        ...

    def on_launch_painter(self) -> None:
        ...

    def on_launch_designer(self) -> None:
        ...

    def on_launch_unreal(self) -> None:
        ...


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    lucid_launcher_window = LucidLauncherWindow()
    lucid_launcher_window.show()

    app.exec_()


if __name__ == '__main__':
    main()

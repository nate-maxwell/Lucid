"""
# Lucid Pipeline Launcher GUI

* Description

    The main entry point for users into the Lucid Pipeline ecosystem.

* Update History

    `2023-09-19` - Init

    `2023-11-09` - Added renamer and placeholder project settings buttons.
"""


import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2 import QtCore

sys.path.append(Path(__file__).parent.parent.parent.as_posix())

import lucid.constants
import lucid.launch
import lucid.ui.qt


class LucidLauncherWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lucid Pipeline Launcher')
        self.setObjectName('LucidLauncher')
        lucid.ui.qt.set_pipeline_qss(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.hlayout_buttons = QtWidgets.QHBoxLayout()

        self.btn_maya_launch = QtWidgets.QPushButton('Maya')
        self.btn_maya_launch.setFixedSize(100, 80)
        self.btn_maya_launch.clicked.connect(self.launch_maya)

        self.btn_unreal_launch = QtWidgets.QPushButton('Unreal')
        self.btn_unreal_launch.setFixedSize(100, 80)
        self.btn_unreal_launch.clicked.connect(self.launch_unreal)

        self.btn_spainter_launch = QtWidgets.QPushButton('Substance\nPainter')
        self.btn_spainter_launch.setFixedSize(100, 80)
        self.btn_spainter_launch.clicked.connect(self.launch_spainter)

        self.btn_sdesigner_launch = QtWidgets.QPushButton('Substance\nDesigner')
        self.btn_sdesigner_launch.setFixedSize(100, 80)
        self.btn_sdesigner_launch.clicked.connect(self.launch_sdesigner)

        self.btn_pipeline_settings = QtWidgets.QPushButton('Pipeline\nSettings')
        self.btn_pipeline_settings.setFixedSize(100, 80)
        self.btn_pipeline_settings.clicked.connect(self.launch_pipeline_settings)

        self.btn_project_manager = QtWidgets.QPushButton('Project\nManager')
        self.btn_project_manager.setFixedSize(100, 80)
        self.btn_project_manager.clicked.connect(self.launch_project_manager)

        self.btn_batch_renamer = QtWidgets.QPushButton('Renamer')
        self.btn_batch_renamer.setFixedSize(100, 80)
        self.btn_batch_renamer.clicked.connect(self.launch_batch_renamer)

        self.hlayout_buttons.addStretch(100)
        self.hlayout_buttons.addWidget(self.btn_maya_launch)
        self.hlayout_buttons.addWidget(self.btn_unreal_launch)
        self.hlayout_buttons.addWidget(self.btn_spainter_launch)
        self.hlayout_buttons.addWidget(self.btn_sdesigner_launch)
        self.hlayout_buttons.addWidget(QtWidgets.QLabel(''))
        self.hlayout_buttons.addWidget(self.btn_pipeline_settings)
        self.hlayout_buttons.addWidget(self.btn_project_manager)
        self.hlayout_buttons.addWidget(self.btn_batch_renamer)
        self.hlayout_buttons.addStretch(100)

        self.launcher_widget = QtWidgets.QWidget()
        self.launcher_widget.setLayout(self.hlayout_buttons)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.launcher_widget)

        self.setCentralWidget(self.launcher_widget)

    @staticmethod
    def launch_maya():
        lucid.launch.launch_maya()

    @staticmethod
    def launch_unreal():
        lucid.launch.launch_unreal()

    def launch_spainter(self):
        pass

    def launch_sdesigner(self):
        pass

    def launch_pipeline_settings(self):
        lucid.launch.launch_pipeline_settings()

    @staticmethod
    def launch_project_manager():
        lucid.launch.launch_project_manager()

    @staticmethod
    def launch_batch_renamer():
        lucid.launch.launch_renamer()


def main():
    app = QtWidgets.QApplication(sys.argv)
    lucid_launcher_window = LucidLauncherWindow()
    lucid_launcher_window.show()

    app.exec_()


if __name__ == '__main__':
    main()

"""
# Lucid Pipeline Launcher GUI

* Description:

    The main entry point for users into the Lucid Pipeline ecosystem.

* Update History:

    `2023.09.19` - Init
"""


import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2 import QtCore

appended = Path(__file__).parent.parent.parent.as_posix()
sys.path.append(appended)

import lucid.constants


class LucidLauncherWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lucid Pipeline Launcher')
        self.setObjectName('LucidLauncher')
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
        self.btn_pipeline_settings.clicked.connect(self.launch_sdesigner)

        self.hlayout_buttons.addStretch(100)
        self.hlayout_buttons.addWidget(self.btn_maya_launch)
        self.hlayout_buttons.addWidget(self.btn_unreal_launch)
        self.hlayout_buttons.addWidget(self.btn_spainter_launch)
        self.hlayout_buttons.addWidget(self.btn_sdesigner_launch)
        self.hlayout_buttons.addWidget(self.btn_pipeline_settings)
        self.hlayout_buttons.addStretch(100)

        self.launcher_widget = QtWidgets.QWidget()
        self.launcher_widget.setLayout(self.hlayout_buttons)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.launcher_widget)

        self.setCentralWidget(self.launcher_widget)

    def launch_maya(self):
        pass

    def launch_unreal(self):
        pass

    def launch_spainter(self):
        pass

    def launch_sdesigner(self):
        pass

    def launch_pipeline_settings(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    lucid_launcher_window = LucidLauncherWindow()
    lucid_launcher_window.show()

    qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
    with open(qss_path, 'r') as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)

    app.exec_()


if __name__ == '__main__':
    main()

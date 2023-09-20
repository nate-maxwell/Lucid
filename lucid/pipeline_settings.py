"""
# Lucid Pipeline Settings UI

* Description

    Pipeline settings menu UI for users to customize the pipeline experience
    for their teams.

* Update History

    `2023.09.19` - Init
"""


import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2 import QtCore

import lucid.constants
import lucid.io_utils


network_config = lucid.io_utils.import_data_from_json(lucid.constants.NETWORK_CONFIG_PATH)


class LucidSettingsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lucid Pipeline Settings')
        self.setObjectName('PipelineSettingsMenu')
        self.setMinimumSize(600, 600)

        self.network_settings = lucid.io_utils.import_data_from_json(lucid.constants.NETWORK_CONFIG_PATH)
        self.developer_settings = lucid.io_utils.import_data_from_json(lucid.constants.DEVELOPER_CONFIG_PATH)

        if not lucid.constants.USER_SETTINGS_DIR.exists():
            lucid.io_utils.create_folder(lucid.constants.USER_SETTINGS_DIR)

        self.program_paths = lucid.constants.PATHS_CONFIG

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.load_settings()

    def create_widgets(self):
        # Main Layout
        self.layout_main = QtWidgets.QVBoxLayout()

        # Network
        self.grp_network = QtWidgets.QGroupBox('Network')
        self.hlayout_network = QtWidgets.QHBoxLayout()
        self.rdo_common_network = QtWidgets.QRadioButton('Common Network')
        self.rdo_local_networks = QtWidgets.QRadioButton('Local Networks')
        self.rdo_local_networks.setChecked(True)

        # Program Install Pattern
        self.grp_install = QtWidgets.QGroupBox('Install Directories')
        self.hlayout_install = QtWidgets.QHBoxLayout()
        self.rdo_consistent = QtWidgets.QRadioButton('Consistent')
        self.rdo_inconsistent = QtWidgets.QRadioButton('Inconsistent')
        self.rdo_inconsistent.setChecked(True)

        # Traceback Options
        self.grp_traceback = QtWidgets.QGroupBox('Tracebacks')
        self.hlayout_traceback = QtWidgets.QHBoxLayout()
        self.cbx_debug = QtWidgets.QCheckBox('Debug')
        self.cbx_dev = QtWidgets.QCheckBox('Dev')

        # Executable Locations
        self.grp_programs = QtWidgets.QGroupBox('Programs')
        self.flayout_programs = QtWidgets.QFormLayout()
        self.le_maya_exe = QtWidgets.QLineEdit('')
        self.le_unreal_exe = QtWidgets.QLineEdit('')
        self.le_substance_painter_exe = QtWidgets.QLineEdit('')
        self.le_substance_designer_exe = QtWidgets.QLineEdit('')

        # Extra Directories
        self.grp_extra_directories = QtWidgets.QGroupBox('Extra Directories')
        self.flayout_directories = QtWidgets.QFormLayout()
        self.le_projects_path = QtWidgets.QLineEdit('')

        self.hlayout_save_settings = QtWidgets.QHBoxLayout()
        self.btn_save = QtWidgets.QPushButton('Save Settings')
        self.btn_save.setFixedSize(100, 40)

    def create_layout(self):
        self.hlayout_network.addWidget(self.rdo_common_network)
        self.hlayout_network.addWidget(self.rdo_local_networks)
        self.grp_network.setLayout(self.hlayout_network)

        self.hlayout_install.addWidget(self.rdo_consistent)
        self.hlayout_install.addWidget(self.rdo_inconsistent)
        self.grp_install.setLayout(self.hlayout_install)

        self.hlayout_traceback.addWidget(self.cbx_debug)
        self.hlayout_traceback.addWidget(self.cbx_dev)
        self.grp_traceback.setLayout(self.hlayout_traceback)

        self.flayout_programs.addRow('Maya', self.le_maya_exe)
        self.flayout_programs.addRow('Unreal', self.le_unreal_exe)
        self.flayout_programs.addRow('Substance Painter', self.le_substance_painter_exe)
        self.flayout_programs.addRow('Substance Designer', self.le_substance_designer_exe)
        self.grp_programs.setLayout(self.flayout_programs)

        self.flayout_directories.addRow('Project Path', self.le_projects_path)
        self.grp_extra_directories.setLayout(self.flayout_directories)

        self.hlayout_save_settings.addWidget(self.btn_save)
        self.hlayout_save_settings.addStretch()

        self.layout_main.addWidget(self.grp_network)
        self.layout_main.addWidget(self.grp_install)
        self.layout_main.addWidget(self.grp_traceback)
        self.layout_main.addWidget(self.grp_programs)
        self.layout_main.addWidget(self.grp_extra_directories)
        self.layout_main.addLayout(self.hlayout_save_settings)

        self.setLayout(self.layout_main)

    def create_connections(self):
        self.btn_save.clicked.connect(self.save_settings)

    def load_settings(self):
        self.rdo_consistent.setChecked(self.network_settings['CONSISTENT'])
        self.rdo_inconsistent.setChecked(not self.rdo_consistent.isChecked())

        self.rdo_common_network.setChecked(self.network_settings['COMMON_NETWORK'])
        self.rdo_local_networks.setChecked(not self.rdo_common_network.isChecked())

        self.cbx_dev.setChecked(self.developer_settings['DEV'])
        self.cbx_debug.setChecked(self.developer_settings['DEBUG'])

        if maya := self.program_paths['DCC']['MAYA']:
            self.le_maya_exe.setText(maya)

        if unreal := self.program_paths['DCC']['UNREAL']:
            self.le_unreal_exe.setText(unreal)

        if painter := self.program_paths['DCC']['SUBSTANCE_PAINTER']:
            self.le_substance_painter_exe.setText(painter)

        if designer := self.program_paths['DCC']['SUBSTANCE_DESIGNER']:
            self.le_substance_designer_exe.setText(designer)

        if projects := self.program_paths['PROJECTS']:
            self.le_projects_path.setText(projects)

    def save_settings(self):
        self.network_settings['CONSISTENT'] = self.rdo_consistent.isChecked()
        self.network_settings['COMMON_NETWORK'] = self.rdo_common_network.isChecked()
        lucid.io_utils.export_data_to_json(lucid.constants.NETWORK_CONFIG_PATH, self.network_settings, True)

        self.developer_settings['DEV'] = self.cbx_dev.isChecked()
        self.developer_settings['DEBUG'] = self.cbx_debug.isChecked()
        lucid.io_utils.export_data_to_json(lucid.constants.DEVELOPER_CONFIG_PATH, self.developer_settings, True)

        self.program_paths['DCC']['MAYA'] = self.le_maya_exe.text()
        self.program_paths['DCC']['UNREAL'] = self.le_unreal_exe.text()
        self.program_paths['DCC']['SUBSTANCE_PAINTER'] = self.le_substance_painter_exe.text()
        self.program_paths['DCC']['SUBSTANCE_DESIGNER'] = self.le_substance_designer_exe.text()
        self.program_paths['PROJECTS'] = self.le_projects_path.text()

        if self.rdo_consistent.isChecked():
            lucid.io_utils.export_data_to_json(Path(lucid.constants.CONFIG_PATH, 'program_paths.json'),
                                               self.program_paths, True)
        else:
            lucid.io_utils.export_data_to_json(Path(lucid.constants.USER_SETTINGS_DIR, 'program_paths.json'),
                                               self.program_paths, True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    lucid_settings_window = LucidSettingsWindow()
    lucid_settings_window.show()

    qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
    with open(qss_path, 'r') as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)

    app.exec_()


if __name__ == '__main__':
    main()

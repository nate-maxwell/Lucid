"""
# Maya Anim Browser

* Description

    Anim file browser and importer.

* Update History

    `2023-10-05` - Init
"""


from pathlib import Path

from PySide2 import QtWidgets

import lucid.constants
import lucid.io_utils
import lucid.maya
import lucid.maya.io
from lucid.ui.components import LucidFileBrowser


global window_singleton


class AnimBrowser(LucidFileBrowser):
    def __init__(self):
        columns = ['Project', 'Category', 'Set', 'Name', 'Direction']
        super().__init__(columns, lucid.constants.PROJECTS_PATH, (1024, 850), (1280, 850), lucid.maya.get_maya_window())

        global window_singleton
        window_singleton = self
        self.setWindowTitle('Lucid Anim Browser')

        qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
        with open(qss_path, 'r') as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

        self.columns[0].populate_column(lucid.io_utils.list_folder_contents(lucid.constants.PROJECTS_PATH))
        self.asset_files_directory = Path()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self):
        # Main
        self.main_widget = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)

        # IO
        self.widget_io = QtWidgets.QWidget()
        self.widget_io.setFixedWidth(250)
        self.vlayout_io = QtWidgets.QVBoxLayout()
        self.btn_import = QtWidgets.QPushButton('Open')

        # Version
        self.grp_version = QtWidgets.QGroupBox('Version')
        self.vlayout_version = QtWidgets.QHBoxLayout()
        self.cmb_version = QtWidgets.QComboBox()

        # IO Metadata
        self.grp_meta = QtWidgets.QGroupBox('Metadata')
        self.flayout_metadata = QtWidgets.QFormLayout()
        self.le_notes = QtWidgets.QLineEdit()
        self.le_user = QtWidgets.QLineEdit()
        self.le_date = QtWidgets.QLineEdit()
        self.le_time = QtWidgets.QLineEdit()

    def create_layout(self):
        # IO Metadata
        self.grp_meta.setLayout(self.flayout_metadata)
        self.flayout_metadata.addRow('User', self.le_user)
        self.flayout_metadata.addRow('Notes', self.le_notes)
        self.flayout_metadata.addRow('Date', self.le_date)
        self.flayout_metadata.addRow('Time', self.le_time)

        # Version
        self.grp_version.setLayout(self.vlayout_version)
        self.vlayout_version.addWidget(self.cmb_version)

        # IO Column
        self.widget_io.setLayout(self.vlayout_io)
        self.vlayout_io.addWidget(self.btn_import)
        self.vlayout_io.addWidget(self.grp_version)
        self.vlayout_io.addWidget(self.grp_meta)
        self.vlayout_io.addStretch()

        # Main
        self.layout_main.addLayout(self.hlayout_columns)
        self.layout_main.addWidget(self.widget_io)

    def create_connections(self):
        self.cmb_version.currentTextChanged.connect(self.cmb_version_connection)
        self.btn_import.clicked.connect(self.open_file)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def base_path(self) -> Path:
        return Path(lucid.constants.PROJECTS_PATH, self.columns[0].selected_item, 'Anim')

    def column_action(self, index: int):
        if index == 0:
            path = self.base_path
        elif index == 1:
            path = Path(self.base_path, self.columns[1].selected_item)
        elif index == 2:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item)
        elif index == 3:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                        self.columns[3].selected_item, 'Maya')
        elif index == 4:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                        self.columns[3].selected_item, 'Maya', self.columns[4].selected_item, 'ma')
            self.asset_files_directory = path
            self.set_version_contents_from_path(path)
        else:
            path = self.base_path

        items = lucid.io_utils.list_folder_contents(path)
        if not index + 1 == len(self.columns):
            self.columns[index + 1].populate_column(items)
            self.clear_columns_right_of(index + 1)
            self.cmb_version.clear()

    def set_version_contents_from_path(self, path: Path):
        """
        Fills the version combobox with all versions of the current file.

        Args:
            path(Path): The path to the current asset's directory.
        """
        self.cmb_version.clear()
        version_files = []
        for i in lucid.io_utils.list_folder_contents(path):
            if str(i).endswith('.ma'):
                version_files.append(i)
        self.cmb_version.addItems(version_files)

    def cmb_version_connection(self):
        if self.cmb_version.currentText():
            metadata_path = self.file_path.with_suffix('.json')
            if metadata_path.exists():
                data = lucid.io_utils.import_data_from_json(metadata_path)
                self.le_notes.setText(data['Notes'])
                self.le_user.setText(data['User'])
                self.le_date.setText(data['Date'])
                self.le_time.setText(data['Time'])
            else:
                self.le_notes.clear()
                self.le_user.clear()
                self.le_date.clear()
                self.le_time.clear()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def file_path(self) -> Path:
        """The full file path to the file, as defined by the UI elements."""
        return Path(self.asset_files_directory, self.cmb_version.currentText())

    def open_file(self):
        lucid.maya.io.open_file(self.file_path)


def main():
    global window_singleton
    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except NameError:
        pass

    window_singleton = AnimBrowser()
    window_singleton.show()


if __name__ == '__main__':
    main()

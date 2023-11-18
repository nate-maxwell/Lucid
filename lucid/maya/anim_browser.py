"""
# Maya Anim Browser

* Description

    Anim file browser and importer.

* Update History

    `2023-10-05` - Init

    `2023-11-11` - Window now dynamically reads directories from tools_directory.json.
    Window now also sets pipeline environment variables when opening an animation.
"""


import os
from pathlib import Path

from PySide2 import QtWidgets

import lucid.constants
import lucid.schema
import lucid.io_utils
import lucid.maya
import lucid.maya.io
import lucid.ui.qt
from lucid.ui.components import LucidFileBrowser


global window_singleton


class AnimBrowser(LucidFileBrowser):
    def __init__(self):
        self.token_structure = lucid.schema.get_token_structure('maya_anim_browser')
        columns = lucid.schema.get_variable_tokens_keys(self.token_structure)
        super().__init__(columns, lucid.constants.PROJECTS_PATH, (1024, 850), (1280, 850), lucid.maya.get_maya_window())

        global window_singleton
        window_singleton = self
        self.setWindowTitle('Lucid Anim Browser')
        lucid.ui.qt.set_pipeline_qss(self)

        self.columns[0].populate_column(lucid.io_utils.list_folder_contents(lucid.constants.PROJECTS_PATH))
        self.asset_files_directory = Path()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self) -> None:
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

    def create_layout(self) -> None:
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

    def create_connections(self) -> None:
        self.cmb_version.currentTextChanged.connect(self.cmb_version_connection)
        self.btn_import.clicked.connect(self.open_file)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def column_action(self, index: int) -> None:
        path = self.get_path_to_index(index + 1)
        if index == len(self.columns) - 1:
            self.asset_files_directory = path
            self.set_version_contents_from_path(path)
            return
        else:
            self.clear_columns_right_of(index + 1)
            self.cmb_version.clear()
            items = lucid.io_utils.list_folder_contents(self.get_path_to_index(index + 1))
            self.columns[index + 1].populate_column(items)

    def set_version_contents_from_path(self, path: Path) -> None:
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

    def cmb_version_connection(self) -> None:
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
        """
        The full file path to the file, as defined by the UI elements.

        Returns:
            Path: Calculated file path.
        """
        return Path(self.get_path_to_index(len(self.columns)), self.cmb_version.currentText())

    def get_path_to_index(self, index: int) -> Path:
        """
        Collects row values to create a token list and return a path up to the specified
        row's index. This is procedurally done with lucid.schema.create_path_from_tokens.

        Args:
            index(int): The row number to create the path up to.

        Returns:
            Path: The generated path, up to the given index. If the path does not exist,
            a path equal to '/does/not/exist' will be returned instead.
        """
        tokens = []
        for c in self.columns:
            if c.id < index:
                tokens.append(c.selected_item)

        try:
            return lucid.schema.create_path_from_tokens(tokens, 'maya_anim_browser')
        except TypeError:
            return Path('/does/not/exist')

    def set_pipe_environment_vars(self) -> None:
        """
        Sets the relevant maya environment vars for the pipeline.
        These vars are largely the asset context.
        """
        project_token = lucid.schema.get_tool_schema_value('maya_asset_browser',
                                                           'project_related_token')
        project = self.get_selected_by_column_label(project_token)
        os.environ[lucid.constants.ENV_PROJECT] = project
        os.environ[lucid.constants.ENV_ROLE] = 'ANIM'

    def open_file(self) -> None:
        self.set_pipe_environment_vars()
        lucid.maya.io.open_file(self.file_path)


def main() -> None:
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

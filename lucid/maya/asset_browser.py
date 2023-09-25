"""
# Maya Asset Browser

* Description

    The primary asset browser for Lucid in Maya.

* Update History

    `2023-09-23` - Init
"""


import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import maya.cmds

import lucid.constants
import lucid.io_utils
import lucid.maya
import lucid.maya.io
import lucid.legex
from lucid.ui.components import LucidFileBrowser


global window_singleton


class AssetBrowser(LucidFileBrowser):
    def __init__(self):
        columns = ['Project', 'Category', 'Set', 'Asset', 'LoD']
        super().__init__(columns, lucid.constants.PROJECTS_PATH, (1024, 850), (1280, 850), lucid.maya.get_maya_window())

        global window_singleton
        window_singleton = self

        qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
        with open(qss_path, 'r') as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

        self.columns[0].populate_column(lucid.io_utils.list_folder_contents(lucid.constants.PROJECTS_PATH))

        self.default_image_path = Path(lucid.constants.RESOURCE_PATH, 'default_textures', 'T_NoPreview.png')
        self.asset_files_directory = Path()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)

        self.vlayout_import_components = QtWidgets.QVBoxLayout()

        # Import buttons
        self.grp_import_actions = QtWidgets.QGroupBox('File Actions')
        self.vlayout_import_actions = QtWidgets.QVBoxLayout()
        self.btn_open = QtWidgets.QPushButton('Open')
        self.btn_import = QtWidgets.QPushButton('Import')
        self.btn_reference = QtWidgets.QPushButton('Reference')
        self.btn_swap_ref = QtWidgets.QPushButton('Swap Ref')
        self.btn_remove_ref = QtWidgets.QPushButton('Remove Ref')

        # Version control
        self.grp_version = QtWidgets.QGroupBox('Version')
        self.vlayout_version = QtWidgets.QVBoxLayout()
        self.cmb_version = QtWidgets.QComboBox()

        # Metadata
        self.grp_metadata = QtWidgets.QGroupBox('Metadata')
        self.flayout_metadata = QtWidgets.QFormLayout()
        self.le_notes = QtWidgets.QLineEdit()
        self.le_pub_date = QtWidgets.QLineEdit()
        self.le_author = QtWidgets.QLineEdit()

        # Preview image
        self.grp_preview = QtWidgets.QGroupBox('Preview')
        self.vlayout_preview = QtWidgets.QVBoxLayout()
        self.img_thumbnail_preview = QtWidgets.QLabel('Test')
        self.update_pixmap()
        self.img_thumbnail_preview.setPixmap(self.pixmap_preview)

    def create_layout(self):
        # Import Actions
        self.grp_import_actions.setLayout(self.vlayout_import_actions)
        self.vlayout_import_actions.addWidget(self.btn_open)
        self.vlayout_import_actions.addWidget(self.btn_import)
        self.vlayout_import_actions.addWidget(self.btn_reference)
        self.vlayout_import_actions.addWidget(self.btn_swap_ref)
        self.vlayout_import_actions.addWidget(self.btn_remove_ref)

        # Version
        self.grp_version.setLayout(self.vlayout_version)
        self.vlayout_version.addWidget(self.cmb_version)

        # Metadata
        self.grp_metadata.setLayout(self.flayout_metadata)
        self.flayout_metadata.addRow('Notes', self.le_notes)
        self.flayout_metadata.addRow('Date', self.le_pub_date)
        self.flayout_metadata.addRow('Author', self.le_author)

        # Preview
        self.grp_preview.setLayout(self.vlayout_preview)
        self.vlayout_preview.addWidget(self.img_thumbnail_preview)

        # Import Column
        self.vlayout_import_components.addWidget(self.grp_import_actions)
        self.vlayout_import_components.addWidget(self.grp_version)
        self.vlayout_import_components.addWidget(self.grp_metadata)
        self.vlayout_import_components.addWidget(self.grp_preview)
        self.vlayout_import_components.addStretch()

        # Main
        self.layout_main.addLayout(self.hlayout_columns)
        self.layout_main.addLayout(self.vlayout_import_components)

    def create_connections(self):
        self.btn_open.clicked.connect(self.open_asset)
        self.btn_import.clicked.connect(self.import_asset)
        self.btn_reference.clicked.connect(self.reference_asset)
        self.btn_swap_ref.clicked.connect(self.swap_reference)
        self.btn_remove_ref.clicked.connect(self.remove_reference)
        self.cmb_version.currentTextChanged.connect(self.cmb_version_connection)

    def debug(self):
        print(self.asset_files_directory)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def update_pixmap(self, image_path: Path = None):
        """
        Updates and resets the pixmap to display the asset thumbnail.

        Args:
            image_path(Path): The file path to the image.
        """
        if not image_path:
            image_path = self.default_image_path

        self.pixmap_preview = QtGui.QPixmap(image_path.as_posix())
        self.pixmap_preview = self.pixmap_preview.scaled(384, 384, QtCore.Qt.KeepAspectRatio)
        self.img_thumbnail_preview.setPixmap(self.pixmap_preview)

    def set_version_contents_from_path(self, path: Path):
        """
        Fills the version combobox with all versions of the current file.

        Args:
            path(Path): The path to the current asset's directory, including
            LoD and extension folders.
        """
        self.cmb_version.clear()
        version_files = []
        for i in lucid.io_utils.list_folder_contents(path):
            if str(i).endswith('.ma'):
                version_files.append(i)
        self.cmb_version.addItems(version_files)

    def update_metadata(self):
        json_path = self.file_path.with_suffix('.json')
        if json_path.exists():
            data = lucid.io_utils.import_data_from_json(json_path)
            self.le_notes.setText(data['Notes'])
            self.le_pub_date.setText(data['Date'])
            self.le_author.setText(data['User'])
        else:
            self.le_notes.clear()
            self.le_pub_date.clear()
            self.le_author.clear()

    def cmb_version_connection(self):
        if self.cmb_version.currentText():
            texture_path = self.file_path.with_suffix('.jpg')
            if texture_path.exists():
                self.update_pixmap(texture_path)
            else:
                self.update_pixmap()
        else:
            pass

        self.update_metadata()

    @property
    def base_path(self) -> Path:
        return Path(lucid.constants.PROJECTS_PATH, self.columns[0].selected_item, 'Asset')

    @property
    def path_to_file_dir(self) -> Path:
        path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                    self.columns[3].selected_item, 'Maya', 'Model', self.columns[4].selected_item,
                    self.columns[5].selected_item, 'ma')
        return path

    def column_action(self, index: int):
        if index == 0:
            path = self.base_path
        elif index == 1:
            path = Path(self.base_path, self.columns[1].selected_item)
        elif index == 2:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item)
        elif index == 3:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                        self.columns[3].selected_item, 'Maya', 'Model')
        elif index == 4:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                        self.columns[3].selected_item, 'Maya', 'Model', self.columns[4].selected_item, 'ma')
            self.asset_files_directory = path
            self.set_version_contents_from_path(path)
            return
        else:
            path = self.base_path

        items = lucid.io_utils.list_folder_contents(path)
        if not index + 1 == len(self.columns):
            self.columns[index + 1].populate_column(items)
            self.clear_columns_right_of(index + 1)

            self.cmb_version.clear()
            self.update_pixmap()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def file_path(self) -> Path:
        """The full file path to the file, as defined by the UI elements."""
        return Path(self.asset_files_directory, self.cmb_version.currentText())

    def open_asset(self):
        """Opens the selected maya ascii file."""
        print(self.file_path)
        if self.file_path.exists():
            lucid.maya.io.open_file(self.file_path)
        else:
            print('No valid file selected.')

    def import_asset(self):
        """Imports the maya ascii file into the scene."""
        options = lucid.maya.io.MayaAsciiImportOptions()
        options.filepath = self.file_path
        lucid.maya.io.import_ma(options)

    def reference_asset(self):
        """References the maya ascii file into the scene."""
        options = lucid.maya.io.MayaAsciiReferenceOptions()
        options.filepath = self.file_path
        lucid.maya.io.reference_ma(options)

    def swap_reference(self):
        """
        Swaps all selected references to another file.

        Selection can either be the transform node of the actor,
        or the reference node itself.

        More than one selection is allowed, but all selected referenced
        actors will be swapped.
        """
        selected = maya.cmds.ls(sl=True)
        if len(selected) == 0:
            return

        references = []
        number = None
        for i in selected:
            name = i.split(':')[0]

            if name[-1].isnumeric():
                number = lucid.legex.get_trailing_numbers(name)
                base_name = name.split(str(number))[0]
                if base_name.endswith('RN'):
                    references.append(name)
                else:
                    references.append(f'{base_name}RN{number}')
            else:
                if name.endswith('RN'):
                    references.append(name)
                else:
                    references.append(f'{name}RN')

        for ref in references:
            maya.cmds.file(self.file_path, loadReference=ref)

    def remove_reference(self):
        """Removes the referenced asset from the scene."""
        maya.cmds.file(self.file_path, removeReference=True)


def main():
    global window_singleton
    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except NameError:
        pass

    window_singleton = AssetBrowser()
    window_singleton.show()


if __name__ == '__main__':
    main()

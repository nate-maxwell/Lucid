"""
# Maya Asset Publisher

* Description

    The primary asset publisher from maya to the rest of the lucid ecosystem.

* Update History

    `2023-09-22` - Init

    `2023-09-23` - Added basic metadata support + bug fixes.
"""


import os
from pathlib import Path

from PySide2 import QtWidgets
from maya import cmds

import lucid.constants
import lucid.io_utils
import lucid.maya
import lucid.maya.io
import lucid.maya.confirm_window


global window_singleton


class MayaAssetPublisher(QtWidgets.QMainWindow):
    def __init__(self):
        super(MayaAssetPublisher, self).__init__(lucid.maya.get_maya_window())

        global window_singleton
        window_singleton = self

        self.setWindowTitle('Asset Publisher')
        self.setMinimumSize(300, 400)

        qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
        with open(qss_path, 'r') as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

        self.projects_path = Path(lucid.constants.PATHS_CONFIG['PROJECTS'])

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.initialize_boxes()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    UI Construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self):
        self.layout_main = QtWidgets.QVBoxLayout()
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        # Publish Options
        self.grp_publish_params = QtWidgets.QGroupBox('Publish Options')
        self.vlayout_options = QtWidgets.QVBoxLayout()
        self.rows = []
        index = 0
        for i in ['Project', 'Category', 'Set', 'Name', 'LoD']:
            row = EnvironmentComboBox(self, i, [], index)
            self.rows.append(row)
            self.vlayout_options.addLayout(row)
            index += 1
        self.rows[0].set_box_contents(lucid.io_utils.list_folder_contents(self.projects_path))

        self.hlayout_types = QtWidgets.QHBoxLayout()
        self.grp_dcc_type = QtWidgets.QGroupBox('DCC Type')
        self.vlayout_dcc_type = QtWidgets.QVBoxLayout()
        self.rdo_maya = QtWidgets.QRadioButton('Maya')
        self.rdo_maya.setChecked(True)
        self.rdo_unreal = QtWidgets.QRadioButton('Unreal')

        self.grp_file_type = QtWidgets.QGroupBox('File Type')
        self.vlayout_file_type = QtWidgets.QVBoxLayout()
        self.rdo_ascii = QtWidgets.QRadioButton('Maya Ascii')
        self.rdo_ascii.setChecked(True)
        self.rdo_fbx = QtWidgets.QRadioButton('FBX')

        self.grp_notes = QtWidgets.QGroupBox('Notes')
        self.le_notes = QtWidgets.QLineEdit()
        self.hlayout_notes = QtWidgets.QHBoxLayout()

        self.btn_publish_asset = QtWidgets.QPushButton('Publish Asset')

    def create_layout(self):
        self.main_widget.setLayout(self.layout_main)

        self.grp_publish_params.setLayout(self.vlayout_options)

        self.hlayout_types.addWidget(self.grp_dcc_type)
        self.grp_dcc_type.setLayout(self.vlayout_dcc_type)
        self.vlayout_dcc_type.addWidget(self.rdo_maya)
        self.vlayout_dcc_type.addWidget(self.rdo_unreal)

        self.hlayout_types.addWidget(self.grp_file_type)
        self.grp_file_type.setLayout(self.vlayout_file_type)
        self.vlayout_file_type.addWidget(self.rdo_ascii)
        self.vlayout_file_type.addWidget(self.rdo_fbx)

        self.grp_notes.setLayout(self.hlayout_notes)
        self.hlayout_notes.addWidget(self.le_notes)

        self.layout_main.addWidget(self.grp_publish_params)
        self.layout_main.addLayout(self.hlayout_types)
        self.layout_main.addWidget(self.grp_notes)
        self.layout_main.addWidget(self.btn_publish_asset)
        self.layout_main.addStretch()

    def create_connections(self):
        self.rdo_unreal.clicked.connect(self.rdo_unreal_connection)
        self.rdo_maya.clicked.connect(self.rdo_maya_connection)
        self.btn_publish_asset.clicked.connect(self.publish_asset)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def initialize_boxes(self):
        """Sets the startup values of each row's combobox."""
        for row in self.rows:
            if row.index + 1 < len(self.rows):
                self.populate_box_at_index(row.index + 1)

    def populate_box_at_index(self, index: int):
        """
        Fills the combobox of the row's index based on previous row's selections.
        Will autopopulate the following boxes with first possible path.

        If the path formed does not exist, then all remaining boxes will be cleared.
        """
        path = Path(self.projects_path, self.rows[0].selected_item, 'Asset')
        if not path.exists():
            self.clear_rows_from_index(1)
            return
        for row in self.rows:
            if 0 < row.index < index:
                if row.index == 3:
                    # Fix context token to 'Model' for asset pubbing
                    if self.rdo_maya.isChecked():
                        path = Path(path, row.selected_item, 'Maya', 'Model')
                    elif self.rdo_unreal.isChecked():
                        path = Path(path, row.selected_item, 'Unreal', 'Model')
                else:
                    path = Path(path, row.selected_item)

            elif row.index == index:
                row.set_box_contents(lucid.io_utils.list_folder_contents(path))
                if not path.exists():
                    self.clear_rows_from_index(index + 1)
                self.populate_box_at_index(index + 1)

    def clear_rows_from_index(self, index: int):
        """Empties each row's combo box at and after the given index."""
        for row in self.rows:
            if row.index >= index:
                row.set_box_contents([])

    def rdo_unreal_connection(self):
        self.rdo_ascii.setChecked(False)
        self.rdo_fbx.setChecked(True)

    def rdo_maya_connection(self):
        self.rdo_ascii.setChecked(True)
        self.rdo_fbx.setChecked(False)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def asset_path(self) -> Path:
        """The path of the current asset, before file type."""
        path = Path(self.projects_path, self.rows[0].selected_item, 'Asset')
        for row in self.rows:
            if row.index > 0:
                if row.index == 3:
                    if self.rdo_maya.isChecked():
                        path = Path(path, row.selected_item, 'Maya', 'Model')
                    elif self.rdo_unreal.isChecked():
                        path = Path(path, row.selected_item, 'Unreal', 'Model')
                else:
                    path = Path(path, row.selected_item)

        return path

    @property
    def base_file_path(self) -> Path:
        """The full file path to the current asset."""
        if self.rdo_fbx.isChecked():
            ext = 'fbx'
        elif self.rdo_ascii.isChecked():
            ext = 'ma'
        else:
            ext = 'fbx'

        asset_name = f'{self.rows[3].selected_item}_{self.rows[4].selected_item}.{ext}'
        path = Path(self.asset_path, ext, asset_name)
        return path

    def create_meta_dict(self):
        """
        Creates a dict of the metadata values for the asset publish and saves it to a json.
        The json file is the same as self.base_file_path but with a .json extension.
        """
        meta = {}
        ext = self.base_file_path.suffix
        version = lucid.io_utils.get_next_version_from_dir(self.base_file_path.parent, ext)

        for row in self.rows:
            meta[row.row_name] = row.selected_item
        meta['Type'] = 'Asset'
        meta['Time'] = lucid.io_utils.get_time()
        meta['Date'] = lucid.io_utils.get_date()
        meta['Version'] = version
        meta['User'] = lucid.constants.USER
        meta['Notes'] = self.le_notes.text()

        json_file = self.base_file_path.with_suffix('.json')
        lucid.io_utils.export_data_to_json(json_file, meta, True)

    def generate_thumbnail(self):
        """
        Generates the asset thumbnail for the asset browser. Uses current viewport camera.
        Thumbnail is named after asset without version number. Asset is deselected during
        thumbnail capturing and reselected after.

        Returns:
            str: the path to the generated thumbnail.
        """
        thumbnail_path = self.base_file_path.parent
        asset_name = f'{self.rows[3].selected_item}_{self.rows[4].selected_item}'
        target_name = Path(thumbnail_path, asset_name)
        frame = cmds.currentTime(query=True)
        generated_path = Path(thumbnail_path, f'{asset_name}.{str(int(frame))}.jpg')

        selection = cmds.ls(sl=True)
        cmds.select(clear=True)

        cmds.playblast(startTime=frame, endTime=frame, forceOverwrite=True, format='image', filename=target_name,
                       offScreen=True, clearCache=True, viewer=False, showOrnaments=0, framePadding=0, percent=100,
                       compression='jpg', quality=100, widthHeight=[512, 512])

        # maya includes frame number in generated image name, so copy/paste with correct name and remove old one
        lucid.io_utils.copy_file(generated_path, thumbnail_path, f'{target_name}.jpg')
        lucid.io_utils.delete_file(generated_path)

        cmds.select(selection)

        return Path(thumbnail_path, f'{target_name}.jpg')

    def publish_initial_textures(self):
        pub_texture_path = Path(self.base_file_path.parent, 'textures')
        if lucid.io_utils.list_folder_contents(pub_texture_path, True):
            return

        for node in cmds.ls(type='file'):
            source_path = Path(cmds.getAttr(node + '.fileTextureName'))
            current_name = source_path.name
            ext = source_path.suffix
            filename = current_name.split('.')[0]

            version_padding = 3
            initial_version_num = '1'.zfill(version_padding)

            initial_pub_name = f'{filename}_v{initial_version_num}{ext}'
            initial_pub_path = Path(pub_texture_path, initial_pub_name)

            if not initial_pub_path.exists():
                lucid.io_utils.copy_file(source_path, pub_texture_path)
                os.rename(Path(pub_texture_path, current_name), initial_pub_path)

            cmds.setAttr((node + '.fileTextureName'), initial_pub_path, type='string')

    def publish_asset(self):
        """
        The primary asset publishing switch.
        Should more DCCs or file types need to be added, here is where they should go.
        """
        if cmds.objExists(self.rows[1].selected_item):
            print(f'PUBLISHING ASSET to {self.base_file_path.parent}')
            lucid.io_utils.create_folder(self.base_file_path.parent)
            self.generate_thumbnail()

            if self.rdo_maya.isChecked():
                if self.rdo_ascii.isChecked():
                    print('Pubbing Maya Ascii')
                    self.publish_maya_ascii()

                elif self.rdo_fbx.isChecked():
                    print('Pubbing Maya FBX')
                    self.publish_maya_fbx()

            elif self.rdo_unreal.isChecked():
                if self.rdo_ascii.isChecked():
                    print('Not a valid publish options, try again.')

                elif self.rdo_fbx.isChecked():
                    print('Pubbing Unreal FBX')
                    self.publish_unreal_fbx()

            self.create_version_file()
        else:
            line1 = f'No null named "{self.rows[1].selected_item}" found.'
            line2 = 'Assets must be children of a category null!'
            warning = f'{line1}\n{line2}'
            lucid.maya.confirm_window.info(warning)

    def publish_maya_ascii(self):
        self.publish_initial_textures()
        options = lucid.maya.io.MayaAsciiExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_ma(options)
        self.create_meta_dict()

    def publish_maya_fbx(self):
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_fbx(options)
        self.create_meta_dict()

    def publish_unreal_fbx(self):
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_fbx(options)
        self.create_meta_dict()

    def create_version_file(self):
        """Copies the published file and renames it based on its version number."""
        file_name = self.base_file_path.name
        ext = self.base_file_path.suffix
        base_name = file_name.split(ext)[0]
        version = lucid.io_utils.get_next_version_from_dir(self.base_file_path.parent, ext)
        print('VERSION:: ', version)
        version_base_name = f'{base_name}_v{version}'
        version_file_name = f'{version_base_name}{ext}'
        lucid.io_utils.copy_file(self.base_file_path, self.base_file_path.parent, version_file_name)  # Base file
        lucid.io_utils.copy_file(self.base_file_path.with_suffix('.json'), self.base_file_path.parent,  # Json file
                                 version_base_name)
        lucid.io_utils.copy_file(self.base_file_path.with_suffix('.jpg'), self.base_file_path.parent,  # thumbnail fail
                                 f'{version_base_name}')


class EnvironmentComboBox(QtWidgets.QHBoxLayout):
    def __init__(self, parent_ui: MayaAssetPublisher,
                 label: str, contents: list[str], index: int):
        super().__init__()

        self.parent_ui = parent_ui
        self.row_name = label
        self.index = index
        self.lbl_name = QtWidgets.QLabel(self.row_name)
        self.cmb_combobox = QtWidgets.QComboBox()
        self.cmb_combobox.addItems(contents)
        self.btn_add = QtWidgets.QPushButton('+')
        self.btn_add.setFixedSize(20, 20)

        self.addWidget(self.lbl_name)
        self.addWidget(self.cmb_combobox)
        self.addWidget(self.btn_add)

        self.cmb_combobox.activated.connect(self.update_parent)
        self.btn_add.clicked.connect(self.button_add_item)

    def update_parent(self):
        """Updates the following rows on the parent."""
        self.parent_ui.populate_box_at_index(self.index + 1)

    def button_add_item(self):
        """Adds the input to the combobox and updates the following rows."""
        item = QtWidgets.QInputDialog.getText(self.parent_ui, f'New {self.row_name}',
                                              f'New {self.row_name}' 'Name: ')
        selection = item[0]
        if selection:
            self.cmb_combobox.addItem(selection)
            self.cmb_combobox.setCurrentText(selection)

        self.parent_ui.populate_box_at_index(self.index + 1)

    @property
    def selected_item(self):
        """Shortened namespace way to get combo box value."""
        return self.cmb_combobox.currentText()

    def set_box_contents(self, contents: list[str]):
        """Sets the items of the combobox to the given list."""
        self.cmb_combobox.clear()
        if contents:
            self.cmb_combobox.addItems(contents)
        else:
            self.cmb_combobox.addItems([''])


def main():
    """Close and crate UI in singleton fashion."""
    global window_singleton
    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except NameError:
        pass

    window_singleton = MayaAssetPublisher()
    window_singleton.show()


if __name__ == '__main__':
    main()

"""
# Unreal Asset Browser

* Description

    The primary asset browser UI for unreal in Lucid.

* Update History

    `2023-09-24` - Init
"""


import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import unreal

import lucid.constants
import lucid.ui.components
import lucid.io_utils
import lucid.unreal.file_io
import lucid.unreal.paths


global window_singleton


class UnrealAssetBrowser(lucid.ui.components.LucidFileBrowser):
    def __init__(self):
        columns = ['Project', 'Category', 'Set', 'Asset', 'LoD']
        super().__init__(columns, lucid.constants.PROJECTS_PATH, (1024, 850), (1280, 850))

        global window_singleton
        window_singleton = self

        qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
        with open(qss_path, 'r') as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

        self.default_image_path = Path(lucid.constants.RESOURCE_PATH, 'default_textures', 'T_NoPreview.png')
        self.asset_files_directory = Path('does/not/exist')
        self.skeletons_dict = lucid.io_utils.import_data_from_json(lucid.unreal.paths.SKELETON_CONFIG)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        projects = lucid.io_utils.list_folder_contents(lucid.constants.PROJECTS_PATH)
        self.columns[0].populate_column(projects)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)

        self.vlayout_columns = QtWidgets.QVBoxLayout()
        self.vlayout_import_options = QtWidgets.QVBoxLayout()

        # Action buttons
        self.btn_asset_import = QtWidgets.QPushButton('Import')
        self.btn_asset_refresh = QtWidgets.QPushButton('Refresh')

        self.grp_skeleton_type = QtWidgets.QGroupBox('Skeleton')
        self.hlayout_skeleton_type = QtWidgets.QHBoxLayout()
        self.cmb_skeleton_type = QtWidgets.QComboBox()
        self.cmb_skeleton_type.addItems(self.skeletons_dict.keys())
        self.cmb_skeleton_type.addItem('FBX Included')

        self.grp_uniform_scale = QtWidgets.QGroupBox('Uniform Scale')
        self.hlayout_uniform_scale = QtWidgets.QHBoxLayout()
        self.sbx_uniform_scale = QtWidgets.QDoubleSpinBox()
        self.sbx_uniform_scale.setValue(1.0)

        self.grp_location_offset = QtWidgets.QGroupBox('Location Offset (X,Y,Z)')
        self.hlayout_location_offset = QtWidgets.QHBoxLayout()
        self.sbx_loc_x = QtWidgets.QDoubleSpinBox()
        self.sbx_loc_y = QtWidgets.QDoubleSpinBox()
        self.sbx_loc_z = QtWidgets.QDoubleSpinBox()

        self.grp_rotation_offset = QtWidgets.QGroupBox('Rotation Offset(X,Y,Z)')
        self.hlayout_rotation_offset = QtWidgets.QHBoxLayout()
        self.sbx_rot_x = QtWidgets.QDoubleSpinBox()
        self.sbx_rot_y = QtWidgets.QDoubleSpinBox()
        self.sbx_rot_z = QtWidgets.QDoubleSpinBox()

        self.grp_misc = QtWidgets.QGroupBox('Misc')
        self.vlayout_misc = QtWidgets.QVBoxLayout()
        self.cbx_merge_mesh = QtWidgets.QCheckBox('Merge Mesh')
        self.cbx_convert_materials = QtWidgets.QCheckBox('Convert Materials')

        # Preview Image
        self.grp_preview = QtWidgets.QGroupBox('Preview')
        self.hlayout_preview = QtWidgets.QHBoxLayout()
        self.img_thumbnail_preview = QtWidgets.QLabel()
        self.update_pixmap()
        self.img_thumbnail_preview.setPixmap(self.pixmap_preview)

    def create_layout(self):
        self.grp_skeleton_type.setLayout(self.hlayout_skeleton_type)
        self.hlayout_skeleton_type.addWidget(self.cmb_skeleton_type)

        self.grp_uniform_scale.setLayout(self.hlayout_uniform_scale)
        self.hlayout_uniform_scale.addWidget(self.sbx_uniform_scale)

        self.grp_location_offset.setLayout(self.hlayout_location_offset)
        self.hlayout_location_offset.addWidget(self.sbx_loc_x)
        self.hlayout_location_offset.addWidget(self.sbx_loc_y)
        self.hlayout_location_offset.addWidget(self.sbx_loc_z)

        self.grp_rotation_offset.setLayout(self.hlayout_rotation_offset)
        self.hlayout_rotation_offset.addWidget(self.sbx_rot_x)
        self.hlayout_rotation_offset.addWidget(self.sbx_rot_y)
        self.hlayout_rotation_offset.addWidget(self.sbx_rot_z)

        self.grp_misc.setLayout(self.vlayout_misc)
        self.vlayout_misc.addWidget(self.cbx_merge_mesh)
        self.vlayout_misc.addWidget(self.cbx_convert_materials)

        self.grp_preview.setLayout(self.hlayout_preview)
        self.hlayout_preview.addWidget(self.img_thumbnail_preview)

        self.vlayout_import_options.addWidget(QtWidgets.QLabel(''))
        self.vlayout_import_options.addWidget(self.btn_asset_import)
        self.vlayout_import_options.addWidget(self.btn_asset_refresh)
        self.vlayout_import_options.addWidget(self.grp_skeleton_type)
        self.vlayout_import_options.addWidget(self.grp_uniform_scale)
        self.vlayout_import_options.addWidget(self.grp_location_offset)
        self.vlayout_import_options.addWidget(self.grp_rotation_offset)
        self.vlayout_import_options.addWidget(self.grp_misc)
        self.vlayout_import_options.addWidget(self.grp_preview)

        self.vlayout_import_options.addStretch()
        self.layout_main.addLayout(self.hlayout_columns)
        self.layout_main.addLayout(self.vlayout_columns)
        self.layout_main.addLayout(self.vlayout_import_options)

    def create_connections(self):
        self.btn_asset_import.clicked.connect(self.import_asset)
        self.btn_asset_refresh.clicked.connect(self.btn_refresh_connection)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def update_pixmap(self, image_path: Path = None):
        """Updates the preview thumbnail image."""
        if not image_path:
            image_path = self.default_image_path

        self.pixmap_preview = QtGui.QPixmap(image_path.as_posix())
        self.pixmap_preview = self.pixmap_preview.scaled(384, 384, QtCore.Qt.KeepAspectRatio)
        self.img_thumbnail_preview.setPixmap(self.pixmap_preview)

    def show_preview_from_selection(self):
        """A callback for the row manager class to update the image."""
        asset_name = f'{self.columns[3].selected_item}_{self.columns[4].selected_item}.jpg'
        thumbnail_path = Path(self.asset_files_directory, asset_name)
        self.update_pixmap(thumbnail_path)

    @property
    def base_path(self) -> Path:
        return Path(lucid.constants.PROJECTS_PATH, self.columns[0].selected_item, 'Asset')

    @property
    def path_to_file_dir(self) -> Path:
        path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                    self.columns[3].selected_item, 'Unreal', 'Model', self.columns[4].selected_item,
                    self.columns[5].selected_item, 'fbx')
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
                        self.columns[3].selected_item, 'Unreal', 'Model')
        elif index == 4:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                        self.columns[3].selected_item, 'Unreal', 'Model', self.columns[4].selected_item, 'fbx')
            self.asset_files_directory = path
            self.show_preview_from_selection()
            # self.set_version_contents_from_path(path)
            return
        else:
            path = self.base_path

        if path.exists():
            items = lucid.io_utils.list_folder_contents(path)
            if not index + 1 == len(self.columns):
                self.columns[index + 1].populate_column(items)
                self.clear_columns_right_of(index + 1)

                self.update_pixmap()

    def btn_refresh_connection(self):
        self.clear_columns_right_of(0)
        self.columns[0].deselect_item()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def column_item_by_index(self, index: int) -> str:
        """
        Shorthand way to get the selected item of a column by index number.
        Args:
            index(int): The column index to retrieve.

        Returns:
            str: The selected value of the specified column.
        """
        return self.columns[index].selected_item

    def all_columns_check(self) -> bool:
        """
        Loops through each column to make sure there is a selected item.

        Returns:
            bool: Returns False if a single column.selected_item == None,
            else returns True.
        """
        for i in self.columns:
            if not i.selected_item:
                return False
        else:
            return True

    @property
    def asset_file_path(self) -> Path:
        """
        The full file path to the asset from the selected UI values.

        Returns:
            Path: Returns the path of valid, else returns Path('/does/not/exist').
        """
        if self.all_columns_check():
            asset_name = f'{self.column_item_by_index(3)}_{self.column_item_by_index(4)}.fbx'
            path = Path(lucid.constants.PROJECTS_PATH, self.column_item_by_index(0), 'Asset',
                        self.column_item_by_index(1), self.column_item_by_index(2),
                        self.column_item_by_index(3), 'Unreal', 'Model',
                        self.column_item_by_index(4), 'fbx', asset_name)
            return path
        else:
            return Path('/does/not/exist')

    def import_asset(self):
        """All procedures and functions that take place when importing an asset."""
        if not self.asset_file_path.exists():
            return

        asset_name = f'{self.column_item_by_index(2)}_{self.column_item_by_index(3)}'
        # TODO: Make this dynamically build from /Game/ downwards
        destination_package_path = f'/Game/02_Assets/{self.column_item_by_index(1)}/{self.column_item_by_index(2)}/{asset_name}'
        loc = unreal.Vector(self.sbx_loc_x.value(), self.sbx_loc_y.value(), self.sbx_loc_z.value())
        rot = unreal.Rotator(self.sbx_rot_x.value(), self.sbx_rot_y.value(), self.sbx_rot_z.value())

        if self.columns[1].selected_item == 'env':
            lucid.unreal.file_io.import_static_mesh(self.asset_file_path.as_posix(),
                                                    destination_package_path,
                                                    asset_name,
                                                    loc,
                                                    rot,
                                                    self.sbx_uniform_scale.value(),
                                                    self.cbx_merge_mesh.isChecked())
        else:
            if self.cmb_skeleton_type.currentText() == 'FBX Included':
                skeleton = None
            else:
                skeleton = unreal.load_asset(self.skeletons_dict[self.cmb_skeleton_type.currentText()])
            lucid.unreal.file_io.import_skeletal_mesh(self.asset_file_path.as_posix(),
                                                      destination_package_path,
                                                      skeleton,
                                                      asset_name,
                                                      loc,
                                                      rot,
                                                      self.sbx_uniform_scale.value())

        unreal.EditorAssetLibrary.save_directory(destination_package_path)

        if self.cbx_convert_materials.isChecked():
            pass  # TODO: hook up material conversion for imported fbx files.


def main():
    global window_singleton

    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except:
        pass

    if not QtWidgets.QApplication.instance():
        QtWidgets.QApplication(sys.argv)
    else:
        QtWidgets.QApplication.instance()

    window_singleton = UnrealAssetBrowser()
    window_singleton.show()
    unreal.parent_external_window_to_slate(window_singleton.winId())


if __name__ == '__main__':
    main()
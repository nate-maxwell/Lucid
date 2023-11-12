"""
# Unreal Asset Browser

* Description

    The primary asset browser UI for unreal in Lucid.

* Update History

    `2023-09-24` - Init
"""


import os
import sys
from pathlib import Path

from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import unreal

import lucid.constants
import lucid.schema
import lucid.ui.components
import lucid.io_utils
import lucid.legex
import lucid.unreal.file_io
import lucid.unreal.paths
import lucid.unreal.lod


global window_singleton


class UnrealAssetBrowser(lucid.ui.components.LucidFileBrowser):
    def __init__(self):
        self.token_structure = lucid.schema.get_token_structure('unreal_asset_browser')
        columns = lucid.schema.get_variable_tokens_keys(self.token_structure)
        super().__init__(columns, lucid.constants.PROJECTS_PATH, (1024, 850), (1280, 850))

        global window_singleton
        window_singleton = self

        qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
        with open(qss_path, 'r') as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

        self.setWindowTitle('Lucid Asset Browser')
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

    def create_widgets(self) -> None:
        self.main_widget = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)

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

        self.grp_rotation_offset = QtWidgets.QGroupBox('Rotation Offset (X,Y,Z)')
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

    def create_layout(self) -> None:
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
        self.layout_main.addLayout(self.vlayout_import_options)

    def create_connections(self) -> None:
        self.btn_asset_import.clicked.connect(self.import_asset)
        self.btn_asset_refresh.clicked.connect(self.btn_refresh_connection)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def update_pixmap(self, image_path: Path = None) -> None:
        """Updates the preview thumbnail image."""
        if not image_path:
            image_path = self.default_image_path

        self.pixmap_preview = QtGui.QPixmap(image_path.as_posix())
        self.pixmap_preview = self.pixmap_preview.scaled(384, 384, QtCore.Qt.KeepAspectRatio)
        self.img_thumbnail_preview.setPixmap(self.pixmap_preview)

    def show_preview_from_selection(self) -> None:
        """A callback for the row manager class to update the image."""
        asset_name_token = lucid.schema.get_tool_schema_value('unreal_asset_browser',
                                                              'asset_name_related_token')
        asset_name = f'{self.get_selected_by_column_label(asset_name_token)}_Model.jpg'
        thumbnail_path = Path(self.get_path_to_index(len(self.columns) + 1), asset_name)
        self.update_pixmap(thumbnail_path)

    def column_action(self, index: int) -> None:
        path = self.get_path_to_index(index + 1)
        if index == len(self.columns) - 1:
            self.asset_files_directory = path
            self.show_preview_from_selection()
            return
        else:
            self.clear_columns_right_of(index + 1)
            items = lucid.io_utils.list_folder_contents(path)
            if not index + 1 == len(self.columns):
                self.columns[index + 1].populate_column(items)

    def btn_refresh_connection(self) -> None:
        self.clear_columns_right_of(0)
        self.columns[0].deselect_item()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def asset_file_path(self) -> Path:
        """
        The full file path to the source asset from the selected UI values,
        to be imported into the engine.

        Returns:
            Path: Returns the path of valid, else returns Path('/does/not/exist').
        """
        if self.all_columns_check():
            print(self.asset_name)
            path = Path(self.get_path_to_index(len(self.columns)), self.asset_name)
            print(path)
            return path
        else:
            return Path('/does/not/exist')

    @property
    def asset_name(self) -> str:
        asset_name_token = lucid.schema.get_tool_schema_value('unreal_asset_browser',
                                                              'asset_name_related_token')
        return f'{self.get_selected_by_column_label(asset_name_token)}_Model.fbx'

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
            return lucid.schema.create_path_from_tokens(tokens, 'unreal_asset_browser')
        except TypeError:
            return Path('/does/not/exist')

    def set_pipe_environment_vars(self) -> None:
        """Sets the relevant maya environment vars for the pipeline."""
        project_token = lucid.schema.get_tool_schema_value('unreal_asset_browser',
                                                           'project_related_token')
        project = self.get_selected_by_column_label(project_token)
        os.environ[lucid.constants.ENV_PROJECT] = project
        os.environ[lucid.constants.ENV_ROLE] = 'ASSET'

    def import_env(self, destination_package_path: str, asset_name: str, loc: unreal.Vector, rot: unreal.Rotator) -> None:
        lod_index = lucid.legex.get_trailing_numbers(self.columns[4].selected_item)
        if lod_index == 0:
            lucid.unreal.file_io.import_static_mesh(self.asset_file_path,
                                                    destination_package_path,
                                                    asset_name,
                                                    loc,
                                                    rot,
                                                    self.sbx_uniform_scale.value(),
                                                    self.cbx_merge_mesh.isChecked())
        else:
            lucid.unreal.lod.import_sm_lod(destination_package_path, lod_index, self.asset_file_path.as_posix())

    def import_skel(self, destination_package_path: str, asset_name: str, loc: unreal.Vector, rot: unreal.Rotator) -> None:
        lod_index = lucid.legex.get_trailing_numbers(self.columns[4].selected_item)
        if lod_index == 0:
            if self.cmb_skeleton_type.currentText() == 'FBX Included':
                skeleton = None
            else:
                skeleton = unreal.load_asset(self.skeletons_dict[self.cmb_skeleton_type.currentText()])
            lucid.unreal.file_io.import_skeletal_mesh(self.asset_file_path,
                                                      destination_package_path,
                                                      skeleton,
                                                      asset_name,
                                                      loc,
                                                      rot,
                                                      self.sbx_uniform_scale.value())
        else:
            unreal.log(f'import to: {destination_package_path}')
            asset_name = destination_package_path.split('/')[-1]
            lucid.unreal.lod.import_sk_lod(f'{destination_package_path}/{asset_name}', lod_index, self.asset_file_path.as_posix())

    def import_asset(self) -> None:
        """All procedures and functions that take place when importing an asset."""
        self.set_pipe_environment_vars()
        if not self.asset_file_path.exists():
            return

        category_token = lucid.schema.get_tool_schema_value('unreal_asset_browser',
                                                            'category_related_token')
        set_token = lucid.schema.get_tool_schema_value('unreal_asset_browser',
                                                            'set_related_token')
        category_value = self.get_selected_by_column_label(category_token)
        set_value = self.get_selected_by_column_label(set_token)

        # TODO: Make this dynamically build from /Game/ downwards
        destination_package_path = f'/Game/02_Assets/{category_value}/{set_value}/{self.asset_name}'
        loc = unreal.Vector(self.sbx_loc_x.value(), self.sbx_loc_y.value(), self.sbx_loc_z.value())
        rot = unreal.Rotator(self.sbx_rot_x.value(), self.sbx_rot_y.value(), self.sbx_rot_z.value())

        if self.columns[1].selected_item == 'env':
            self.import_env(destination_package_path, self.asset_name, loc, rot)
        else:
            self.import_skel(destination_package_path, self.asset_name, loc, rot)

        unreal.EditorAssetLibrary.save_directory(destination_package_path)

        if self.cbx_convert_materials.isChecked():
            pass  # TODO: hook up material conversion for imported fbx files.


def main() -> None:
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

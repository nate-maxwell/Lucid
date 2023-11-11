"""
# Unreal Anim Browser

* Description

    The primary anim browser UI for unreal in Lucid.

* Update History

    `2023-10-06` - Init
"""


import sys
from pathlib import Path

from PySide2 import QtWidgets
import unreal

import lucid.constants
import lucid.ui.components
import lucid.io_utils
import lucid.legex
import lucid.unreal.file_io
import lucid.unreal.paths
import lucid.unreal.lod


global window_singleton


class UnrealAssetBrowser(lucid.ui.components.LucidFileBrowser):
    def __init__(self):
        columns = ['Project', 'Category', 'Set', 'Animation', 'Direction']
        super().__init__(columns, lucid.constants.PROJECTS_PATH, (1024, 850), (1280, 850))

        global window_singleton
        window_singleton = self

        qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
        with open(qss_path, 'r') as f:
            stylesheet = f.read()
            self.setStyleSheet(stylesheet)

        self.setWindowTitle('Lucid Anim Browser')
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

        self.grp_fps = QtWidgets.QGroupBox('FPS')
        self.hlayout_fps = QtWidgets.QHBoxLayout()
        self.sbx_fps = QtWidgets.QSpinBox()
        self.sbx_fps.setValue(30)

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
        self.cbx_del_morph_targets = QtWidgets.QCheckBox('Delete Morph Targets')

    def create_layout(self) -> None:
        self.grp_skeleton_type.setLayout(self.hlayout_skeleton_type)
        self.hlayout_skeleton_type.addWidget(self.cmb_skeleton_type)

        self.grp_fps.setLayout(self.hlayout_fps)
        self.hlayout_fps.addWidget(self.sbx_fps)

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
        self.vlayout_misc.addWidget(self.cbx_del_morph_targets)

        self.vlayout_import_options.addWidget(QtWidgets.QLabel(''))
        self.vlayout_import_options.addWidget(self.btn_asset_import)
        self.vlayout_import_options.addWidget(self.btn_asset_refresh)
        self.vlayout_import_options.addWidget(self.grp_skeleton_type)
        self.vlayout_import_options.addWidget(self.grp_fps)
        self.vlayout_import_options.addWidget(self.grp_uniform_scale)
        self.vlayout_import_options.addWidget(self.grp_location_offset)
        self.vlayout_import_options.addWidget(self.grp_rotation_offset)
        self.vlayout_import_options.addWidget(self.grp_misc)

        self.vlayout_import_options.addStretch()
        self.layout_main.addLayout(self.hlayout_columns)
        self.layout_main.addLayout(self.vlayout_import_options)

    def create_connections(self) -> None:
        self.btn_asset_refresh.clicked.connect(self.btn_refresh_connection)
        self.btn_asset_import.clicked.connect(self.import_animation)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def base_path(self) -> Path:
        return Path(lucid.constants.PROJECTS_PATH, self.columns[0].selected_item, 'Anim')

    @property
    def path_to_file_dir(self) -> Path:
        path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                    self.columns[3].selected_item, 'Unreal', self.columns[4].selected_item, 'fbx')
        return path

    def column_action(self, index: int) -> None:
        if index == 0:
            path = self.base_path
        elif index == 1:
            path = Path(self.base_path, self.columns[1].selected_item)
        elif index == 2:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item)
        elif index == 3:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                               self.columns[3].selected_item, 'Unreal')
        elif index == 4:
            path = Path(self.base_path, self.columns[1].selected_item, self.columns[2].selected_item,
                               self.columns[3].selected_item, 'Unreal', self.columns[4].selected_item, 'fbx')
            self.asset_files_directory = path
            return
        else:
            path = self.base_path

        if path.exists():
            items = lucid.io_utils.list_folder_contents(path)
            if not index + 1 == len(self.columns):
                self.columns[index + 1].populate_column(items)
                self.clear_columns_right_of(index + 1)

    def btn_refresh_connection(self) -> None:
        self.clear_columns_right_of(0)
        self.columns[0].deselect_item()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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
        The full file path to the source asset from the selected UI values,
        to be imported into the engine.

        Returns:
            Path: Returns the path of valid, else returns Path('/does/not/exist').
        """
        if self.all_columns_check():
            asset_name = f'{self.columns[2].selected_item}_{self.columns[3].selected_item}_{self.columns[4].selected_item}.fbx'
            path = Path(self.path_to_file_dir, asset_name)
            return path
        else:
            return Path('/does/not/exist')

    def import_animation(self) -> None:
        """All procedures and functions that take place when importing an animation."""
        if not self.asset_file_path.exists():
            return

        asset_name = f'{self.columns[2].selected_item}_{self.columns[3].selected_item}_{self.columns[4].selected_item}'
        dest_pkg_path = f'/Game/05_Anim/{self.columns[1].selected_item}/{self.columns[2].selected_item}/{asset_name}'
        skeleton = unreal.load_asset(self.skeletons_dict[self.cmb_skeleton_type.currentText()])
        loc = unreal.Vector(self.sbx_loc_x.value(), self.sbx_loc_y.value(), self.sbx_loc_z.value())
        rot = unreal.Rotator(self.sbx_rot_x.value(), self.sbx_rot_y.value(), self.sbx_rot_z.value())

        lucid.unreal.file_io.import_animation(self.asset_file_path.as_posix(), dest_pkg_path, skeleton,
                                              self.sbx_fps.value(), loc, rot, self.sbx_uniform_scale.value(),
                                              True, self.cbx_del_morph_targets.isChecked())


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

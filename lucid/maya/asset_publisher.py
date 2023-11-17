"""
# Maya Asset Publisher

* Description

    The primary asset publisher from maya to the rest of the lucid ecosystem.

* Update History

    `2023-09-22` - Init

    `2023-09-23` - Added basic metadata support + bug fixes.

    `2023-09-27` - Added skeleton unparenting so there are no extra nodes when exporting
    to unreal or other DCCs that interpret extra nodes as bones. Thumbnail generation
    was also done between the last update and now, but mistakenly not documented in the
    update history of the header.

    `2023-11-10` - Now uses dynamic paths, checking lucid.config.tools_directory.json.
    A check for project specific directory structures will probably be added at some
    point in the future.

    `2023-11-11` - Now sets environment vars, currently only role and project.

    `2023-11-16` - Fixed bug with initial publishes appending '_v001' to the end,
    regardless of whether it was using an already valid version suffix.
    File versioning is now gotten from project configs, using ENV_PROJECT environment
    var.
"""


import os
from pathlib import Path
from typing import Union

from PySide2 import QtWidgets
from maya import cmds

import lucid.constants
import lucid.io_utils
import lucid.proj_manager
import lucid.ui.components
import lucid.ui.qt
import lucid.maya
import lucid.maya.io
import lucid.maya.confirm_window
import lucid.maya.common_actions
import lucid.legex
import lucid.schema


global window_singleton


class MayaAssetPublisher(QtWidgets.QMainWindow):
    """
    The primary asset publisher for Maya in Lucid.

    Any asset exporting from Maya, for Maya, Unreal, or future DCCs is done through
    this tool. Asset metadata and thumbnails are also written out.

    Notes:
         Currently version padding is fixed by the constant at the top of the module.
         This may change in the future.
    """
    def __init__(self):
        super(MayaAssetPublisher, self).__init__(lucid.maya.get_maya_window())

        global window_singleton
        window_singleton = self

        self.setWindowTitle('Lucid Asset Publisher')
        self.setMinimumSize(420, 400)
        lucid.ui.qt.set_pipeline_qss(self)

        self.projects_path = Path(lucid.constants.PROJECTS_PATH)
        self.token_structure = lucid.schema.get_token_structure('maya_asset_publisher')

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.initialize_boxes()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    UI Construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self) -> None:
        self.layout_main = QtWidgets.QVBoxLayout()
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        # Publish Options
        self.grp_publish_context = QtWidgets.QGroupBox('Publish Context')
        self.vlayout_options = QtWidgets.QVBoxLayout()
        self.rows = []
        index = 0
        for i in lucid.schema.get_variable_tokens_keys(self.token_structure):
            if index == 0:
                # First row should be project selection
                row = lucid.ui.components.EnvironmentComboBox(self, i, [], index, False)
            else:
                row = lucid.ui.components.EnvironmentComboBox(self, i, [], index)
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

        # Pre-Process publish options
        self.grp_pre_proces = QtWidgets.QGroupBox('Pre-Processes')
        self.vlayout_publish_options = QtWidgets.QVBoxLayout()
        self.cbx_version_up_textures = QtWidgets.QCheckBox('Version Up Textures')
        self.cbx_delete_all_history = QtWidgets.QCheckBox('Delete All History')
        self.cbx_delete_non_deformer_history = QtWidgets.QCheckBox('Delete All Non-Deformer History')

        self.btn_publish_asset = QtWidgets.QPushButton('Publish Asset')

    def create_layout(self) -> None:
        self.main_widget.setLayout(self.layout_main)

        self.grp_publish_context.setLayout(self.vlayout_options)

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

        self.grp_pre_proces.setLayout(self.vlayout_publish_options)
        self.vlayout_publish_options.addWidget(self.cbx_version_up_textures)
        self.vlayout_publish_options.addWidget(self.cbx_delete_all_history)
        self.vlayout_publish_options.addWidget(self.cbx_delete_non_deformer_history)

        self.layout_main.addWidget(self.grp_publish_context)
        self.layout_main.addLayout(self.hlayout_types)
        self.layout_main.addWidget(self.grp_notes)
        self.layout_main.addWidget(self.grp_pre_proces)
        self.layout_main.addWidget(self.btn_publish_asset)
        self.layout_main.addStretch()

    def create_connections(self) -> None:
        self.rdo_unreal.clicked.connect(self.rdo_unreal_connection)
        self.rdo_maya.clicked.connect(self.rdo_maya_connection)
        self.btn_publish_asset.clicked.connect(self.publish_asset)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def initialize_boxes(self) -> None:
        """Sets the startup values of each row's combobox."""
        for row in self.rows:
            if row.index + 1 < len(self.rows):
                self.populate_box_at_index(row.index + 1)

    def populate_box_at_index(self, index: int) -> None:
        """
        Fills the combobox of the row's index based on previous row's selections.
        Will autopopulate the following boxes with first possible path.

        If the path formed does not exist, then all remaining boxes will be cleared.

        Args:
            index(int): The box to populate.
        """
        path = self.path_to_index(index)
        if path.exists():
            self.rows[index].set_box_contents(lucid.io_utils.list_folder_contents(path))
            if index < len(self.rows) - 1:
                self.clear_rows_from_index(index + 1)
                self.populate_box_at_index(index + 1)
        else:
            self.clear_rows_from_index(index + 1)

    def clear_rows_from_index(self, index: int) -> None:
        """Empties each row's combo box at and after the given index."""
        for row in self.rows:
            if row.index >= index:
                row.set_box_contents([])

    def rdo_unreal_connection(self) -> None:
        self.rdo_ascii.setChecked(False)
        self.rdo_fbx.setChecked(True)

    def rdo_maya_connection(self) -> None:
        self.rdo_ascii.setChecked(True)
        self.rdo_fbx.setChecked(False)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def padding_num(self) -> int:
        return lucid.proj_manager.get_value_from_config('General.json', 'version_padding')

    @property
    def asset_path(self) -> Path:
        """
        The path of the current asset, before file type.

        Returns:
            Path: The publish path for the asset.
        """
        return self.path_to_index(len(self.rows))

    @property
    def base_file_path(self) -> Path:
        """
        The full file path to the current asset.

        Returns:
            Path: The full file path.
        """
        if self.rdo_fbx.isChecked():
            ext = 'fbx'
        elif self.rdo_ascii.isChecked():
            ext = 'ma'
        else:
            ext = 'fbx'

        if self.rdo_maya.isChecked():
            dcc = 'Maya'
        elif self.rdo_unreal.isChecked():
            dcc = 'Unreal'
        else:
            dcc = 'Maya'

        name_token = lucid.schema.get_tool_schema_value('maya_asset_publisher',
                                                        'anim_name_related_token')
        subcontext_token = lucid.schema.get_tool_schema_value('maya_asset_publisher',
                                                              'subcontext_related_token')
        name_value = self.get_row_value_by_name(name_token)
        subcontext_value = self.get_row_value_by_name(subcontext_token)
        asset_name = f'{name_value}_{subcontext_value}.{ext}'
        path = Path(self.asset_path, dcc, ext, asset_name)
        return path

    def path_to_index(self, index: int) -> Path:
        """
        Collects row values to create a token list and return a path up to the specified
        row's index. This is procedurally done with lucid.schema.create_path_from_tokens.

        Args:
            index(int): The row number to create the path up to.

        Returns:
            Path: The generated path, up to the given index.
        """
        tokens = []
        for row in self.rows:
            if row.index < index:
                tokens.append(row.selected_item)
        return lucid.schema.create_path_from_tokens(tokens, 'maya_asset_publisher')

    def get_row_by_name(self, row_name: str) -> Union[lucid.ui.components.EnvironmentComboBox, None]:
        """
        Gets the current environment row widget of the given name.

        Args:
            row_name(str): The row name to match against when retrieving the row

        Returns:
            Union[lucid.ui.components.EnvironmentComboBox, None]: The row widget
            or None, if one with the given row name couldn't be found.
        """
        for row in self.rows:
            if row.row_name == row_name:
                return row
        else:
            return None

    def get_row_value_by_name(self, row_name: str) -> Union[str, None]:
        """
        Gets the current value of the combobox of the corresponding row name.

        Args:
            row_name(str): The row name to match against when retrieving the
            combobox value.

        Returns:
            Union[str, None]: The selected item from the combobox, or None if row
            does not exist.
        """
        row = self.get_row_by_name(row_name)
        return row.selected_item

    def create_meta_dict(self) -> None:
        """
        Creates a dict of the metadata values for the asset publish and saves it to a json.
        The json file is the same as self.base_file_path but with a .json extension.
        """
        meta = {}
        ext = self.base_file_path.suffix
        version = lucid.io_utils.get_next_version_from_dir(self.base_file_path.parent, ext,
                                                           padding=self.padding_num)

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

    def set_pipe_environment_vars(self) -> None:
        """Sets the relevant maya environment vars for the pipeline."""
        project_token = lucid.schema.get_tool_schema_value('maya_asset_publisher',
                                                           'project_related_token')
        project = self.get_row_value_by_name(project_token)
        os.environ[lucid.constants.ENV_PROJECT] = project
        os.environ[lucid.constants.ENV_ROLE] = 'ASSET'

    def generate_thumbnail(self) -> Path:
        """
        Generates the asset thumbnail for the asset browser. Uses current viewport camera.
        Thumbnail is named after asset without version number. Asset is deselected during
        thumbnail capturing and reselected after.

        Returns:
            Path: the path to the generated thumbnail.
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

    def publish_initial_textures(self) -> None:
        """
        Loops through the fileTextureName file nodes and copies their contents
        to the textures path, if it is empty.
        """
        pub_texture_path = Path(self.base_file_path.parent, 'textures')
        if lucid.io_utils.list_folder_contents(pub_texture_path, True):
            return

        for node in cmds.ls(type='file'):
            source_path = Path(cmds.getAttr(node + '.fileTextureName'))

            initial_pub_name = lucid.legex.version_up_filename(source_path.name, self.padding_num)
            initial_pub_path = Path(pub_texture_path, initial_pub_name)

            if not initial_pub_path.exists():
                lucid.io_utils.copy_file(source_path, pub_texture_path)
                os.rename(Path(pub_texture_path, source_path.name), initial_pub_path)

            cmds.setAttr((node + '.fileTextureName'), initial_pub_path, type='string')

    def publish_new_texture_versions(self) -> None:
        """
        Loops through the fileTextureName file nodes and copies their contents
        to the textures path, if it is filled, versioning up the version suffix.
        Will run self.publish_initial_textures() if the texture pub path is
        empty or missing.
        """
        pub_texture_path = Path(self.base_file_path.parent, 'textures')

        if not pub_texture_path.exists():
            self.publish_initial_textures()
            return
        if not lucid.io_utils.list_folder_contents(pub_texture_path, True):
            self.publish_initial_textures()
            return

        for node in cmds.ls(type='file'):
            source_path = Path(cmds.getAttr(node + '.fileTextureName'))

            new_pub_name = lucid.legex.version_up_filename(source_path.name, self.padding_num)
            new_pub_path = Path(pub_texture_path, new_pub_name)

            lucid.io_utils.copy_file(source_path, pub_texture_path, new_pub_name)

            cmds.setAttr((node + '.fileTextureName'), new_pub_path, type='string')

    def source_publish_pre_process(self) -> None:
        """
        Preprocess checklist before any file writing happens
        These should happen in order they are displayed on the UI.

        Currently, these preprocesses are only intended for maya ascii
        publishes. A maya ascii publish should always take place before
        a publish for another DCC or another file type, but is not
        enforced.
        """
        if self.cbx_version_up_textures.isChecked():
            self.publish_new_texture_versions()
        else:
            self.publish_initial_textures()

        if self.cbx_delete_all_history.isChecked():
            cmds.delete(all=True, ch=True)

        if self.cbx_delete_non_deformer_history.isChecked():
            lucid.maya.common_actions.delete_all_non_deformer_history()

    def publish_asset(self) -> None:
        """
        The primary asset publishing switch.
        Should more DCCs or file types need to be added, here is where they should go.
        """
        self.set_pipe_environment_vars()

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

    @lucid.maya.retain_selection
    def publish_maya_ascii(self) -> None:
        self.source_publish_pre_process()
        options = lucid.maya.io.MayaAsciiExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_ma(options)
        self.create_meta_dict()

    @lucid.maya.retain_selection
    def publish_maya_fbx(self) -> None:
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_fbx(options)
        self.create_meta_dict()

    @lucid.maya.retain_selection
    def publish_unreal_fbx(self) -> None:
        """
        Publishes an unreal fbx asset to <projects path> in the Unreal/fbx folder based
        on the input values from the UI. This will unparent geoGrp and skeletonGrp from
        the category node, export the two of them, then reparent them to the category
        node.
        """
        category_token = lucid.schema.get_tool_schema_value('maya_asset_publisher',
                                                            'category_related_token')
        category = self.get_row_value_by_name(category_token)
        # Rigged asset check
        if cmds.objExists('skeletonGrp') and cmds.objExists('geoGrp'):
            cmds.select('skeletonGrp', 'geoGrp')
            selected = cmds.ls(selection=True)
            cmds.parent(selected, world=True)
            cmds.delete(category)
        else:
            selected = cmds.select(category)

        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        # export_selected doesn't seem to be working so for now we delete the category null
        # and group the skeletonGrp and geoGrp back to one afterward.
        options.export_selected = True

        lucid.maya.io.export_fbx(options)
        self.create_meta_dict()

        # Rigged asset check
        if cmds.objExists('skeletonGrp') and cmds.objExists('geoGrp'):
            cmds.group(selected, n=category)

    def create_version_file(self) -> None:
        """Copies the published file and renames it based on its version number."""
        file_name = self.base_file_path.name
        ext = self.base_file_path.suffix
        base_name = file_name.split(ext)[0]
        version = lucid.io_utils.get_next_version_from_dir(self.base_file_path.parent, ext,
                                                           padding=self.padding_num)
        version_base_name = f'{base_name}_v{version}'
        version_file_name = f'{version_base_name}{ext}'
        lucid.io_utils.copy_file(self.base_file_path, self.base_file_path.parent,  # Base file
                                 version_file_name)
        lucid.io_utils.copy_file(self.base_file_path.with_suffix('.json'),  # Json file
                                 self.base_file_path.parent, version_base_name)
        lucid.io_utils.copy_file(self.base_file_path.with_suffix('.jpg'),
                                 self.base_file_path.parent, f'{version_base_name}')  # thumbnail file


def main() -> None:
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

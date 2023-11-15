"""
# Animation Publisher

* Description

    The primary animation publisher for Maya.

* Update History

    `2023-10-01` - Init

    `2023-11-11` - Now dynamically reads directory structure.
"""


import os
from pathlib import Path
from typing import Union

from PySide2 import QtWidgets
from maya import cmds

import lucid.schema
import lucid.io_utils
import lucid.constants
import lucid.ui.components
import lucid.ui.qt
import lucid.maya
import lucid.maya.io
import lucid.maya.confirm_window


global window_singleton  # Global for singleton.


class MayaAnimPublisher(QtWidgets.QMainWindow):
    def __init__(self):
        super(MayaAnimPublisher, self).__init__(lucid.maya.get_maya_window())

        global window_singleton
        window_singleton = self

        self.setWindowTitle('Lucid Anim Publisher')
        self.setMinimumSize(320, 400)
        lucid.ui.qt.set_pipeline_qss(self)

        self.projects_path = Path(lucid.constants.PROJECTS_PATH)
        self.token_structure = lucid.schema.get_token_structure('maya_anim_publisher')

        self.projects_path = lucid.constants.PROJECTS_PATH

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.initialize_boxes()

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Widget construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self) -> None:
        self.main_widget = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)

        # Publish Context
        self.grp_publish_context = QtWidgets.QGroupBox('Publish Context')
        self.vlayout_options = QtWidgets.QVBoxLayout()
        self.rows = []
        index = 0
        for i in lucid.schema.get_variable_tokens_keys(self.token_structure):
            # First row should be project selection
            if index == 0:
                row = lucid.ui.components.EnvironmentComboBox(self, i, [], index, False)
            else:
                row = lucid.ui.components.EnvironmentComboBox(self, i, [], index)
            self.rows.append(row)
            self.vlayout_options.addLayout(row)
            index += 1
        self.rows[0].set_box_contents(lucid.io_utils.list_folder_contents(self.projects_path))

        # Direction Context Box
        directions = ['Forward', 'Fwd Left', 'Fwd Right', 'Left', 'Right', 'Backward',
                      'Bwd Left', 'Bwd Right', 'vertical', 'In-Place', 'interaction']
        direction_row_name = lucid.schema.get_tool_schema_value('maya_anim_publisher',
                                                                   'direction_related_token')
        self.cmb_direction = self.get_row_by_name(direction_row_name)
        self.cmb_direction.set_box_contents(directions)

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

        self.btn_publish_animation = QtWidgets.QPushButton('Publish Animation')

    def create_layout(self) -> None:
        # Context
        self.grp_publish_context.setLayout(self.vlayout_options)

        # DCC Types
        self.hlayout_types.addWidget(self.grp_dcc_type)
        self.grp_dcc_type.setLayout(self.vlayout_dcc_type)
        self.vlayout_dcc_type.addWidget(self.rdo_maya)
        self.vlayout_dcc_type.addWidget(self.rdo_unreal)

        # File Types
        self.hlayout_types.addWidget(self.grp_file_type)
        self.grp_file_type.setLayout(self.vlayout_file_type)
        self.vlayout_file_type.addWidget(self.rdo_ascii)
        self.vlayout_file_type.addWidget(self.rdo_fbx)

        # Notes
        self.grp_notes.setLayout(self.hlayout_notes)
        self.hlayout_notes.addWidget(self.le_notes)

        # Main Layout Assembly
        self.layout_main.addWidget(self.grp_publish_context)
        self.layout_main.addWidget(self.grp_publish_context)
        self.layout_main.addLayout(self.hlayout_types)
        self.layout_main.addWidget(self.grp_notes)
        self.layout_main.addWidget(self.btn_publish_animation)
        self.layout_main.addStretch()

    def create_connections(self) -> None:
        self.rdo_unreal.clicked.connect(self.rdo_unreal_connection)
        self.rdo_maya.clicked.connect(self.rdo_maya_connection)
        self.btn_publish_animation.clicked.connect(self.btn_publish_animation_connection)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def initialize_boxes(self) -> None:
        """Sets the startup values of each row's combobox."""
        for row in self.rows:
            if row.index + 1 < (len(self.rows) - 1):
                self.populate_box_at_index(row.index + 1)

    def populate_box_at_index(self, index: int) -> None:
        """
        Fills the combobox of the row's index based on previous row's selections.
        Will autopopulate the following boxes with first possible path.

        If the path formed does not exist, then all remaining boxes will be cleared.

        Args:
            index(int): Which box to populate.
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
        """
        Empties each row's combo box at and after the given index.

        Args:
            index(int): Which row to start clearing.
        """
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

        set_token = lucid.schema.get_tool_schema_value('maya_anim_publisher',
                                                       'set_related_token')
        name_token = lucid.schema.get_tool_schema_value('maya_anim_publisher',
                                                        'anim_name_related_token')
        direction_token = lucid.schema.get_tool_schema_value('maya_anim_publisher',
                                                             'direction_related_token')
        set_value = self.get_row_value_by_name(set_token)
        name_value = self.get_row_value_by_name(name_token)
        direction_value = self.get_row_value_by_name(direction_token)
        anim_name = f'{set_value}_{name_value}_{direction_value}.{ext}'
        path = Path(self.path_to_index(len(self.rows)), dcc, ext, anim_name)
        return path

    @lucid.maya.retain_selection
    def bake_skeleton(self) -> None:
        """Bakes all joint nodes in the scene."""
        joints = cmds.ls(type='joint')
        cmds.select(joints)
        start = cmds.playbackOptions(q=True, min=True)
        end = cmds.playbackOptions(q=True, max=True)
        cmds.bakeSimulation(time=(start, end), hierarchy='both')

    def path_to_index(self, index: int) -> Path:
        tokens = []
        for r in self.rows:
            if r.index < index:
                tokens.append(r.selected_item)

        return lucid.schema.create_path_from_tokens(tokens, 'maya_anim_publisher')

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

    def create_meta_dict(self) -> None:
        """
        Creates a dict of the metadata values for the asset publish and saves it to a json.
        The json file is the same as self.base_file_path but with a .json extension.
        """
        meta = {}
        ext = self.base_file_path.suffix
        version = lucid.io_utils.get_next_version_from_dir(self.base_file_path.parent, ext)

        for row in self.rows:
            meta[row.row_name] = row.selected_item
        meta['Type'] = 'Anim'
        meta['Time'] = lucid.io_utils.get_time()
        meta['Date'] = lucid.io_utils.get_date()
        meta['Version'] = version
        meta['User'] = lucid.constants.USER
        meta['Notes'] = self.le_notes.text()
        meta['Direction'] = self.cmb_direction.selected_item

        json_file = self.base_file_path.with_suffix('.json')
        lucid.io_utils.export_data_to_json(json_file, meta, True)

    def set_pipe_environment_vars(self) -> None:
        """Sets the relevant maya environment vars for the pipeline."""
        project_token = lucid.schema.get_tool_schema_value('maya_anim_publisher',
                                                           'project_related_token')
        project = self.get_row_value_by_name(project_token)
        os.environ[lucid.constants.ENV_PROJECT] = project
        os.environ[lucid.constants.ENV_ROLE] = 'ANIM'

    def btn_publish_animation_connection(self) -> None:
        """
        The primary anim publishing switch.
        Should more DCCs or file types need to be added, here is where they should go.
        """
        self.set_pipe_environment_vars()

        if cmds.objExists(self.rows[1].selected_item):
            print(f'PUBLISHING Anim to {self.base_file_path.parent}')
            lucid.io_utils.create_folder(self.base_file_path.parent)

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
        options = lucid.maya.io.MayaAsciiExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_ma(options)
        self.create_meta_dict()

    @lucid.maya.retain_selection
    def publish_maya_fbx(self) -> None:
        """
        Unlike publish_unreal_fbx, this will not unparent skeletonGrp and geoGrp
        when publishing, nor will any bake occur.
        """
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_fbx(options)
        self.create_meta_dict()

    @lucid.maya.retain_selection
    def publish_unreal_fbx(self) -> None:
        """
        Bakes the joint nodes and then exports the geoGrp and skeletonGrp.
        They will be re-parented under the category node afterward, with baked keys.
        """
        # Category null check
        category_token = lucid.schema.get_tool_schema_value('maya_anim_publisher',
                                                            'category_related_token')
        category = self.get_row_value_by_name(category_token)
        if not cmds.objExists(category):
            line1 = f'No null named "{self.rows[1].selected_item}" found.'
            line2 = 'Assets must be children of a category null!'
            warning = f'{line1}\n{line2}'
            lucid.maya.confirm_window.info(warning)
            return

        # Rigged asset check
        if cmds.objExists('skeletonGrp') and cmds.objExists('geoGrp'):
            cmds.select('skeletonGrp', 'geoGrp')
            selected = cmds.ls(selection=True)
            cmds.parent(selected, world=True)
        else:
            line1 = 'Unreal FBX anim pubbing only for non-env assets'
            line2 = 'that contain both skeletonGrp and geoGrp nodes.'
            warning = f'{line1}\n{line2}'
            lucid.maya.confirm_window.info(warning)
            return

        self.bake_skeleton()
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        options.export_selected = True
        lucid.maya.io.export_fbx(options)
        self.create_meta_dict()

        # group re-parent
        if cmds.objExists('skeletonGrp') and cmds.objExists('geoGrp'):
            cmds.parent(selected, category)

    def create_version_file(self) -> None:
        """Copies the published file and renames it based on its version number."""
        file_name = self.base_file_path.name
        ext = self.base_file_path.suffix
        base_name = file_name.split(ext)[0]
        version = lucid.io_utils.get_next_version_from_dir(self.base_file_path.parent, ext)
        version_base_name = f'{base_name}_v{version}'
        version_file_name = f'{version_base_name}{ext}'
        lucid.io_utils.copy_file(self.base_file_path, self.base_file_path.parent,
                                 version_file_name)  # Base file
        lucid.io_utils.copy_file(self.base_file_path.with_suffix('.json'),
                                 self.base_file_path.parent, version_base_name)  # Json file


def main() -> None:
    """Close and crate UI in singleton fashion."""
    global window_singleton
    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except NameError:
        pass

    window_singleton = MayaAnimPublisher()
    window_singleton.show()


if __name__ == '__main__':
    main()

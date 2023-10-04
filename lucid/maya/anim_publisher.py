"""
# Animation Publisher

* Description

    The primary animation publisher for Maya.

* Update History

    `2023-10-01` - Init
"""


from pathlib import Path

from PySide2 import QtWidgets
from maya import cmds

import lucid.io_utils
import lucid.constants
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
    Widget construction
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)

        # Publish Context
        self.grp_publish_context = QtWidgets.QGroupBox('Publish Context')
        self.vlayout_options = QtWidgets.QVBoxLayout()
        self.rows = []
        index = 0
        for i in ['Project', 'Category', 'Set', 'Name']:
            row = EnvironmentComboBox(self, i, [], index)
            self.rows.append(row)
            self.vlayout_options.addLayout(row)
            index += 1
        self.rows[0].set_box_contents(lucid.io_utils.list_folder_contents(self.projects_path))

        # Direction Context Box
        directions = ['Forward', 'Fwd Left', 'Fwd Right', 'Left', 'Right', 'Backward',
                      'Bwd Left', 'Bwd Right', 'vertical', 'In-Place', 'interaction']
        self.cmb_direction = EnvironmentComboBox(self, 'Direction', directions, len(self.rows))
        self.vlayout_options.addLayout(self.cmb_direction)

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

    def create_layout(self):
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

    def create_connections(self):
        self.rdo_unreal.clicked.connect(self.rdo_unreal_connection)
        self.rdo_maya.clicked.connect(self.rdo_maya_connection)
        # self.btn_publish_animation.clicked.connect(self.btn_publish_animation_connection)
        self.btn_publish_animation.clicked.connect(self.btn_publish_animation_connection)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Front end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def initialize_boxes(self):
        """Sets the startup values of each row's combobox."""
        for row in self.rows:
            if row.index + 1 < (len(self.rows) - 1):
                self.populate_box_at_index(row.index + 1)

    def populate_box_at_index(self, index: int):
        """
        Fills the combobox of the row's index based on previous row's selections.
        Will autopopulate the following boxes with first possible path.

        If the path formed does not exist, then all remaining boxes will be cleared.

        Args:
            index(int): Which box to populate.
        """
        path = Path(self.projects_path, self.rows[0].selected_item, 'Anim')
        for row in self.rows:
            if 0 < row.index < index:
                path = Path(path, row.selected_item)
            elif row.index == index:
                row.set_box_contents(lucid.io_utils.list_folder_contents(path))
                if not path.exists():
                    self.clear_rows_from_index(index + 1)
                self.populate_box_at_index(index + 1)

    def clear_rows_from_index(self, index: int):
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
    def anim_path(self) -> Path:
        """
        The path of the current anim, before file type.

        Returns:
            Path: The publish path for the anim.
        """
        path = Path(self.projects_path, self.rows[0].selected_item, 'Anim')
        for row in self.rows:
            if row.index > 0:
                if row.index == 3:
                    if self.rdo_maya.isChecked():
                        path = Path(path, row.selected_item, 'Maya')
                    elif self.rdo_unreal.isChecked():
                        path = Path(path, row.selected_item, 'Unreal')
                else:
                    path = Path(path, row.selected_item)

        return path

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

        anim_name = f'{self.rows[2].selected_item}_{self.rows[3].selected_item}_{self.cmb_direction.selected_item}.{ext}'
        path = Path(self.anim_path, self.cmb_direction.selected_item, ext, anim_name)
        return path

    @lucid.maya.retain_selection
    def bake_skeleton(self):
        """Bakes all joint nodes in the scene."""
        joints = cmds.ls(type='joint')
        cmds.select(joints)
        start = cmds.playbackOptions(q=True, min=True)
        end = cmds.playbackOptions(q=True, max=True)
        cmds.bakeSimulation(time=(start, end), hierarchy='both')

    def get_environ_value_by_name(self, row_name: str):
        """
        Gets the current value of the combobox of the corresponding row name.

        Args:
            row_name(str): The row name to match against when retrieving the
            combobox value.

        Returns:
            str: the selected item from the combobox.
        """
        for i in self.rows:
            if i.row_name == row_name:
                return i.selected_item

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
        meta['Type'] = 'Anim'
        meta['Time'] = lucid.io_utils.get_time()
        meta['Date'] = lucid.io_utils.get_date()
        meta['Version'] = version
        meta['User'] = lucid.constants.USER
        meta['Notes'] = self.le_notes.text()
        meta['Direction'] = self.cmb_direction.selected_item

        json_file = self.base_file_path.with_suffix('.json')
        lucid.io_utils.export_data_to_json(json_file, meta, True)

    def btn_publish_animation_connection(self):
        """
        The primary anim publishing switch.
        Should more DCCs or file types need to be added, here is where they should go.
        """
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
    def publish_maya_ascii(self):
        options = lucid.maya.io.MayaAsciiExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_ma(options)
        self.create_meta_dict()

    @lucid.maya.retain_selection
    def publish_maya_fbx(self):
        """
        Unlike publish_unreal_fbx, this will not unparent skeletonGrp and geoGrp
        when publishing, nor will any bake occur.
        """
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_fbx(options)
        self.create_meta_dict()

    @lucid.maya.retain_selection
    def publish_unreal_fbx(self):
        """
        Bakes the joint nodes and then exports the geoGrp and skeletonGrp.
        They will be re-parented under the category node afterward, with baked keys.
        """
        # Category null check
        category = self.get_environ_value_by_name('Category')
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

    def create_version_file(self):
        """Copies the published file and renames it based on its version number."""
        file_name = self.base_file_path.name
        ext = self.base_file_path.suffix
        base_name = file_name.split(ext)[0]
        version = lucid.io_utils.get_next_version_from_dir(self.base_file_path.parent, ext)
        version_base_name = f'{base_name}_v{version}'
        version_file_name = f'{version_base_name}{ext}'
        lucid.io_utils.copy_file(self.base_file_path, self.base_file_path.parent, version_file_name)  # Base file
        lucid.io_utils.copy_file(self.base_file_path.with_suffix('.json'), self.base_file_path.parent,  # Json file
                                 version_base_name)


class EnvironmentComboBox(QtWidgets.QHBoxLayout):
    """
    The primary widget for creating asset context rows in the
    lucid.maya.anim_publisher.MayaAnimPublisher.

    Args:
        parent_ui(MayaAnimPublisher): The managing maya asset publisher parent
        class. This is to communicate back to the parent if necessary.

        label(str): The name of the generated row.

        contents(list[str]): The initial list of items to add to the combobox.

        index(int): A unique id number in-case normal filtering is not doable.

    Properties:
        selected_item(str): The current text of the combobox.
    """
    def __init__(self, parent_ui: MayaAnimPublisher,
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
            self.cmb_combobox.addItems([selection])
            self.cmb_combobox.setCurrentText(selection)

        self.parent_ui.populate_box_at_index(self.index + 1)

    @property
    def selected_item(self) -> str:
        """
        Shortened namespace way to get combo box value.

        Returns:
            str: The current text of the combobox.
        """
        return self.cmb_combobox.currentText()

    def set_box_contents(self, contents: list[str]):
        """
        Sets the items of the combobox to the given list.

        Args:
            contents(list[str]): The items to add to the combobox.
        """
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

    window_singleton = MayaAnimPublisher()
    window_singleton.show()


if __name__ == '__main__':
    main()

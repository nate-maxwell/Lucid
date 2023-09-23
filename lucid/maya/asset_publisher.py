"""
# Maya Asset Publisher

* Description

    The primary asset publisher from maya to the rest of the lucid ecosystem.

* Update History

    `2023-09-22` - Init
"""


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
                    path = Path(path, row.selected_item, 'Model')
                else:
                    path = Path(path, row.selected_item)

            elif row.index == index:
                row.set_box_contents(lucid.io_utils.list_folder_contents(path))
                if not path.exists():
                    self.clear_rows_from_index(index + 1)
                self.populate_box_at_index(index + 1)

    def clear_rows_from_index(self, index: int):
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
        if self.rdo_fbx.isChecked():
            ext = 'fbx'
        elif self.rdo_ascii.isChecked():
            ext = 'ma'
        else:
            ext = 'fbx'

        asset_name = f'{self.rows[3].selected_item}_{self.rows[4].selected_item}.{ext}'
        path = Path(self.asset_path, ext, asset_name)
        return path

    def publish_asset(self):
        if cmds.objExists(self.rows[1].selected_item):
            print(f'PUBLISHING ASSET to {self.base_file_path.parent}')
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
        else:
            line1 = f'No null named "{self.rows[1].selected_item}" found.'
            line2 = 'Assets must be children of a category null!'
            warning = f'{line1}\n{line2}'
            lucid.maya.confirm_window.info(warning)

    def publish_maya_ascii(self):
        options = lucid.maya.io.MayaAsciiExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_ma(options)

    def publish_maya_fbx(self):
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_fbx(options)

    def publish_unreal_fbx(self):
        options = lucid.maya.io.FBXExportOptions()
        options.filepath = self.base_file_path
        lucid.maya.io.export_fbx(options)


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
        self.parent_ui.populate_box_at_index(self.index + 1)

    def button_add_item(self):
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
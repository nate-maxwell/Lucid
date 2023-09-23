"""
# Maya Asset Publisher

* Description

    The primary asset publisher from maya to the rest of the lucid ecosystem.

* Update History

    `2023-09-22` - Init
"""


from pathlib import Path

from PySide2 import QtWidgets

import lucid.constants
import lucid.io_utils
import lucid.maya


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
        """
        path = Path(self.projects_path, self.rows[0].selected_item, 'Asset')
        for row in self.rows:
            if row.index > 0:
                if row.index < index:
                    if row.index == 3:
                        # Fix context token to 'Model' for asset pubbing
                        path = Path(path, row.selected_item, 'Model')
                    else:
                        path = Path(path, row.selected_item)
                elif row.index == index:
                    row.set_box_contents(lucid.io_utils.list_folder_contents(path))

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Back end functions
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def asset_path(self) -> Path:
        path = Path(self.projects_path, self.rows[0].selected_item, 'Asset')
        for row in self.rows:
            if row.index > 0:
                if row.index == 3:
                    path = Path(path, row.selected_item, 'Model')
                else:
                    path = Path(path, row.selected_item)

        return path

    def publish_asset(self):
        print(f'PUBLISHING ASSET to {self.asset_path}')
        pass


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

    def update_parent(self):
        self.parent_ui.populate_box_at_index(self.index + 1)

    def button_add_item(self):
        item = QtWidgets.QInputDialog.getText(self, f'New {self.row_name}', 'Name: ')
        if item[0]:
            self.cmb_combobox.addItem(item[0])
            self.cmb_combobox.setCurrentText(item[0])

    @property
    def selected_item(self):
        """Shortened namespace way to get combo box value."""
        return self.cmb_combobox.currentText()

    def set_box_contents(self, contents: list[str]):
        self.cmb_combobox.clear()
        self.cmb_combobox.addItems(contents)


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

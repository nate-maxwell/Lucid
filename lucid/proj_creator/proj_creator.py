"""
# Lucid Project Creator

* Description:

    Project creation and configuration tools for Lucid.

* Update History:

    `2023-11-15` - Init
"""


import sys
from pathlib import Path
from typing import Union
from typing import Any

from PySide2 import QtWidgets

import lucid.constants
import lucid.io_utils
import lucid.environ
import lucid.ui.qt


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Tool Constants
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


TEMPLATE_CONFIG_PATH = Path(Path(__file__).parent, 'template_configs')
CONFIG_PATH = Path(lucid.constants.CONFIG_PATH, 'proj_settings.json')
CONFIG_SCHEMA = lucid.io_utils.import_data_from_json(CONFIG_PATH)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
General Helpers
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def get_value_from_config(config_name: str, key: str) -> Union[str, None]:
    pass


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Component Classes
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class CustomInput(QtWidgets.QWidget):
    def __init__(self, json_key: str, input_name: str):
        super().__init__()
        self.json_key = json_key
        self.name = input_name

        self.flayout_main = QtWidgets.QFormLayout()
        self.setLayout(self.flayout_main)

    @property
    def config_path(self):
        proj = lucid.environ.get_environ_var_as_list(lucid.constants.ENV_PROJECT)[0]
        return Path(lucid.constants.PROJECTS_PATH, proj, 'config')

    @property
    def value(self) -> Any:
        """
        The value to add to the main dict that will be saved in the config.
        Should return {self.json_key: some_value}
        """
        return Any

    @value.setter
    def value(self, value: Any):
        """
        Call this to set the value from a config to be displayed on the
        widget element.
        """


class EnumInput(CustomInput):
    def __init__(self, input_name: str, json_key: str, items: list[str]):
        super().__init__(json_key, input_name)
        if items:
            self.items = items
        else:
            self.items = ['']

        self.cmb_selection = QtWidgets.QComboBox()
        self.cmb_selection.addItems(self.items)

        self.flayout_main.addRow(self.name, self.cmb_selection)

    @property
    def value(self) -> dict:
        return {self.json_key: self.cmb_selection.currentText()}

    @value.setter
    def value(self, value: str):
        if type(value) == str:
            self.cmb_selection.setCurrentText(value)
        else:
            self.cmb_selection.setCurrentText('')


class IntInput(CustomInput):
    def __init__(self, input_name: str, json_key: str):
        super().__init__(json_key, input_name)
        self.spbx_int = QtWidgets.QSpinBox()
        self.spbx_int.setMaximum(10000)
        self.flayout_main.addRow(self.name, self.spbx_int)

    @property
    def value(self) -> dict:
        return {self.json_key: self.spbx_int.value()}

    @value.setter
    def value(self, value: int):
        if type(value) == int:
            self.spbx_int.setValue(value)
        else:
            self.spbx_int.setValue(0)


class FloatInput(CustomInput):
    def __init__(self, input_name: str, json_key: str):
        super().__init__(json_key, input_name)
        self.spbx_float = QtWidgets.QDoubleSpinBox()
        self.flayout_main.addRow(self.name, self.spbx_float)

    @property
    def value(self) -> dict:
        return {self.json_key: self.spbx_float.value()}

    @value.setter
    def value(self, value: float):
        if type(value) == float:
            self.spbx_float.setValue(value)
        else:
            self.spbx_float.setValue(0.0)


class StringInput(CustomInput):
    def __init__(self, input_name: str, json_key: str):
        super().__init__(json_key, input_name)
        self.json_key = json_key
        self.le_string = QtWidgets.QLineEdit()
        self.flayout_main.addRow(self.name, self.le_string)

    @property
    def value(self) -> dict:
        return {self.json_key: self.le_string.text()}

    @value.setter
    def value(self, value: str):
        if type(value) == str:
            self.le_string.setText(value)
        else:
            self.le_string.setText('')


class ListInput(CustomInput):
    def __init__(self, input_name: str, json_key: str, t: type):
        super().__init__(json_key, input_name)
        self.t = t
        self.le_list = QtWidgets.QLineEdit()
        self.flayout_main.addRow(self.name, self.le_list)

    @property
    def value(self) -> dict:
        return {self.json_key: self.convert_to_list_of_type(self.t)}

    @value.setter
    def value(self, value: list):
        self.le_list.setText(str(value).replace('[', '').replace(']', ''). replace("'", ''))

    def convert_input_to_list(self) -> list:
        text = self.le_list.text()
        text = text.replace(' ', '')
        if text.endswith(','):
            self.le_list.setText(text[:-1])
            self.convert_input_to_list()
        else:
            return text.split(',')

    def convert_to_list_of_type(self, t: type) -> list:
        converted_list = []
        for i in self.convert_input_to_list():
            if i or i == 0 and not i == '':
                converted_list.append(t(i))

        return converted_list

class ConfiguratorTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def save_settings(self):
        raise NotImplemented

    @staticmethod
    def create_input_by_type( type: str, name: str, key: str, enums: list[str] = None) -> CustomInput:
        """Factory for creating inputs."""
        types = {
            "int": IntInput(name, key),
            "float": FloatInput(name, key),
            "str": StringInput(name, key),
            "list[int]": ListInput(name, key, int),
            "list[float]": ListInput(name, key, float),
            "list[str]": ListInput(name, key, str),
            "enum": EnumInput(name, key, enums)
        }

        return types[type]

    @staticmethod
    def convert_key_to_name(key: str) -> str:
        """Converts 'example_name' to 'Example Name'."""
        spaced = key.replace('_', ' ')
        return spaced.title()


class ProjSettingsTab(ConfiguratorTab):
    """A widget for building proj config inputs from a schema."""
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.populate_inputs()

    def save_settings(self):
        config_dict = {}
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i).widget()
            if isinstance(item, CustomInput):
                config_dict.update(item.value)

        proj = lucid.environ.get_environ_var_as_list(lucid.constants.ENV_PROJECT)[0]
        output_path = Path(lucid.constants.PROJECTS_PATH, proj, 'config', f'{self.name}.json')
        lucid.io_utils.create_folder(output_path.parent)
        lucid.io_utils.export_data_to_json(output_path, config_dict, True)

    def load_settings(self):
        proj = lucid.environ.get_environ_var_as_list(lucid.constants.ENV_PROJECT)[0]
        if proj == '_template':
            proj_config_path = Path(TEMPLATE_CONFIG_PATH, f'{self.name}.json')
        else:
            proj_config_path = Path(lucid.constants.PROJECTS_PATH, proj, 'config', f'{self.name}.json')

        if proj_config_path.exists():
            self.assign_custom_input_value(lucid.io_utils.import_data_from_json(proj_config_path))
        else:
            self.assign_custom_input_value()

    def assign_custom_input_value(self, config: dict = None):
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i).widget()
            if isinstance(item, CustomInput):
                if config:
                    try:
                        item.value = config[item.json_key]
                    except KeyError:
                        pass
                else:
                    item.value = ''

    def populate_inputs(self):
        """
        Calls a factory function to create the necessary input. All inputs are listed in string form in the
        scheme config, including lists. Because Python doesn't have real Enums we use a list containing
        Enum values within the config.
        """
        for k in (config := CONFIG_SCHEMA[self.name]):
            if type(config[k]) == list:
                self.layout.addWidget(self.create_input_by_type('enum', self.convert_key_to_name(k), k, config[k]))
            else:
                self.layout.addWidget(self.create_input_by_type(config[k], self.convert_key_to_name(k), k))

        self.layout.addStretch()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Primary Class
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class ProjectCreator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Lucid Project Creator')
        self.setMinimumSize(600, 600)
        lucid.ui.qt.set_pipeline_qss(self)

        self.projs = []
        for i in lucid.io_utils.list_folder_contents(lucid.constants.PROJECTS_PATH):
            if not i.startswith('_'):
                self.projs.append(i)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.setCentralWidget(self.main_widget)

        self.cmb_proj_connection()
        self.load_default_values()

    def create_widgets(self):
        # Main layout
        self.layout_main = QtWidgets.QVBoxLayout()
        self.main_widget = QtWidgets.QWidget()

        # Parent tab manager
        self.settings_tab_manager = QtWidgets.QTabWidget()

        # proj tab
        self.tab_proj = QtWidgets.QWidget()
        self.vlayout_proj = QtWidgets.QVBoxLayout()
        self.proj_settings_tab_manager = QtWidgets.QTabWidget()
        self.defaults_settings_tab_manager = QtWidgets.QTabWidget()

        # proj selection
        self.hlayout_proj_selection = QtWidgets.QHBoxLayout()
        self.cmb_proj = QtWidgets.QComboBox()
        self.cmb_proj.addItems(self.projs)

        # Defaults tab
        self.tab_defaults = QtWidgets.QWidget()
        self.vlayout_defaults  =QtWidgets.QVBoxLayout()

        # General settings tab population for proj + Defaults
        self.settings_tab_array = []
        self.defaults_tab_array = []
        for k in list(CONFIG_SCHEMA.keys()):
            proj_tab = ProjSettingsTab(k)
            defaults_tab = ProjSettingsTab(k)

            self.settings_tab_array.append(proj_tab)
            self.proj_settings_tab_manager.addTab(proj_tab, k)

            self.defaults_tab_array.append(defaults_tab)
            self.defaults_settings_tab_manager.addTab(defaults_tab, k)

        # Actions
        self.hlayout_actions = QtWidgets.QHBoxLayout()
        self.btn_create_proj = QtWidgets.QPushButton('New Project')
        self.btn_create_proj.setFixedSize(150, 30)
        self.btn_update_proj = QtWidgets.QPushButton('Update Project')
        self.btn_update_proj.setFixedSize(150, 30)

    def create_layout(self):
        # proj selection
        self.hlayout_proj_selection.addWidget(QtWidgets.QLabel('proj'))
        self.hlayout_proj_selection.addWidget(self.cmb_proj)
        self.hlayout_proj_selection.addStretch()

        # proj Tab
        self.vlayout_proj.addLayout(self.hlayout_proj_selection)
        self.vlayout_proj.addWidget(self.proj_settings_tab_manager)
        self.tab_proj.setLayout(self.vlayout_proj)

        # Defaults tab
        self.vlayout_defaults.addWidget(self.defaults_settings_tab_manager)
        self.tab_defaults.setLayout(self.vlayout_defaults)

        # Parent tab
        self.settings_tab_manager.addTab(self.tab_proj, 'proj')
        self.settings_tab_manager.addTab(self.tab_defaults, 'Defaults')

        # Action buttons
        self.hlayout_actions.addStretch()
        self.hlayout_actions.addWidget(self.btn_create_proj)
        self.hlayout_actions.addWidget(self.btn_update_proj)

        self.layout_main.addWidget(self.settings_tab_manager)
        self.layout_main.addLayout(self.hlayout_actions)
        self.main_widget.setLayout(self.layout_main)

    def create_connections(self):
        self.btn_create_proj.clicked.connect(self.create_new_proj_connection)
        self.btn_update_proj.clicked.connect(self.save_connection)
        self.cmb_proj.currentTextChanged.connect(self.cmb_proj_connection)

    def create_new_proj_connection(self):
        text, confirm = QtWidgets.QInputDialog.getText(self, 'Are you sure?', 'Project Code')
        if confirm:
            self.cmb_proj.addItem(text)
            self.cmb_proj.setCurrentIndex(self.cmb_proj.count()-1)
            source = Path(Path(__file__).parent, 'template_configs')
            dest = Path(lucid.constants.PROJECTS_PATH, text, 'config')
            if dest.exists():
                return
            lucid.io_utils.copy_folder_contents(source, dest)

            general_config_path = Path(lucid.constants.PROJECTS_PATH, self.cmb_proj.currentText(), 'config', 'General.json')
            general_config = lucid.io_utils.import_data_from_json(general_config_path)
            general_config['proj_code'] = self.cmb_proj.currentText()
            lucid.io_utils.export_data_to_json(general_config_path, general_config, True)

            self.cmb_proj_connection()

    def save_connection(self):
        """Runs the corresponding save function to the selected tab."""
        # Specifically check the tab name when adding new tabs, formatting may change so the index isn't reliable
        if self.settings_tab_manager.tabText(self.settings_tab_manager.currentIndex()) == 'proj':
            lucid.environ.update_environ_var(lucid.constants.ENV_PROJECT, [self.cmb_proj.currentText()])
            self.update_proj()
            print('Updating existing proj! Users may need to restart applications.')

        elif self.settings_tab_manager.tabText(self.settings_tab_manager.currentIndex()) == 'Defaults':
            lucid.environ.update_environ_var(lucid.constants.ENV_PROJECT, ['_template'])
            self.update_proj()
            print('Updating template proj! All future projects will be forged with these settings.')

    def update_proj(self):
        for i in range(self.proj_settings_tab_manager.count()):
            if hasattr(self.settings_tab_array[i], 'save_settings'):
                self.settings_tab_array[i].save_settings()

    def cmb_proj_connection(self):
        lucid.environ.update_environ_var(lucid.constants.ENV_PROJECT, [self.cmb_proj.currentText()])
        for i in range(self.proj_settings_tab_manager.count()):
            if isinstance(self.settings_tab_array[i], ProjSettingsTab):
                self.settings_tab_array[i].load_settings()

    def load_default_values(self):
        lucid.environ.update_environ_var(lucid.constants.ENV_PROJECT, ['_template'])
        for i in range(self.defaults_settings_tab_manager.count()):
            if isinstance(self.defaults_tab_array[i], ProjSettingsTab):
                self.defaults_tab_array[i].load_settings()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ProjectCreator()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()

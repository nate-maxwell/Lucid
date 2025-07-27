"""
# User Settings Menu

* Description:

    User's could have inconsistent machines, i.e. they have dcc and application
    paths in differing locations, and different drive structures. This menu
    allows users to inform the pipeline about their machine.
"""


import sys

from PySide2 import QtWidgets

from lucid.core import const
from lucid.core import io_utils
from lucid.core.widgets.main_window import LMainWindow
from lucid.launcher.application_settings import ApplicationSettings


class UserSettingsMenu(LMainWindow):
    def __init__(self) -> None:
        super().__init__('User Settings')
        self.application_rows: dict[str, ApplicationSettings] = {}
        self.setMinimumWidth(700)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.load_settings()

    def create_widgets(self) -> None:
        self.set_layout(QtWidgets.QVBoxLayout())

        for dcc in const.DCCs:
            str_val = dcc.value.replace('DCC_', '').title()
            app_row = ApplicationSettings(str_val)
            app_row.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Preferred)
            self.application_rows[str_val] = app_row

        self.hlayout_save = QtWidgets.QHBoxLayout()
        self.btn_save = QtWidgets.QPushButton('Save')
        self.btn_save.setFixedSize(100, 35)

    def create_layout(self) -> None:
        for _, i in self.application_rows.items():
            self.layout_main.addWidget(i)
        self.layout_main.addStretch()

        self.hlayout_save.addStretch()
        self.hlayout_save.addWidget(self.btn_save)
        self.add_layout(self.hlayout_save)

    def create_connections(self) -> None:
        self.btn_save.clicked.connect(self.save_settings)

    def load_settings(self) -> None:
        if not const.USER_SETTINGS_FILE.exists():
            return

        data = io_utils.import_data_from_json(const.USER_SETTINGS_FILE)
        if not data:
            return

        for k, v in data.items():
            self.application_rows[k].file_selector.le_path.text = v

    def save_settings(self) -> None:
        data: dict[str, str] = {}
        for k, v in self.application_rows.items():
            data[k] = v.file_selector.le_path.text
        io_utils.export_data_to_json(const.USER_SETTINGS_FILE, data, True)


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    lucid_settings_window = UserSettingsMenu()
    lucid_settings_window.show()

    app.exec_()


if __name__ == '__main__':
    main()

"""
# Environment Var UI

* Description:

    A simple menu for users to adjust the environment vars if they need to.
    DCC agnostic, although it will accept a Shiboken pointer to the maya main window.
    You must also specify a key prefix to weed out unwanted os.environ keys.
    This should be something all the keys that are relevant to your DCC tools start with.

* Update History:

    `2023-11-09` - Init
"""


import os

from PySide2 import QtWidgets
from PySide2 import QtCore

import lucid.ui.qt


class _EnvironEntry(QtWidgets.QVBoxLayout):
    """
    A QVBoxLayout that contains a QTextEdit for storing all the key entries.

    Args:
        environ_var(str): The environment var to handle the variables for.

    Notes:
        update_environment() will join each line of the text edit with ';'
        and store the results in the environment var used to created the
        class.
    """
    def __init__(self, environ_var: str):
        super().__init__()
        self.lbl_environ_var = QtWidgets.QLabel(environ_var)
        self.te_values = QtWidgets.QTextEdit()

        self.addWidget(self.lbl_environ_var)
        self.addWidget(self.te_values)

        values = os.getenv(environ_var).split(';')
        entries = ''
        for v in values:
            entries += (v + '\n')

        self.te_values.setPlainText(entries)

    def update_environment(self) -> None:
        values = self.te_values.toPlainText().split('\n')
        update = ';'.join(values)
        os.environ[self.lbl_environ_var.text()] = update


class EnvVarMenu(QtWidgets.QMainWindow):
    """
    A simple window for displaying and updating environment variables.

    A key prefix must be provided to weed out unrelated environment vars.
    This should be something that all the keys, that you want to display, start with.
    """
    def __init__(self, key_prefix: str = '', maya_parent_ref: QtWidgets.QWidget = None):
        if maya_parent_ref:
            super(EnvVarMenu, self).__init__(maya_parent_ref)
        else:
            super().__init__()

        self.key_prefix = key_prefix
        self.environment_entries = []

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.setCentralWidget(self.main_widget)

        self.setMinimumSize(500, 600)
        self.setWindowTitle('Environment Customization')
        lucid.ui.qt.set_pipeline_qss(self)

    def create_widgets(self) -> None:
        # Main
        self.layout_main = QtWidgets.QVBoxLayout()
        self.main_widget = QtWidgets.QWidget()

        self.hlayout_update = QtWidgets.QHBoxLayout()

        self.sa_environ = QtWidgets.QScrollArea()
        self.sa_environ.setWidgetResizable(True)
        self.sa_environ.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.sa_environ.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.widget_environ = QtWidgets.QWidget()
        self.vlayout_environ = QtWidgets.QVBoxLayout()

        env_vars = os.environ.keys()
        for k in env_vars:
            if k.startswith(self.key_prefix):
                entry = _EnvironEntry(k)
                self.vlayout_environ.addLayout(entry)
                self.environment_entries.append(entry)

        self.btn_update = QtWidgets.QPushButton('Update Environment')

    def create_layout(self) -> None:
        self.widget_environ.setLayout(self.vlayout_environ)
        self.sa_environ.setWidget(self.widget_environ)
        self.layout_main.addWidget(self.sa_environ)
        self.layout_main.addLayout(self.hlayout_update)
        self.hlayout_update.addStretch()
        self.hlayout_update.addWidget(self.btn_update)
        self.main_widget.setLayout(self.layout_main)

    def create_connections(self) -> None:
        self.btn_update.clicked.connect(self.update_environment)

    def update_environment(self) -> None:
        for e in self.environment_entries:
            e.update_environment()

"""
# Environment Var UI for Unreal

* Description:

    A simple wrapper for lucid.ui.envvar_menu for UE.

* Update History:

    `2023-09-26` - Init

    `2023-10-27` - Added missing lucid.constants import
"""


import sys
from pathlib import Path

import unreal
from PySide2 import QtWidgets

import lucid.constants
from lucid.ui.envvar_menu import EnvVarMenu


global window_singleton


class UnrealEnvVarMenu(EnvVarMenu):
    """This exists primarily for the global window_singleton var for the main function."""
    def __init__(self):
        super().__init__('LUCID_', None)
        global window_singleton
        window_singleton = self


def main():
    global window_singleton

    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except:
        pass

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    window_singleton = UnrealEnvVarMenu()
    window_singleton.show()
    unreal.parent_external_window_to_slate(window_singleton.winId())

    qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
    with open(qss_path, 'r') as f:
        style = f.read()
        app.setStyleSheet(style)


if __name__ == '__main__':
    main()

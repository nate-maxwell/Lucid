"""
# Environment Var UI

* Description:

    A simple menu for users to adjust the environment vars if they need to.

* Update History:

    `2023-09-11` - Init
"""


import lucid.maya
from lucid.ui.envvar_menu import EnvVarMenu


global window_singleton  # Global for singleton


class EnvironmentMenu(EnvVarMenu):
    def __init__(self):
        super().__init__('LUCID_', lucid.maya.get_maya_window())
        global window_singleton
        window_singleton = self


def main():
    """Close and create UI in singleton fashion."""
    global window_singleton

    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except NameError:
        pass

    window_singleton = EnvironmentMenu()
    window_singleton.show()


if __name__ == '__main__':
    main()

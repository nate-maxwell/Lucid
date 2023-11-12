"""
# Lucid Maya Developer Library

* Description:

    Developer and debug functions exclusive to Maya development.

* Update History:

    `2023-10-24` - Init
"""


from PySide2 import QtWidgets

import lucid.maya


global window_singleton


class Reimporter(QtWidgets.QMainWindow):
    """
    A class for conveniently reimporting modules.

    The list of modules listed is manually made within the class.
    This is primarily to handpick which modules should be able to be
    reimported.
    """
    def __init__(self):
        super(Reimporter, self).__init__(lucid.maya.get_maya_window())

        global window_singleton
        window_singleton = self

        self.setWindowTitle(f'Easy Module Reimporter')
        self.resize(350, 50)

        self.layout_main = QtWidgets.QHBoxLayout()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)
        self.cmb_modules = QtWidgets.QComboBox()
        self.btn_reimport = QtWidgets.QPushButton('Reimport Module')
        self.layout_main.addWidget(QtWidgets.QLabel('Module: '))
        self.layout_main.addWidget(self.cmb_modules)
        self.layout_main.addWidget(self.btn_reimport)

        modules = [
            'constants',
            'color',
            'debug',
            'environ',
            'io_utils',
            'legex',
            'maya',
            'maya.anim_browser',
            'maya.anim_publisher',
            'maya.asset_browser',
            'maya.asset_publisher',
            'maya.common_actions',
            'maya.confirm_window',
            'maya.developer',
            'maya.io',
            'ui.qt',
            'ui.components',
            'rename',
            'schema'
        ]
        modules.sort()
        self.cmb_modules.addItems(modules)

        self.btn_reimport.clicked.connect(self.btn_reimport_connection)

    def btn_reimport_connection(self) -> None:
        cmd = f'import importlib\n'\
              f'importlib.reload(lucid.{self.cmb_modules.currentText()})'
        print(cmd)
        exec(cmd)


def show_reimport_window() -> None:
    """Close and create Reimporter in singleton fashion."""
    global window_singleton

    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except NameError:
        pass

    reimport_window = Reimporter()
    reimport_window.show()

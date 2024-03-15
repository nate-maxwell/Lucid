"""
# Lucid Maya Developer Library

* Description:

    Developer and debug functions exclusive to Maya development.

* Update History:

    `2023-10-24` - Init
"""


from PySide2 import QtWidgets

import lucid.maya
import lucid.ui.qt


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

        lucid.ui.qt.set_pipeline_qss(self)

        global window_singleton
        window_singleton = self

        self.setWindowTitle(f'Easy Module Reimporter')
        self.resize(350, 50)

        self.layout_main = QtWidgets.QVBoxLayout()

        # Single import line
        self.hlayout_single_import = QtWidgets.QHBoxLayout()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)
        self.cmb_modules = QtWidgets.QComboBox()
        self.btn_reimport = QtWidgets.QPushButton('Reimport Module')
        self.hlayout_single_import.addWidget(QtWidgets.QLabel('Module: '))
        self.hlayout_single_import.addWidget(self.cmb_modules)
        self.hlayout_single_import.addWidget(self.btn_reimport)

        # import all line
        self.btn_import_all = QtWidgets.QPushButton('Import All')

        self.layout_main.addLayout(self.hlayout_single_import)
        self.layout_main.addWidget(self.btn_import_all)

        self.modules = [
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
            'rename',
            'schema'
        ]
        self.modules.sort()
        self.cmb_modules.addItems(self.modules)

        self.btn_reimport.clicked.connect(self.btn_reimport_connection)
        self.btn_import_all.clicked.connect(self.btn_import_all_connection)

    def btn_reimport_connection(self):
        module = self.cmb_modules.currentText()
        cmd = f'import importlib\ntry:\n\timportlib.reload(lucid.{module})\nexcept AttributeError:\n\timport lucid.{module}'
        print(cmd)
        exec(cmd)

    def btn_import_all_connection(self):
        for i in self.modules:
            cmd = f'import importlib\ntry:\n\timportlib.reload(lucid.{i})\nexcept AttributeError:\n\timport lucid.{i}'
            print(cmd)
            exec(cmd)


def show_reimport_window():
    """Close and create Reimporter in singleton fashion."""
    global window_singleton

    try:
        window_singleton.close()
        window_singleton.deleteLater()
    except NameError:
        # temp
        pass

    window_singleton = Reimporter()
    window_singleton.show()

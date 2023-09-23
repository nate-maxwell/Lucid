"""Lucid Maya"""


import shiboken2
from PySide2 import QtWidgets
from maya import OpenMayaUI


def get_maya_window() -> QtWidgets.QMainWindow:
    """Return the Maya main window widget as a python object."""
    return shiboken2.wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QMainWindow)

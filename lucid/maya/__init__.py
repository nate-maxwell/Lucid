"""Lucid Maya"""


from typing import Callable

import shiboken2
from PySide2 import QtWidgets
from maya import OpenMayaUI
from maya import cmds


def get_maya_window() -> QtWidgets.QMainWindow:
    """Return the Maya main window widget as a python object."""
    return shiboken2.wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QMainWindow)


def retain_selection(func: Callable):
    """
    Decorator for retaining selected nodes after executing a function.
    The nodes are queried before the function executes and then set as
    the selection once the function finishes executing.

    Example:
        >>>@retain_selection
        >>>def format_my_scene(nodes: list):
        >>>     # Some actions that require changing/modifying selected nodes.
        >>>     ...
    """
    def inner_func(*args, **kwargs):
        selected = cmds.ls(selection=True)
        func(*args, **kwargs)
        cmds.select(selected)

    return inner_func

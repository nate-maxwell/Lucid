"""
# Lucid Maya

* Description

    Lucid's primary maya module.

* Update History

    `2023-09-22` - Init

    `2023-11-17` - Added UndoChunk.
"""

from typing import Callable

import shiboken2
from PySide2 import QtWidgets
from maya import OpenMayaUI
from maya import cmds


def get_maya_window() -> QtWidgets.QMainWindow:
    """Return the Maya main window widget as a python object."""
    return shiboken2.wrapInstance(int(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QMainWindow)


class UndoChunk(object):
    """
    Lucid manager for a Maya undoChunk.

    Everything under the `with` statement will be grouped into a single undo
    action. This is similar to pymel's `pymel.core.system.UndoChunk`, with the
    exception that this implementation forces you to provide an undo name.

    Examples:
        >>> with UndoChunk('Duplicate and mirror'):
        >>>     # Everything here will be part of a single undoChunk
        >>>     ...
        >>>
    """
    def __init__(self, chunk_name: str):
        self.chunk_name = chunk_name

    def __enter__(self):
        cmds.undoInfo(openChunk=True, chunkName=self.chunk_name)

    def __exit__(self, exc_type, exc_val, traceback):
        cmds.undoInfo(closeChunk=True)


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

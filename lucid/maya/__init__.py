from typing import Any
from typing import Callable

import maya.cmds
import maya.OpenMayaUI as omui
import shiboken2
from PySide2 import QtWidgets


class UndoChunk:
    """Context manager for a Maya undoChunk.

    Everything under the `with` statement will be grouped into a single undo
    action. This is similar to pymel's `pymel.core.system.UndoChunk`, with the
    exception that this implementation forces you to provide an undo name.

    Examples:
        >>> with UndoChunk('Duplicate and mirror'):
        >>>     # Everything here will be part of a single undoChunk
        >>>     ...
        >>>
    """

    def __init__(self, chunk_name: str) -> None:
        self.chunk_name = chunk_name

    def __enter__(self) -> None:
        maya.cmds.undoInfo(openChunk=True, chunkName=self.chunk_name)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        maya.cmds.undoInfo(closeChunk=True)


def get_main_window() -> QtWidgets.QMainWindow:
    """Get the Maya main window as a QMainWindow instance."""
    return shiboken2.wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow)


def open_command_port() -> None:
    """
    Open a Maya command port to enable sending code from VSCode.
    Will skip execution of an instance of maya is already running
    connected to this port.
    """
    try:
        maya.cmds.commandPort(name='localhost:7001')
    except RuntimeError:
        pass


def retain_selection(func: Callable) -> Callable:
    """
    Decorator for retaining selected nodes after executing a function.
    The nodes are queried before the function executes and then set as the
    selection, once the function finishes executing.

    Examples:
        >>> @retain_selection
        >>> def format_my_scene(nodes: list):
        >>>     # Some actions that require changing/manipulating selected nodes.
        >>>     ...
        >>>
    """
    def inner_func(*args, **kwargs) -> Any:
        selected = maya.cmds.ls(selection=True)
        func(*args, **kwargs)
        maya.cmds.select(selected)

    return inner_func

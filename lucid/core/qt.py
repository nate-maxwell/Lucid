"""
# Lucid Qt Utilities

* Descriptions

    A library of PyQt/PySide helper functions.
"""


import json
from pathlib import Path
from typing import Optional
from typing import Union

from PySide2 import QtCore
from PySide2 import QtWidgets

from lucid.core import gui_paths
from lucid.core import io_utils


def remove_layout(layout: QtWidgets.QLayout) -> None:
    """
    Recursively empties and deletes a layout by deleting each element.

    Args:
        layout(QtWidgets.QLayout): The layout to remove. Deletes children of layout.
    """
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                remove_layout(item.layout())


def set_pipeline_qss(tool: QtWidgets.QWidget, qss_name: str = 'Combinear.qss') -> None:
    """
    Sets the style sheet, from a qss file in the pipeline resources folder.

    Args:
        tool(QtWidgets.QWidget): Which tool to set the style sheet for. This should
        be called within the tool's constructor and should pass self through, although
        it can be called through some style sheet manager/function.

        qss_name(str): The name of the style sheet to use.
    """
    # Extension check
    qss_input_name = Path(qss_name)
    qss_file_name = f'{qss_input_name.stem}.qss'

    qss_path = Path(gui_paths.RESOURCES_PATH, qss_file_name)
    with open(qss_path, 'r') as f:
        stylesheet = f.read()
        tool.setStyleSheet(stylesheet)


def get_main_window_parent(widget: QtWidgets.QWidget) -> Optional[QtWidgets.QMainWindow]:
    """
    Returns the QtWidgets.QMainWindow that contains a given widget.

    Args:
        widget(QtWidgets.QWidget): The widget to get the parent QMainWindow from.

    Returns:
        QtWidgets.QMainWindow: The owning QMainWindow currently holding the widget.
    """
    parent_widget = widget.parent()
    while parent_widget is not None:
        if isinstance(parent_widget, QtWidgets.QMainWindow):
            return parent_widget
        parent_widget = parent_widget.parent
    return None


def save_json_to_qsettings(data: dict,
                           settings: QtCore.QSettings,
                           settings_val: str) -> None:
    """
    Saves the given dict to the q settings object under the settings value.

    Args:
        data (dict): The data to serialize
        settings (QtCore.QSettings): The settings object to save it to.
        settings_val (str): The value name to save it under.
    """
    json_string = json.dumps(data)
    settings.setValue(settings_val, json_string)


def load_json_from_qsettings(settings: QtCore.QSettings,
                             settings_val: str) -> Optional[dict]:
    """

    Args:
        settings (QtCore.QSettings): The settings object to pull from.
        settings_val (str): The settings field to pull from.

    Returns:
        Optional[dict]: The json data if it could be retrieved, else None.
    """
    json_string = settings.value(settings_val, type=str)
    if json_string:
        try:
            data = json.loads(json_string)
            return data
        except json.JSONDecodeError as e:
            io_utils.print_error_msg(f'Failed to parse q settings: {e}')
            return None

    return None

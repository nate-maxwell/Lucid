"""
# Lucid Qt Utilities

* Descriptions

    A library of PyQt/PySide helper functions.

* Update History

    `2023-09-20` - Init
"""


from pathlib import Path

from PySide2 import QtWidgets

import lucid.constants


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

    qss_path = Path(lucid.constants.RESOURCE_PATH, qss_file_name)
    with open(qss_path, 'r') as f:
        stylesheet = f.read()
        tool.setStyleSheet(stylesheet)


def get_main_window_parent(widget: QtWidgets.QWidget) -> QtWidgets.QMainWindow:
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

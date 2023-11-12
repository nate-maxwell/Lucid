"""
# Lucid Qt Utilities

* Descriptions

    A library of PyQt/PySide helper functions.

* Update History

    `2023-09-20` - Init
"""


from PySide2 import QtWidgets


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

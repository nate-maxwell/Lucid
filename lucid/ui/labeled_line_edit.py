"""
# Environment Combo Box

* Description

    A simple row widget with a label and a line edit.

* Update History

    `2024-02-14` - Init
"""


from PySide2 import QtWidgets


class LabeledLineEdit(QtWidgets.QWidget):
    """
    A simple QHBoxLayout with a label and a line edit.

    Args:
        label(str): The label for the row.

        default_text(str): The default text to give the line edit.
    """
    def __init__(self, label: str, default_text: str):
        super().__init__()
        self.layout_main = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout_main)
        self.layout_main.addWidget(QtWidgets.QLabel(label))
        self.line_edit = QtWidgets.QLineEdit()
        if default_text:
            self.line_edit.setText(default_text)
        self.layout_main.addWidget(self.line_edit)

    @property
    def text(self) -> str:
        """Shortened namespace way to get current text."""
        return self.line_edit.text()

    def clear(self) -> None:
        """Shortened namespace way to clear text."""
        self.line_edit.clear()

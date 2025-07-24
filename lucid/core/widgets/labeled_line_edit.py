"""
# Labeled Line Edit

* Description:

    QLineEdit wrapper that adds label.
"""


from typing import Optional

from PySide2 import QtWidgets


class LLabeledLineEdit(QtWidgets.QWidget):
    def __init__(self, label: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self.layout_main = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout_main)

        self._label = QtWidgets.QLabel(label)
        self.line_edit = QtWidgets.QLineEdit()

        self.layout_main.addWidget(self._label)
        self.layout_main.addWidget(self.line_edit)

    @property
    def text(self) -> str:
        return self.line_edit.text()

    @text.setter
    def text(self, text: str) -> None:
        self.line_edit.setText(text)

    @property
    def label(self) -> str:
        return self._label.text()

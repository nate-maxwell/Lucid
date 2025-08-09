"""
# Labeled Combobox

* Description:

    QComboBox wrapper that adds label.
"""


from typing import Optional

from PySide2 import QtWidgets


class LabeledComboBox(QtWidgets.QWidget):
    def __init__(self, label: str, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self.layout_main = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout_main)

        self._label = QtWidgets.QLabel(label)
        self.combobox = QtWidgets.QComboBox()

        self.layout_main.addWidget(self._label)
        self.layout_main.addWidget(self.combobox)
        self.layout_main.addStretch()

    def add_item(self, item: str) -> None:
        self.combobox.addItem(item)

    def add_items(self, items: list[str]) -> None:
        self.combobox.addItems(items)

    @property
    def current_text(self) -> str:
        return self.combobox.currentText()

    @property
    def label(self) -> str:
        return self._label.text()

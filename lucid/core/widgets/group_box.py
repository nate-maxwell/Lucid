"""
# Group Box

* Description:

    QGroupBox wrapper to eliminate boilerplate.
"""


from PySide2 import QtWidgets


class LGroupBox(QtWidgets.QGroupBox):
    def __init__(self, label: str = '', horizontal: bool = False) -> None:
        super().__init__(label)
        if horizontal:
            self.layout = QtWidgets.QHBoxLayout()
        else:
            self.layout = QtWidgets.QVBoxLayout()

        self.setLayout(self.layout)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        self.layout.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout) -> None:
        self.layout.addLayout(layout)

    def add_stretch(self) -> None:
        self.layout.addStretch()

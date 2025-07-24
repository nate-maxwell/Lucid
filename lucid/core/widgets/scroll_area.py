"""
# Scroll Area

* Descriptions

    Small wrapper for a Qt scroll area to eliminate writing the layout
    setting, saving a few lines.
"""


from PySide2 import QtWidgets


class LScrollArea(QtWidgets.QScrollArea):
    def __init__(self, horizontal: bool = False) -> None:
        super().__init__()
        self.setWidgetResizable(True)
        self.widget_main = QtWidgets.QWidget()
        self.widget_main.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.widget_main)
        if horizontal:
            self.layout = QtWidgets.QHBoxLayout()
        else:
            self.layout = QtWidgets.QVBoxLayout()
        self.widget_main.setLayout(self.layout)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        self.layout.addWidget(widget)

    def add_layout(self, layout: QtWidgets.QLayout) -> None:
        self.layout.addLayout(layout)

    def add_stretch(self) -> None:
        self.layout.addStretch()

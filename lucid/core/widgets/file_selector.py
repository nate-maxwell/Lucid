"""
# File Path Selection Widget

* Description:

    A simple gui class that lets users specify file paths through a QFileDialog
    and then displays and stores the path.
"""


from pathlib import Path

from PySide2 import QtWidgets

from lucid.core.widgets.group_box import GroupBox
from lucid.core.widgets.labeled_line_edit import LabeledLineEdit


class FileSelector(QtWidgets.QWidget):
    def __init__(self, name: str) -> None:
        """Label text before line edit."""
        super().__init__()
        self.name = name
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self) -> None:
        self.hlayout_main = QtWidgets.QHBoxLayout()
        self.le_path = LabeledLineEdit(self.name)
        self.le_path.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Preferred)
        self.btn_exe = QtWidgets.QPushButton('Open')

    def create_layout(self) -> None:
        self.hlayout_main.addWidget(self.le_path)
        self.hlayout_main.addWidget(self.btn_exe)
        self.setLayout(self.hlayout_main)

    def create_connections(self) -> None:
        self.btn_exe.clicked.connect(self.find_path)

    def find_path(self) -> None:
        directory = ''
        if self.le_path.text:
            directory = self.le_path.text
        location = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', directory)
        self.le_path.text = location[0]

    @property
    def path(self) -> Path:
        return Path(self.le_path.text)

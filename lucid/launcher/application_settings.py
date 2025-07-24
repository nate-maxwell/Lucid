"""
# Application Path Settings Widget

* Description:

    A simple gui class that lets users specify where applications are on their
    local system.
"""


from pathlib import Path

from PySide2 import QtWidgets

from lucid.core.widgets.group_box import LGroupBox
from lucid.core.widgets.labeled_line_edit import LLabeledLineEdit


class ApplicationSettings(LGroupBox):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self) -> None:
        self.hlayout_app_path = QtWidgets.QHBoxLayout()
        self.le_path = LLabeledLineEdit('EXE Path:')
        self.le_path.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Preferred)
        self.btn_exe = QtWidgets.QPushButton('Open')

    def create_layout(self) -> None:
        self.hlayout_app_path.addWidget(self.le_path)
        self.hlayout_app_path.addWidget(self.btn_exe)
        self.add_layout(self.hlayout_app_path)

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

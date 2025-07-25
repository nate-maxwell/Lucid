"""
# Application Path Settings Widget

* Description:

    A simple gui class that lets users specify where applications are on their
    local system.
"""


from pathlib import Path

from lucid.core.widgets.file_selector import FileSelector
from lucid.core.widgets.group_box import LGroupBox


class ApplicationSettings(LGroupBox):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name
        self.create_widgets()
        self.create_layout()

    def create_widgets(self) -> None:
        self.file_selector = FileSelector('EXE Path:')

    def create_layout(self) -> None:
        self.add_widget(self.file_selector)

    @property
    def path(self) -> Path:
        return self.file_selector.path

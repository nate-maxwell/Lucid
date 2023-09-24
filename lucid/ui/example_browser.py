"""
An example way to build a file browser using the lucid.ui.components.LucidFileBrowser.
Doubles as a manual unit test.
"""


import sys
from pathlib import Path

from PySide2 import QtWidgets

import lucid.io_utils
from lucid.ui.components import LucidFileBrowser


labels = ['first', 'second', 'third', 'fourth', 'fifth']
test_dir = Path('E:/')


class ExampleManager(LucidFileBrowser):
    def __init__(self):
        super().__init__(labels, test_dir, (1000, 500), (1000, 500))

    def column_action(self, index: int):
        if index == 0:  # First column
            self.clear_columns_right_of(0)
            self.fill_column_at_index(1)
        elif index == len(self.column_labels):  # Last column
            pass
        else:
            self.fill_column_at_index(index + 1)  # Middle columns

    def fill_column_at_index(self, index: int):
        if '.' not in self.tokens[index - 1]:
            self.clear_columns_right_of(index - 1)
            path = self.default_path
            for i in range(index + 1):
                path = Path(path, self.tokens.get(i))

            if path.exists():
                self.columns[index].populate_column(lucid.io_utils.list_folder_contents(path))


class ExampleBrowser(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent = None)
        self.setWindowTitle('Example Browser')

        # Default Values
        self.column_manager = ExampleManager()
        self.column_manager.columns[0].populate_column(lucid.io_utils.list_folder_contents(self.column_manager.default_path))

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def create_layout(self):
        self.main_layout.addWidget(self.column_manager)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    browser_window = ExampleBrowser()
    browser_window.show()
    app.exec_()

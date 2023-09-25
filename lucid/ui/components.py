"""
# Qt Components

* Description

    A library of qt widget components created for Lucid that were too
    small to require their own file.

* Update History

    `2023-09-20` - Init
"""


from pathlib import Path

from PySide2 import QtWidgets
from PySide2 import QtCore

import lucid.ui.qt


class SearchableList(QtWidgets.QVBoxLayout):
    """
    A component class representing a searchable list of items.
    This is primarily intended for file/asset/folder listing within the Lucid
    pipeline directory structure.

    Args:
        column_label(str):
        Name of the column, displayed above the column.

        id_num(int):
        An index, or int id, number to keep track of each instanced SearchableList.

    Relevant Methods:
        populate_column(contents: list[str]):
        Populates the column from a list of string items.

        clear_list:
        Clears the items from the QListWidget component.
    """
    def __init__(self, column_label: str, id_num: int):
        super().__init__()
        self.column_label = column_label
        self.id = id_num

        self.le_search = QtWidgets.QLineEdit()
        self.list_column = QtWidgets.QListWidget()
        self.lbl_column = QtWidgets.QLabel(column_label)
        self.lbl_column.setAlignment(QtCore.Qt.AlignCenter)
        self.contents: list[str] = []

        self.addWidget(self.lbl_column)
        self.addWidget(self.le_search)
        self.addWidget(self.list_column)

        self.list_column.itemClicked.connect(self.item_selected)
        self.le_search.textChanged.connect(self._search_list)

    def _search_list(self):
        """
        Refines the items to the input text of self.le_search. Uses self.contents,
        set in self.populate_column(), to retain original items.
        """
        self.clear_list()
        if len(self.le_search.text()) > 0:
            for item in self.contents:
                if self.le_search.text().upper() in item.upper():
                    self.list_column.addItem(item)
        else:
            self.list_column.addItems(self.contents)

    def clear_list(self):
        """Shortened namedspace way to clear the list."""
        self.list_column.clear()

    def populate_column(self, contents: list[str]):
        """Adds a list of strings to the QListWidget."""
        self.contents = contents
        self.list_column.clear()
        self.list_column.addItems(self.contents)

    def item_selected(self, item):
        """
        A function connected to the on click event of an item in the QListWidget.
        This can be overridden in manager/parent classes to conveniently connect
        events to the user selecting an item.
        """
        pass

    @property
    def selected_item(self):
        return self.list_column.currentItem().text()


class LucidFileBrowser(QtWidgets.QMainWindow):
    """
    A column based file manager for Lucid asset/file browsers. This is a QtWidget
    that can be inserted into other widgets.

    Args:
        column_labels(list[str]): The names of the columns to initialize the browser with.
        default_path(Path): The default path used to construct the contents of the first column.
        Although this does not contribute to any logic, derived classes can conveniently use this
        for path building logic.
        min_size(tuple[int, int]): The minimum x, y size of the window, if the values are
        greater than (0,0). Defaults to (0, 0)
        max_size(tuple[int, int]): The maximum x, y size of the window, if the values are
        greater than (0,0). Defaults to (0, 0)
        maya_parent_ref(QtWidgets.QWidget): The ref to the maya parent window. If this is
        filled, you do not need to embed into another widget. Defaults to None.
    """
    def __init__(self,column_labels: list[str], default_path: Path,
                 min_size: tuple[int, int] = (0, 0), max_size: tuple[int, int] = (0, 0),
                 maya_parent_ref: QtWidgets.QWidget = None):
        if maya_parent_ref:
            super(LucidFileBrowser, self).__init__(maya_parent_ref)
        else:
            super().__init__()

        self.column_labels = column_labels

        if not min_size == (0, 0):
            self.resize(min_size[0], min_size[1])
            self.setMinimumSize(min_size[0], min_size[1])
        if not max_size == (0, 0):
            self.setMaximumSize(max_size[0], max_size[1])

        self.tokens: dict[int, str] = {}
        self.columns: list[_LFBList] = []
        self.hlayout_columns = QtWidgets.QHBoxLayout()
        self.setLayout(self.hlayout_columns)
        self.default_path = default_path

        for i in self.column_labels:
            self.add_column_to_right(i)
            self.tokens[self.column_labels.index(i)] = ''

    def _column_listener(self, index: int, value: str):
        """_LFBList children will call this on parent to update self.tokens and trigger self.column_action"""
        self.tokens[index] = value
        self.column_action(index)

    def column_action(self, index: int):
        """
        This method should be overwritten in derived classes to call a function
        based on the received index: int of the _LFBList children.
        """
        pass

    def add_column_to_right(self, column_label: str):
        """Adds a column to the right side of the list horizontal box layout."""
        index = len(self.columns)
        self.tokens[index] = ''
        self.columns.append(_LFBList(self, column_label, index))
        self.hlayout_columns.addLayout(self.columns[-1])

    def remove_columns_to_right_of(self, index: int):
        """Removes all lists columns to the right of the specified index in self.columns."""
        if len(self.columns) > 1:
            self.columns = self.columns[:index + 1]

            for child in self.hlayout_columns.children():
                if child not in self.columns:
                    self.hlayout_columns.removeItem(child)
                    lucid.ui.qt.remove_layout(child)

            keys = list(self.tokens)
            for k in keys:
                if keys.index(k) > index:
                    self.tokens.pop(k)

    def clear_columns_right_of(self, index: int):
        """
        Empty the list columns if they appear after the given index in self.columns.
        This also sets the self.tokens value for that column to ''.
        """
        for i in self.columns:
            if self.columns.index(i) > index:
                i.clear_list()
                self.tokens[self.columns.index(i)] = ''
                i.le_search.clear()


class _LFBList(SearchableList):
    def __init__(self, lucid_file_browser: LucidFileBrowser, column_label: str, index: int):
        super().__init__(column_label, index)
        self.lucid_file_browser = lucid_file_browser

    def item_selected(self, item):
        """Sends information back to LucidFileBrowser class."""
        self.lucid_file_browser._column_listener(self.id, item.text())

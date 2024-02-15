"""
# File Browser

* Description

    A column based file browser.

* Update History

    `2024-02-14` - Init
"""


from typing import Optional
from pathlib import Path

from PySide2 import QtWidgets

from lucid.ui.searchable_list import SearchableList
import lucid.ui.qt


class LucidFileBrowser(QtWidgets.QMainWindow):
    """
    A column based file manager for Lucid asset/file browsers.

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
    def __init__(self, column_labels: list[str], default_path: Path,
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

    def _column_listener(self, index: int, value: str) -> None:
        """_LFBList children will call this on parent to update self.tokens and trigger self.column_action"""
        self.tokens[index] = value
        self.column_action(index)

    def column_action(self, index: int) -> None:
        """
        This method should be overwritten in derived classes to call a function
        based on the received index: int of the _LFBList children.
        """
        pass

    def add_column_to_right(self, column_label: str) -> None:
        """Adds a column to the right side of the list horizontal box layout."""
        index = len(self.columns)
        self.tokens[index] = ''
        self.columns.append(_LFBList(self, column_label, index))
        self.hlayout_columns.addLayout(self.columns[-1])

    def remove_columns_to_right_of(self, index: int) -> None:
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

    def clear_columns_right_of(self, index: int) -> None:
        """
        Empty the list columns if they appear after the given index in self.columns.
        This also sets the self.tokens value for that column to ''.
        """
        for i in self.columns:
            if self.columns.index(i) > index:
                i.clear_list()
                self.tokens[self.columns.index(i)] = ''
                i.le_search.clear()

    def get_selected_by_column_label(self, label: str) -> Optional[str]:
        """
        Gets the selected item of the column with the given label.

        Args:
            label(str): The label to match the columns by.

        Returns:
            str: The selected value of the found column. Returns None
            if no column was found.
        """
        for i in self.columns:
            if i.column_label == label:
                return i.selected_item
        else:
            return None

    def all_columns_check(self) -> bool:
        """
        Loops through each column to make sure there is a selected item.

        Returns:
            bool: Returns False if a single column.selected_item == None,
            else returns True.
        """
        for i in self.columns:
            if not i.selected_item:
                return False
        else:
            return True


class _LFBList(SearchableList):
    def __init__(self, lucid_file_browser: LucidFileBrowser, column_label: str, index: int):
        super().__init__(column_label, index)
        self.lucid_file_browser = lucid_file_browser

    def item_selected(self, item) -> None:
        """Sends information back to LucidFileBrowser class."""
        self.lucid_file_browser._column_listener(self.id, item.text())

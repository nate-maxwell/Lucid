"""
# Searchable List

* Description

    A list widget that can be filtered with a search box at the top.
    Widget is topped with a text label.

* Update History

    `2024-02-14` - Init
"""


from typing import Optional

from PySide2 import QtWidgets
from PySide2 import QtCore


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

    def _search_list(self) -> None:
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

    def clear_list(self) -> None:
        """Shortened namedspace way to clear the list."""
        self.list_column.clear()

    def populate_column(self, contents: list[str]) -> None:
        """Adds a list of strings to the QListWidget."""
        self.contents = contents
        self.list_column.clear()
        if contents:
            self.list_column.addItems(self.contents)

    def deselect_item(self) -> None:
        """Deselects any selected item."""
        self.list_column.clearSelection()

    def item_selected(self, item):
        """
        A function connected to the on click event of an item in the QListWidget.
        This can be overridden in manager/parent classes to conveniently connect
        events to the user selecting an item.
        """
        pass

    @property
    def selected_item(self) -> Optional[str]:
        """Returns the str form of the selected item if it exists, else returns None."""
        if self.list_column.currentItem():
            return self.list_column.currentItem().text()
        else:
            return None

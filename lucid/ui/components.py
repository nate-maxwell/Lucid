"""
# Qt Components

* Description

    A library of qt widget components created for Lucid that were too
    small to require their own file.

* Update History

    `2023-09-20` - Init

    `2023-09-25` - Converted LucidFileBrowser to QtWidgets.QMainWindow.
"""


from pathlib import Path
from typing import Optional

from PySide2 import QtWidgets
from PySide2 import QtCore

import lucid.ui.qt


class LabeledLineEdit(QtWidgets.QHBoxLayout):
    """
    A simple QHBoxLayout with a label and a line edit.

    Args:
        label(str): The label for the row.

        default_text(str): The default text to give the line edit.
    """
    def __init__(self, label: str, default_text: str):
        super().__init__()
        self.addWidget(QtWidgets.QLabel(label))
        self.line_edit = QtWidgets.QLineEdit()
        if default_text:
            self.line_edit.setText(default_text)
        self.addWidget(self.line_edit)

    @property
    def text(self) -> str:
        """Shortened namespace way to get current text."""
        return self.line_edit.text()

    def clear(self) -> None:
        """Shortened namespace way to clear text."""
        self.line_edit.clear()


class EnvironmentComboBox(QtWidgets.QHBoxLayout):
    """
    The primary widget for creating asset context rows in the
    lucid.maya.anim_publisher.MayaAnimPublisher.

    Args:
        parent_ui(MayaAnimPublisher): The managing maya asset publisher parent
        class. This is to communicate back to the parent if necessary.

        label(str): The name of the generated row.

        contents(list[str]): The initial list of items to add to the combobox.

        index(int): A unique id number in-case normal filtering is not doable.

        addable(bool): Whether to draw the (+) button next to the row and allow
        users to add items to the combo box.

    Properties:
        selected_item(str): The current text of the combobox.
    """

    def __init__(self, parent_ui, label: str, contents: list[str], index: int, addable: bool = True):
        super().__init__()

        self.parent_ui = parent_ui
        self.row_name = label
        self.index = index
        self.lbl_name = QtWidgets.QLabel(self.row_name)
        self.cmb_combobox = QtWidgets.QComboBox()
        self.cmb_combobox.addItems(contents)
        self.btn_add = QtWidgets.QPushButton('+')
        self.btn_add.setFixedSize(20, 20)

        self.addWidget(self.lbl_name)
        self.addWidget(self.cmb_combobox)

        self.cmb_combobox.activated.connect(self.update_parent)

        if addable:
            self.addWidget(self.btn_add)
            self.btn_add.clicked.connect(self.button_add_item)

    def update_parent(self) -> None:
        """Updates the following rows on the parent."""
        self.parent_ui.populate_box_at_index(self.index + 1)

    def button_add_item(self) -> None:
        """Adds the input to the combobox and updates the following rows."""
        item = QtWidgets.QInputDialog.getText(self.parent_ui, f'New {self.row_name}',
                                              f'New {self.row_name}' 'Name: ')
        selection = item[0]
        if selection:
            self.cmb_combobox.addItems([selection])
            self.cmb_combobox.setCurrentText(selection)

        self.parent_ui.populate_box_at_index(self.index + 1)

    @property
    def selected_item(self) -> str:
        """
        Shortened namespace way to get combo box value.

        Returns:
            str: The current text of the combobox.
        """
        return self.cmb_combobox.currentText()

    def set_box_contents(self, contents: list[str]) -> None:
        """
        Sets the items of the combobox to the given list.

        Args:
            contents(list[str]): The items to add to the combobox.
        """
        self.cmb_combobox.clear()
        if contents:
            self.cmb_combobox.addItems(contents)
        else:
            self.cmb_combobox.addItems([''])


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

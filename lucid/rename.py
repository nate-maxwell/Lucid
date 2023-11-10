"""
# Batch rename utilities

* Description:

    Batch renamer tool for processing large numbers of files.
    This file contains a standalone Batch Renamer application and a batch
    renamer QtWidgets.QVBoxlayout component that can be added to another
    Qt widget.

    This module doubles as a generic library of rename functions and each
    action can be called individually if needed.

    Some functions take a position input. The first character in a string
    is considered at position 1. The position before the first character
    of a string is considered position 0.

* Update History:

    `2023-11-09` - Init
"""


import os
import sys
from pathlib import Path

from PySide2 import QtWidgets

# TODO: Remove
sys.path.append(Path(__file__).parent.parent.as_posix())

import lucid.constants
import lucid.io_utils


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Rename Utility Functions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def insert_substring(string: str, insert: str = '', position: int = 0):
    """
    Inserts a string into another string at the given position.

    Args:
        string(str): The string to modify.
        insert(str): The substring to insert into the base string.
        Defaults to ''.
        position(int): The position to insert the substring at.
        Position 1 is after the first character.
        Defaults to 0.

    Returns:
        str: The modified string with the inserted substring.
    """
    pre = string[:position]
    post = string[position:]
    return f'{pre}{insert}{post}'


def append_substring(string: str, prefix: str = '', suffix: str = ''):
    """
    Adds a prefix and/or suffix to a string.

    Args:
        string(str): The string to modify.
        prefix(str): A string to append to the front of the base string.
        Defaults to ''.
        suffix(str): A string to append to the end fo the base string.
        Defaults to ''.

    Returns:
        str: The modified string with the provided prefix and suffix.
    """
    return f'{prefix}{string}{suffix}'


def remove_chars_from_ends(string: str, first_n: int = 0, last_n: int = 0):
    """
    Removes chars from the first n and last n positions.
    Args:
        string(str): The string to modify.
        first_n(int): The number of chars to remove from the beginning of the string.
        Defaults to 0.
        last_n(int): The number of chars to remove from teh end of the string.
        Defaults to 0.

    Returns:
        str: The modified string with the removed characters.
    """
    first = string[first_n:]
    last = first[:-last_n]

    return last


def remove_from_to_position(string: str, from_pos: int = 0, to_pos: int = 0):
    """
    Removes the substring between the from_pos and to_pos.

    Args:
        string(str): The string to modify.
        from_pos(int): The start position to check the substring for.
        Defaults to 0.
        to_pos(int): The end position to check the substring for.
        Defaults to 0.

    Returns:
        str: The modified string with the substring located in the given
        positions removed.
    """
    pre = string[:from_pos]
    post = string[to_pos:]

    return f'{pre}{post}'


def remove_substring(string: str, substring: str = ''):
    """
    Removes the substring from the given string.
    Only works if substring split makes 2 items.

    Args:
        string(str): The string to modify.
        substring(str): The substring to remove.
        Defaults to ''.

    Returns:
        str: The given string without the substring.
    """
    if substring and len(x := string.split(substring)) == 2:
        return f'{x[0]}{x[1]}'
    else:
        return string


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Batch Renamer Widget + Component Classes
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class StringInput(QtWidgets.QFormLayout):
    """A helper class for the batch renamer for procedurally generating string inputs."""
    def __init__(self, row_name: str):
        super().__init__()

        self.input = QtWidgets.QLineEdit()
        self.addRow(row_name, self.input)

    @property
    def value(self):
        if self.input.text():
            return self.input.text()
        else:
            return ''


class IntInput(QtWidgets.QFormLayout):
    """A helper class for the batch renamer for procedurally generating int inputs."""
    def __init__(self, row_name: str):
        super().__init__()

        self.input = QtWidgets.QSpinBox()
        self.addRow(row_name, self.input)

    @property
    def value(self):
        if self.input.value():
            return self.input.value()
        else:
            return 0


class BatchRenamer(QtWidgets.QVBoxLayout):
    """
    A batch rename QVBoxLayout component. Contains a list view for previewing
    changes of items. Only selected items in the list view are renamed.

    BatchRenamer also contains inputs for a series of rename actions:
    Insert at position, Add prefix/suffix, Remove first/last n chars,
    remove from/to position, remove words, and replace word with new word.
    Rename actions are performed in the order listed above, or left to right
    in the UI.
    """
    def __init__(self):
        super().__init__()

        self.selected_items = []
        self.unedited_list = []

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        # Preview
        self.hlayout_lists = QtWidgets.QHBoxLayout()

        self.vlayout_preview_before = QtWidgets.QVBoxLayout()
        self.grp_preview_before = QtWidgets.QGroupBox('Before')
        self.scroll_preview_before = QtWidgets.QScrollArea()
        self.list_before_preview = QtWidgets.QListWidget()
        self.scroll_preview_before.setWidget(self.list_before_preview)
        self.scroll_preview_before.setWidgetResizable(True)
        self.scroll_preview_before.setFixedHeight(600)

        self.vlayout_preview_after = QtWidgets.QVBoxLayout()
        self.grp_preview_after = QtWidgets.QGroupBox('After')
        self.scroll_preview_after = QtWidgets.QScrollArea()
        self.list_after_preview = QtWidgets.QListWidget()
        self.scroll_preview_after.setWidget(self.list_after_preview)
        self.scroll_preview_after.setWidgetResizable(True)
        self.scroll_preview_after.setFixedHeight(600)

        self.list_before_preview.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.selection_model = self.list_before_preview.selectionModel()

        # Rename Actions
        self.hlayout_actions = QtWidgets.QHBoxLayout()

        # Insert
        self.vlayout_insert = QtWidgets.QVBoxLayout()
        self.lbl_insert = QtWidgets.QLabel('1 - Insert')
        self.insert_word = StringInput('Insert')
        self.insert_at_pos = IntInput('At Pos.')

        # Add
        self.vlayout_add = QtWidgets.QVBoxLayout()
        self.lbl_add = QtWidgets.QLabel('2 - Add')
        self.add_prefix = StringInput('Prefix')
        self.add_suffix = StringInput('Suffix')

        # Remove n
        self.vlayout_remove_n = QtWidgets.QVBoxLayout()
        self.lbl_remove_n = QtWidgets.QLabel('3 - Remove First/Last')
        self.remove_first_n = IntInput('First N')
        self.remove_last_n = IntInput('Last N')

        # Remove From To
        self.vlayout_remove_from_to = QtWidgets.QVBoxLayout()
        self.lbl_remove_from_to = QtWidgets.QLabel('4 - Remove From/To')
        self.remove_from = IntInput('From')
        self.remove_to = IntInput('To')

        # Remove Words
        self.vlayout_remove_word = QtWidgets.QVBoxLayout()
        self.lbl_remove_word = QtWidgets.QLabel('5 - Remove Word')
        self.remove_word = StringInput('Words')

        # Replace
        self.vlayout_replace = QtWidgets.QVBoxLayout()
        self.lbl_replace = QtWidgets.QLabel('6 - Replace')
        self.replace_target = StringInput('Replace')
        self.replace_with = StringInput('With')

        # Extension
        self.hlayout_extension = QtWidgets.QHBoxLayout()
        self.cbx_ignore_extension = QtWidgets.QCheckBox('Ignore Extension')
        self.cbx_ignore_extension.setChecked(True)

    def create_layout(self):
        # List Previews
        self.vlayout_preview_before.addWidget(self.scroll_preview_before)
        self.grp_preview_before.setLayout(self.vlayout_preview_before)
        self.vlayout_preview_after.addWidget(self.scroll_preview_after)
        self.grp_preview_after.setLayout(self.vlayout_preview_after)
        self.hlayout_lists.addWidget(self.grp_preview_before)
        self.hlayout_lists.addWidget(self.grp_preview_after)

        # Insert
        self.vlayout_insert.addWidget(self.lbl_insert)
        self.vlayout_insert.addLayout(self.insert_word)
        self.vlayout_insert.addLayout(self.insert_at_pos)

        # Add
        self.vlayout_add.addWidget(self.lbl_add)
        self.vlayout_add.addLayout(self.add_prefix)
        self.vlayout_add.addLayout(self.add_suffix)

        # Remove n
        self.vlayout_remove_n.addWidget(self.lbl_remove_n)
        self.vlayout_remove_n.addLayout(self.remove_first_n)
        self.vlayout_remove_n.addLayout(self.remove_last_n)

        # Remove From To
        self.vlayout_remove_from_to.addWidget(self.lbl_remove_from_to)
        self.vlayout_remove_from_to.addLayout(self.remove_from)
        self.vlayout_remove_from_to.addLayout(self.remove_to)

        # Remove Words
        self.vlayout_remove_word.addWidget(self.lbl_remove_word)
        self.vlayout_remove_word.addLayout(self.remove_word)
        self.vlayout_remove_word.addStretch()

        # Replace
        self.vlayout_replace.addWidget(self.lbl_replace)
        self.vlayout_replace.addLayout(self.replace_target)
        self.vlayout_replace.addLayout(self.replace_with)

        # Actions Row
        self.hlayout_actions.addLayout(self.vlayout_insert)
        self.hlayout_actions.addStretch()
        self.hlayout_actions.addLayout(self.vlayout_add)
        self.hlayout_actions.addStretch()
        self.hlayout_actions.addLayout(self.vlayout_remove_n)
        self.hlayout_actions.addStretch()
        self.hlayout_actions.addLayout(self.vlayout_remove_from_to)
        self.hlayout_actions.addStretch()
        self.hlayout_actions.addLayout(self.vlayout_remove_word)
        self.hlayout_actions.addStretch()
        self.hlayout_actions.addLayout(self.vlayout_replace)

        # Extension
        self.hlayout_extension.addStretch()
        self.hlayout_extension.addWidget(self.cbx_ignore_extension)

        # Main
        self.addLayout(self.hlayout_lists)
        self.addLayout(self.hlayout_actions)
        self.addStretch()
        self.addLayout(self.hlayout_extension)
        self.addStretch()

    def create_connections(self):
        self.insert_word.input.textChanged.connect(self._update_preview)
        self.insert_at_pos.input.valueChanged.connect(self._update_preview)

        self.add_prefix.input.textChanged.connect(self._update_preview)
        self.add_suffix.input.textChanged.connect(self._update_preview)

        self.remove_first_n.input.valueChanged.connect(self._update_preview)
        self.remove_last_n.input.valueChanged.connect(self._update_preview)

        self.remove_from.input.valueChanged.connect(self._update_preview)
        self.remove_to.input.valueChanged.connect(self._update_preview)

        self.remove_word.input.textChanged.connect(self._update_preview)

        self.replace_target.input.textChanged.connect(self._update_preview)
        self.replace_with.input.textChanged.connect(self._update_preview)

        self.cbx_ignore_extension.toggled.connect(self.cbx_ignore_extension_connection)

    def _update_preview(self):
        """Updates the 'After' column whenever an input is changed."""
        edited_list = []

        for i in range(self.list_before_preview.count()):
            edited_list.append(self.rename_string(self.list_before_preview.item(i).text()))

        self.list_after_preview.clear()
        self.list_after_preview.addItems(edited_list)

    def set_item_list(self, contents: list = None):
        """
        Fills the columns with values.

        Args:
            contents(list): The values to add to the columns.
        """
        if contents:
            items = contents
        else:
            items = []

        self.unedited_list = items

        self.list_before_preview.clear()
        self.list_before_preview.addItems(items)
        self.list_after_preview.clear()
        self.list_after_preview.addItems(items)

    def rename_string(self, string: str) -> str:
        """
        Will rename a given string using the inputs from the user.

        Args:
            string(str): The string to rename

        Returns:
            str: The renamed version of the string.
        """
        if self.cbx_ignore_extension.isChecked():
            start = string.split('.')[0]
            extension = string.split('.')[-1]
        else:
            start = string
            extension = ''

        if self.insert_word.value:
            inserted = insert_substring(start, self.insert_word.value, self.insert_at_pos.value)
        else:
            inserted = start

        if self.add_prefix.value or self.add_suffix.value:
            added_pre_sub = append_substring(inserted, self.add_prefix.value, self.add_suffix.value)
        else:
            added_pre_sub = inserted

        if self.remove_first_n.value or self.remove_last_n.value:
            removed_ends = remove_chars_from_ends(added_pre_sub, self.remove_first_n.value, self.remove_last_n.value)
        else:
            removed_ends = added_pre_sub

        if self.remove_to.value:
            removed_from_to = remove_from_to_position(removed_ends, self.remove_from.value, self.remove_to.value)
        else:
            removed_from_to = removed_ends

        if self.remove_word.value:
            removed_words = remove_substring(removed_from_to, self.remove_word.value)
        else:
            removed_words = removed_from_to

        if self.replace_target.value and self.replace_with.value:
            replaced = removed_words.replace(self.replace_target.value, self.replace_with.value)
        else:
            replaced = removed_words

        if extension:
            end = f'{replaced}.{extension}'
        else:
            end = replaced

        return end

    def get_new_names_all(self) -> list[tuple]:
        """
        Gets the original and new names of all items in the before list, as they are shown in the
        after list, using the user inputs.

        Returns:
            list[tuple]: A list of tuples containing (original_name, new_name)
        """
        name_changes = []

        for i in range(self.list_after_preview.count()):
            name_changes.append((self.list_before_preview.item(i).text(), self.rename_string(self.list_before_preview.item(i).text())))

        return name_changes

    def get_new_names_selected(self) -> list[tuple]:
        """
        Gets the original and new names of all selected items from the before list, as they are shown
        in the after list.

        Returns:
            list[tuple]: A list of tuples containing (original_name, new_name)
        """
        update_names = []

        for i in self.list_before_preview.selectedItems():
            update_names.append((i.text(), self.rename_string(i.text())))

        return update_names

    def cbx_ignore_extension_connection(self):
        """Updates the preview item's extension inclusion."""
        self.list_after_preview.clear()
        items = [self.rename_string(self.list_before_preview.item(i).text()) for i in
                 range(self.list_before_preview.count())]
        self.list_after_preview.addItems(items)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Standalone Batch Renamer
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class BatchRenamerStandalone(QtWidgets.QMainWindow):
    """A standalone batch rename window."""
    def __init__(self):
        super(BatchRenamerStandalone, self).__init__(parent=None)

        self.setMinimumHeight(850)
        self.setMinimumWidth(1000)

        self.items = []

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.setCentralWidget(self.main_widget)

    def create_widgets(self):
        # Main
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.main_layout)

        # Batch Renamer
        self.batch_renamer = BatchRenamer()

        # Directory
        self.selected_directory = QtWidgets.QLineEdit()
        self.btn_select_directory = QtWidgets.QPushButton('Open')
        self.hlayout_directory = QtWidgets.QHBoxLayout()

        # Rename Button
        self.hlayout_rename_button = QtWidgets.QHBoxLayout()
        self.btn_rename_selected = QtWidgets.QPushButton('Rename Selected')
        self.btn_rename_all = QtWidgets.QPushButton('Rename All')

    def create_layout(self):
        # Directory
        self.hlayout_directory.addWidget(self.btn_select_directory)
        self.hlayout_directory.addWidget(self.selected_directory)

        # Rename Button
        self.hlayout_rename_button.addStretch()
        self.hlayout_rename_button.addWidget(self.btn_rename_all)
        self.hlayout_rename_button.addWidget(self.btn_rename_selected)
        self.btn_rename_all.setFixedSize(150, 30)
        self.btn_rename_selected.setFixedSize(150, 30)

        # Main
        self.main_layout.addLayout(self.hlayout_directory)
        self.main_layout.addLayout(self.batch_renamer)
        self.main_layout.addLayout(self.hlayout_rename_button)

    def create_connections(self):
        self.btn_select_directory.clicked.connect(self.btn_select_directory_connection)
        self.btn_rename_selected.clicked.connect(self.btn_rename_selected_connection)
        self.btn_rename_all.clicked.connect(self.btn_rename_all_connection)

    def btn_select_directory_connection(self):
        """Sets self.selected_directory with the chosen path from a QFileDialog."""
        directory = Path(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.selected_directory.setText(directory.as_posix())
        self.create_list_items(directory)

    def create_list_items(self, directory: Path):
        """Creates the item lists to send to the renamer component."""
        items = []
        files = lucid.io_utils.list_folder_contents(directory, True)
        for f in files:
            if not f.is_dir():
                items.append(f.name)

        self.batch_renamer.set_item_list(items)

    def btn_rename_selected_connection(self):
        """
        Renames the files selected in the Before column, with their
        corresponding values in the After column.
        """
        new_names = self.batch_renamer.get_new_names_selected()
        base_path = Path(self.selected_directory.text())

        for i in new_names:
            original_path = Path(base_path, i[0])
            new_path = Path(base_path, i[1])
            os.rename(original_path, new_path)

        self.batch_renamer.set_item_list(lucid.io_utils.list_folder_contents(base_path))

    def btn_rename_all_connection(self):
        """
        Renames all files in the Before column with their corresponding
        values in the After column.
        """
        new_names = self.batch_renamer.get_new_names_all()
        base_path = Path(self.selected_directory.text())

        for i in new_names:
            original_path = Path(base_path, i[0])
            new_path = Path(base_path, i[1])
            os.rename(original_path, new_path)

        self.batch_renamer.set_item_list(lucid.io_utils.list_folder_contents(base_path))


def main():
    """Runs the standalone Batch Renamer."""
    app = QtWidgets.QApplication(sys.argv)
    window = BatchRenamerStandalone()
    window.show()

    qss_path = Path(lucid.constants.RESOURCE_PATH, 'Combinear.qss')
    with open(qss_path, 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    app.exec_()


if __name__ == '__main__':
    main()

"""
# Environment Combo Box

* Description

    A simple row widget with a label and a combo box.

* Update History

    `2024-02-14` - Init
"""


from PySide2 import QtWidgets


class EnvironmentComboBox(QtWidgets.QWidget):
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

        self.layout_main = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout_main)

        self.lbl_name = QtWidgets.QLabel(self.row_name)
        self.cmb_combobox = QtWidgets.QComboBox()
        self.cmb_combobox.addItems(contents)
        self.btn_add = QtWidgets.QPushButton('+')
        self.btn_add.setFixedSize(20, 20)

        self.layout_main.addWidget(self.lbl_name)
        self.layout_main.addWidget(self.cmb_combobox)

        self.cmb_combobox.activated.connect(self.update_parent)

        if addable:
            self.layout_main.addWidget(self.btn_add)
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

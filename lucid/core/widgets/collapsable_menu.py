"""
# Collapsable Menu

* Description:

    A group box with checkbox by label that sets if the item is expanded or
    not. Unchecking the box will recursively hide all contents.
"""


from typing import Optional

from PySide2 import QtWidgets

from lucid.core.widgets.group_box import GroupBox


class CollapsableMenu(GroupBox):
    def __init__(self,
                 label: str,
                 horizontal: bool = False,
                 default_checked: bool = True) -> None:
        super().__init__(label, horizontal)
        self.setCheckable(True)
        self.setChecked(default_checked)
        self.toggled.connect(self.toggle)
        self.toggle(default_checked)

    def toggle(self,
               expanded: bool,
               layout: Optional[QtWidgets.QLayout] = None) -> None:
        """Recursively sets the visibility of items in the layout."""
        if layout is None:
            layout = self.layout

        for i in range(layout.count()):
            item = layout.itemAt(i)

            widget = item.widget()
            if widget is not None:
                widget.setVisible(expanded)
                continue

            child_layout = item.layout()
            if child_layout is not None:
                self.collapse(expanded, child_layout)

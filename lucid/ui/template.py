"""Some simple templates to copy + paste to start UI based tools."""

"""
# Module Name

* Description

    Lorem Ipsum

* Update History

    `2023-09-23` - Init
"""



from PySide2 import QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(self)

        self.create_widgets()
        self.create_layout()
        self.create_connetions()

    def create_widgets(self):
        pass

    def create_layout(self):
        self.layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout_main)

    def create_connections(self):
        pass


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(self)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.layout_main)
        self.setCentralWidget(self.main_widget)

    def create_layout(self):
        pass

    def create_connections(self):
        pass

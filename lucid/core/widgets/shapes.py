"""
# Qt Basic Shapes

* Description:

    Basic shape library to eliminate boilerplate.
"""


from PySide2 import QtWidgets


def create_horizontal_line(sunken: bool = True) -> QtWidgets.QFrame:
    """Creates a horizontal line.

    Args:
        sunken(bool): If the line should sink inwards into the frame.
    Returns:
        QtWidgets.QFrame: The line widget as a QFrame.
    """
    line = QtWidgets.QFrame()
    line.setFrameShape(QtWidgets.QFrame.HLine)
    if sunken:
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
    return line


def create_vertical_line(sunken: bool = True) -> QtWidgets.QFrame:
    """Creates a vertical line.

    Args:
        sunken(bool): If the line should sink inwards into the frame.
    Returns:
        QtWidgets.QFrame: The line widget as a QFrame.
    """
    line = QtWidgets.QFrame()
    line.setFrameShape(QtWidgets.QFrame.VLine)
    if sunken:
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
    return line

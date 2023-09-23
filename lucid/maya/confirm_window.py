"""
# Maya Confirm Windows

* Description

    A warning, generic info, and critical warning dialog box for Maya.

* Update History

    `2023-09-22` - Init
"""


import maya.cmds as cmds


def warning(message: str) -> str:
    """
    A Maya warning dialog box with Yes/No buttons.

    Args:
        message (str): The message to display in the dialog box.

    Returns:
        str: The selected option
    """
    answer = cmds.confirmDialog(
            title='Confirm',
            icon='warning',
            message=message,
            messageAlign='center',
            button = ['Yes', 'No'],
            defaultButton='No',
            cancelButton='No',
            dismissString='No'
    )

    return answer


def info(message: str):
    """
    A Maya warning dialog box with a single 'Okay' button.

    Args:
        message (str): The message to display in the dialog box.

    Returns:
        str: The selected options
    """
    answer = cmds.confirmDialog(
            title='Confirm',
            icon='information',
            message=message,
            messageAlign='center',
            button = ['Okay'],
            defaultButton='Okay',
            cancelButton='Okay',
            dismissString='Okay'
    )

    return answer


def critical(message: str):
    """
    A Maya warning dialog box with Yes/No buttons.

    Args:
        message (str): The message to display in the dialog box.

    Returns:
        str: The selected options
    """
    answer = cmds.confirmDialog(
            title='CRITICAL',
            icon='critical',
            message=message,
            messageAlign='center',
            button = ['Okay'],
            defaultButton='Okay',
            cancelButton='Okay',
            dismissString='Okay'
    )

    return answer

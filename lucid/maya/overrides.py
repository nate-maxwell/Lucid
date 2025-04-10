"""
# Maya Overrides

* Description:

    This module contains replacement commands that override the built-in maya
    commands. This is usually intended to inject extra instructions before
    executing the normal maya command, and in rare cases, outright replace the
    built-in maya command.

* Notes:

    Some function signatures will contain an unused *args. This is because Maya
    consistently calls functions with arguments we do not care about.
"""


# noinspection PyUnresolvedReferences
from maya import cmds

from lucid.system.subsystems import context


def new_file_override(*args) -> None:
    """
    Overrides Maya's new file command, injecting custom instructions
    before opening a new file.
    """
    print('[MYTHOS][MAYA] New file override executed.')
    print("Please, 'untitled document' was my father, call me 'untitled document (1)'")
    context.reset_context()


def enable_overrides() -> None:
    """Enables all custom overrides. This func is called in userSetup."""
    print('--------------------------------------------------')

    print('[LUCID][MAYA] Function overrides enabled.')
    print()

    cmds.scriptJob(e=["NewSceneOpened", new_file_override])
    print('[LUCID][MAYA] "NewSceneOpened" Override enabled.')

    print('--------------------------------------------------')

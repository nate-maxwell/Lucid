"""
# Maya Initialization

* Description:

    This file is initialized by Maya on startup. It is intentionally placed in a
    folder on its own (and without an __init__.py), since we're manually adding
    this folder to the PYTHONPATH environment variable when launching Maya.
"""


# noinspection PyUnresolvedReferences
import maya.cmds

import lucid.maya.file_io


# We have to include `lowestPriority=True` (and hence use
# `maya.cmds.evalDeferred` rather than `maya.utils.executeDeferred`), otherwise
# maya crashes on launch. This is possibly due to Maya's main window and / or
# shiboken not yet being ready.

# ----------Maya Session Setters-------------------------------------------------------------------
maya.cmds.evalDeferred(lucid.maya.open_command_port, lowestPriority=True)

# ----------Register Event Subscribers-------------------------------------------------------------
# ...


# Maya-charm Plugin
try:
    if not maya.cmds.commandPort(":4434", query=True):
        maya.cmds.commandPort(name=":4434")
except RuntimeError:
    pass

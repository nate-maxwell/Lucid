"""
# Launch

* Description

    The primary launch procedures for lucid.

* Update History

    `2023-09-19` - Init
"""


import os
import subprocess

import lucid.constants


def launch_maya():
    """Set environment vars and launch Maya."""
    # Set Maya's libraries before ours to prevent a crash.
    env = os.environ.copy()
    env['PYTHONPATH'] = ';'.join([
        lucid.constants.MAYA_SITE_PACKAGES.as_posix(),
        lucid.constants.LUCID_PATH.parent.as_posix(),
        lucid.constants.MAYA_USER_SETUP_PATH.as_posix()
    ])

    executable = lucid.constants.MAYA_EXEC
    subprocess.Popen(executable, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)


def launch_unreal():
    env = os.environ.copy()
    env['PYTHONPATH'] = ';'.join([
        lucid.constants.LUCID_PATH.parent.as_posix(),
        lucid.constants.LUCID_UNREAL_PATH.as_posix()
    ])

    executable = lucid.constants.UNREAL_EXEC
    subprocess.Popen(executable, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)


def launch_painter():
    pass


def launch_designer():
    pass

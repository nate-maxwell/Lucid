"""
# Launch

* Description

    The primary launch procedures for lucid.

* Update History

    `2023-09-19` - Init
"""


import os
import subprocess
from pathlib import Path

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
    """Sets environment vars and launch Unreal."""
    env = os.environ.copy()
    env['PYTHONPATH'] = ';'.join([
        lucid.constants.LUCID_PATH.parent.as_posix(),
        lucid.constants.LUCID_UNREAL_PATH.as_posix(),
        lucid.constants.VENV_SITE_PACKAGES.as_posix()
    ])

    executable = lucid.constants.UNREAL_EXEC
    subprocess.Popen(executable, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)


def launch_painter():
    raise NotImplementedError


def launch_designer():
    raise NotImplementedError


def launch_project_manager():
    raise NotImplementedError


def launch_pipeline_settings():
    window_path = Path(lucid.constants.LUCID_PATH, 'pipeline_settings.py')

    cmd = f'{lucid.constants.PYTHON_EXEC_PATH} {window_path}'
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    subprocess.Popen(cmd, startupinfo=startupinfo)


def launch_renamer():
    window_path = Path(lucid.constants.LUCID_PATH, 'rename.py')

    cmd = f'{lucid.constants.PYTHON_EXEC_PATH} {window_path}'
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    subprocess.Popen(cmd, startupinfo=startupinfo)

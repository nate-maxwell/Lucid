"""
# Launch

* Description:

    Primary launch procedures for standalone applications and DCCs within the
    lucid pipeline.

    This will load all necessary tools into the program and set any necessary
    environment variables.
"""


import os
import subprocess
from pathlib import Path

from lucid.core import const
from lucid.core import exceptions
from lucid.core.config import Config


def _launch_program(exe: Path, env: dict) -> None:
    """Launches the exe passing in the env.
    Will log any exception raised.
    """
    with exceptions.log_exceptions(f'[Launch :: {exe.stem}]'):
        print(f'Launching: {exe.as_posix()}')
        flag = subprocess.CREATE_NEW_CONSOLE
        subprocess.Popen(exe, env=env, creationflags=flag)


# ----------DCCs---------------------------------------------------------------

def launch_maya(project: str) -> None:
    env = os.environ.copy()
    lucid_env = {
        'PYTHONPATH': ';'.join([
            # Set Maya's libraries before ours to prevent crash.
            Config.applications.MAYA_SITE_PACKAGES.as_posix(),

            const.LUCID_REPO_DIR.as_posix(),
            Config.applications.MAYA_USER_SETUP_DIR.as_posix(),
            const.VENV_SITE_PACKAGES_DIR.as_posix()
        ]),
        const.ENV_PROJECT: project
    }

    env.update(lucid_env)
    executable = Config.applications.MAYA_EXEC
    if executable == const.UNASSIGNED:
        return
    _launch_program(executable, env=env)


def launch_painter(project: str) -> None:
    env = os.environ.copy()
    lucid_env = {
        'PYTHONPATH': ';'.join([
            const.LUCID_REPO_DIR.as_posix(),
            const.VENV_SITE_PACKAGES_DIR.as_posix()
        ]),
        const.ENV_PROJECT: project
    }
    plugin_path = Config.applications.PAINTER_PLUGINS_DIR.as_posix()
    lucid_env['SUBSTANCE_PAINTER_PLUGINS_PATH'] = plugin_path
    env.update(lucid_env)

    executable = Config.applications.PAINTER_EXEC
    if executable == const.UNASSIGNED:
        return
    _launch_program(executable, env=env)


def launch_designer(project: str) -> None:
    env = os.environ.copy()
    lucid_env = {
        'PYTHONPATH': ';'.join([
            const.LUCID_REPO_DIR.as_posix(),
            const.VENV_SITE_PACKAGES_DIR.as_posix()
        ]),
        const.ENV_PROJECT: project
    }
    env.update(lucid_env)

    executable = Config.applications.DESIGNER_EXEC
    if executable == const.UNASSIGNED:
        return
    _launch_program(executable, env=env)


def launch_unreal(project: str) -> None:
    env = os.environ.copy()
    lucid_env = {
        'PYTHONPATH': ';'.join([
            const.LUCID_REPO_DIR.as_posix(),
            Config.applications.LUCID_UE_DIR.as_posix(),
            const.VENV_SITE_PACKAGES_DIR.as_posix()
        ]),
        const.ENV_PROJECT: project
    }

    env.update(lucid_env)
    executable = Config.applications.UNREAL_EXEC
    if executable == const.UNASSIGNED:
        return
    _launch_program(executable, env=env)


# ----------Qt Applications----------------------------------------------------

def _launch_qt_app(app_path: Path) -> None:
    cmd = f'{const.PYTHON_EXEC} {app_path.as_posix()}'
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    env = os.environ.copy()
    env['PYTHONPATH'] = const.LUCID_REPO_DIR.as_posix()

    subprocess.Popen(cmd, env=env, startupinfo=startupinfo)


def launch_user_settings() -> None:
    path = Path(Path(__file__).parent, 'user_settings.py')
    _launch_qt_app(path)

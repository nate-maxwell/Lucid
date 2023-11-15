"""
# Lucid Debug Library

* Description:

    A small library of debug functions that can be tied to the Lucid shelf, or ran
    independently.

* Update History:

    `2023-11-09` - Init
"""


import os
from pathlib import Path

import lucid.io_utils
import lucid.constants


def print_environ_vars(prefix: str = '') -> None:
    """
    Prints the current os environment vars.

    Args:
        prefix(Str): An optional argument that will filter the vars that get
        printed to those that start with the given prefix.
    """
    for k, v in os.environ.items():
        if k.startswith(prefix):
            print(f'{k}:: {v}')


def save_environment_log_to_drive(prefix: str = '') -> None:
    """
    Saves the user's environment variables to disk in V:/pipeline/logs/<username>.

    Args:
        prefix(Str): An optional argument that will filter the vars that get
        saved to those that start with the given prefix.
    """
    data = {}
    for k, v in os.environ.items():
        if k.startswith(prefix):
            data[k] = v

    time = lucid.io_utils.get_time().replace(':', '.')
    log_name = f'{lucid.constants.USER}_log_{lucid.io_utils.get_date()}_{time}.json'
    project = os.environ[lucid.constants.ENV_PROJECT]
    path = Path(lucid.constants.PROJECTS_PATH, project, 'user_data', log_name)

    lucid.io_utils.create_folder(path.parent)
    lucid.io_utils.export_data_to_json(path, data)
    print(path)

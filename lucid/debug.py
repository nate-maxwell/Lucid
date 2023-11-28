"""
# Lucid Debug Library

* Description:

    A small library of debug functions that can be tied to the Lucid shelf, or ran
    independently.

* Update History:

    `2023-11-09` - Init
"""


import os
import time
from pathlib import Path
from typing import Callable

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

    log_time = lucid.io_utils.get_time().replace(':', '.')
    log_name = f'{lucid.constants.USER}_log_{lucid.io_utils.get_date()}_{log_time}.json'
    project = os.environ[lucid.constants.ENV_PROJECT]
    path = Path(lucid.constants.PROJECTS_PATH, project, 'user_data', log_name)

    lucid.io_utils.create_folder(path.parent)
    lucid.io_utils.export_data_to_json(path, data)
    print(path)


def timer(func: Callable):
    """Decorator to print the time it takes to execute a function."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        print(f'Function took: {time.perf_counter() - start} seconds.')

    return wrapper


def print_func_name(func: Callable):
    """
    Decorator to print the name of the decorated function.
    If multiple decorators are used, place this one at the
    bottom of the decorator stack.
    """
    def wrapper(*args, **kwargs):
        print(func.__name__)
        func(*args, **kwargs)

    return wrapper


def print_name_and_exec_time(func: Callable):
    @timer
    def wrapper(*args, **kwargs):
        print(func.__name__)
        func(*args, **kwargs)

    return wrapper

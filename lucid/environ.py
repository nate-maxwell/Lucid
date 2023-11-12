"""
# Lucid  environment variable helper library

* Update History:

    `2023-11-09` - Init
"""


import os
from typing import Union


def update_environ_var(var_name: str, values: list[str]) -> list[str]:
    """
    Updates the environment variable of the given variable name using the dict.update() method.

    Args:
        var_name(str): the name of the variable adding to the environment.
        Will get converted to uppercase.

        values(list[str]): a list of strings to update the environ var.

    Returns:
        list[str]: the list of string entries in the variable that was updated.
    """
    if values:
        new_values = values
    else:
        new_values = []

    key = var_name.upper()

    update = {
        key: ';'.join(new_values)
    }

    env = os.environ
    env.update(update)

    return os.environ.copy()[key].split(';')


def get_environ_var_as_list(var_name: str) -> Union[list[str], None]:
    """
    Will return a list[str] of the contents of the input environment variable.

    Args:
        var_name(str): the environment variable name to fetch.
        Will get converted to uppercase.

    Returns:
        Union[list[str], None]: The list of values in the environment variable, or None
        if key does not exist.
    """
    env = os.environ.copy()
    key = var_name.upper()

    if key not in env:
        return None

    return os.environ[key].split(';')
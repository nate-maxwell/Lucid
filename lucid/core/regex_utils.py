"""
Pipeline Regex Utility Library

A collection of regex and other substring parsing utility functions.
"""


import os
import re
from typing import Optional


_version_padding = 3


def get_file_version_number(file_name: str) -> Optional[str]:
    """
    Gets the integer version number of a file whose name
    ends with the standard version suffix: '_v###.ext',
    if it exists, otherwise returns None.

    Example file name: 'GhostA_anim_v001.ma'

    The suffix's number padding can be any length.

    Args:
        file_name (str): The file name to search.

    Returns:
        int: The integer version number.
    """
    temp = re.search(r'_v(\d*)\..*$', file_name)
    return temp.group(1) if temp else None


def get_file_version_suffix(file_name: str, with_underscore_v: bool = True) -> Optional[str]:
    """
    Given a filename of GhostA_anim_v001.fbx, will return either
    '001' or '_v001'.
    The digit padding is gotten from the show config using the ENV_SHOW environment var.

    Args:
        file_name(str): The name to get the suffix from.

        with_underscore_v(bool) Whether to add '_v' before the padded version number.
        Defaults to True.

    Returns:
        Optional[str]: Will return the generated '###' or '_v###' string if the ENV_SHOW
        value has been set. Otherwise, will return None if no show is set.
    """
    if not _version_padding:
        return None

    ver_num = get_file_version_number(file_name)
    if ver_num is None:
        return None

    padded_ver_num = str(ver_num).zfill(_version_padding)

    if with_underscore_v:
        return f'_v{padded_ver_num}'
    else:
        return padded_ver_num


def is_path_like(value: str) -> bool:
    """Heuristically determine if a string looks like a Windows file or directory path.

    Args:
        value (str): The string to evaluate.
    Returns:
        bool: True if the string looks like a path, False otherwise.
    """
    if not isinstance(value, str):
        return False

    # Check for Windows drive-letter root (e.g. C:\ or D:/)
    if re.match(r'^[a-zA-Z]:[\\/]', value):
        return True

    # Check for UNC path (e.g. \\server\share)
    if value.startswith('\\\\'):
        return True

    # Relative Windows-style path (starts with .\ or ..\)
    if value.startswith(('.\\', '..\\')):
        return True

    # Contains backslashes or forward slashes
    if '\\' in value or '/' in value:
        return True

    # Looks like a filename with an extension
    _, ext = os.path.splitext(value)
    if ext and 1 < len(ext) <= 6:
        return True

    return False


def pascale_to_snake(s: str) -> str:
    """Converts a PascalCase string to snake_case.

        Args:
            s (str): The PascalCase string.
        Returns:
            str: The snake_case version of the string.
        """
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    snake = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
    return snake.lower()

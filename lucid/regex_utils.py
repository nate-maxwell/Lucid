"""
Pipeline Regex Utility Library

A collection of regex and other substring parsing utility functions.
"""


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

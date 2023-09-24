"""
Legex, Lucid Regex

* Descriptions

    Legex is the Lucid regex helper library for common regex functions
    used within the lucid pipeline.

* Update History

    `2023-09-23` - Init
"""


import re
from typing import Optional


def get_trailing_numbers(s: str) -> Optional[str]:
    """
    Gets the integer from the end of a string.

    Args:
        s (str): The string the search.

    Returns:
        int: The integer at the end of the string if one exists.
        Returns None if no integer exists.
    """
    temp = re.search('\d+$', s)
    return int(temp.group()) if temp else None


def get_file_version_number(file_name: str) -> Optional[int]:
    """
    Gets the integer version number of a file whose name
    ends with the standard mythos version suffix: '_v###.ext',
    if it exists, otherwise returns None.

    Example file name: 'GhostA_anim_v001.ma'

    The suffix's number padding can be any length.

    Args:
        file_name (str): The file name to search.

    Returns:
        int: The integer version number.
    """
    temp = re.search('_v(\d*)\..*$', file_name)
    return int(temp.group(1)) if temp else None

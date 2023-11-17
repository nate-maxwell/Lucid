"""
Legex, Lucid Regex

* Descriptions

    Legex is the Lucid regex helper library for common regex functions
    used within the lucid pipeline.

* Update History

    `2023-09-23` - Init

    `2023-09-26` - Fixed bug with get_trailing_numbers

    `2023-11-16` - Added version_up_filename(str, int) to reduce complexity in
    file publishers.
"""


import re
from typing import Optional
from pathlib import Path


PADDING_NUM = 3


def get_trailing_numbers(s: str) -> Optional[int]:
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
    ends with the standard lucid version suffix: '_v###.ext',
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


def get_lucid_file_version_suffix(file_name: str, with_underscore_v: bool = True) -> Optional[str]:
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
    ver_num = get_file_version_number(file_name)
    padded_ver_num = str(ver_num).zfill(PADDING_NUM)

    if with_underscore_v:
        return f'_v{padded_ver_num}'
    else:
        return padded_ver_num


def validation_no_special_chars(string: str) -> bool:
    """
    Checks a string to see if it contains non-alpha-numeric or non-underscore characters.
    Will return True if the string contains no special characters. Will return False
    if the string contains special characters or is an empty string.

    Args:
        string (str): The string to check against.

    Returns:
        bool: Whether the string contains no special characters.

    Notes:
        A common gotcha is that whitespace counts as a special character.
    """
    m = re.match("^[a-zA-Z0-9_]*$", string)
    if m and string != '':
        return True
    else:
        return False


def version_up_filename(filename_w_ext: str, ver_padding: int) -> Optional[str]:
    """
    Versions up a file name from (filename_v002.ext, 3) -> filename_v003.ext

    Args:
        filename_w_ext(str): String filename with extension: filename.ext

        ver_padding(int): How many digits to pad the version number.

    Returns:
        Optional[str]: New string name for the versioned up filename or None
        if an incorrect entry was entered.
    """
    if '.' not in filename_w_ext:
        return None

    source_path = Path(filename_w_ext)
    ext = source_path.suffix

    cur_ver_suffix = get_lucid_file_version_suffix(source_path.name)
    if cur_ver_suffix:
        base_name = source_path.stem.split(cur_ver_suffix)[0]
        cur_ver_num = int(cur_ver_suffix.split('_v')[-1])
        next_ver_suffix = f'v{str(cur_ver_num + 1).zfill(ver_padding)}'  # 3 -> 'v004'
    else:
        base_name = source_path.stem
        next_ver_suffix = f"v{'1'.zfill(ver_padding)}"

    return f'{base_name}_{next_ver_suffix}{ext}'


foo = 'GhostA_anim_v003.fbx'
print(version_up_filename(foo, 3))

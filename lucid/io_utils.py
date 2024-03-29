"""
# IO Utilities
03.11.23

* Description

    Library of helper functions based for Windows OS based directories.

* Notes

    This library is meant to be treated as a pseudo 'pure library', meaning that it is
    entirely written with built-int python libraries and no function in this library is
    dependent on another function that exists outside the built-ins or this library.

    Currently, the one exception is that there is a single safety constant at the top of
    the file to keep users from deleting from folders they do not have permissions for.
    I am still pondering a practical fix for this. Maybe this will eventually move
    away from being as self-contained as it is.

* Update History

    `2023-09-19` - Init

    `2023-09-23` - Fixed bug with create_folder, get_next_version_from_dir, and copy_file.

    `2023-11-20` - copy_folder_contents now copies into existing trees.
"""


import datetime
import json
import math
import os
import platform
import re
import shutil
from pathlib import Path
from typing import Optional
from typing import Union

import lucid.config_paths


def list_folder_contents(folder_path: Path, full_path: bool = False) -> Union[list[Path], list[str], None]:
    """
    Lists the contents, or full path for contents, of a folder.

    Args:
        folder_path (pathlib.Path): Folder path to list contents of.

        full_path (bool): To return string names or paths of folder contents. Defaults to False.

    Returns:
        String names of folder contents if full_path = False,
        Paths for folder contents if full_path = True.
    """
    if folder_path.exists():
        if full_path:
            contents = list(folder_path.glob('*'))
        else:
            contents = os.listdir(folder_path)

        return contents

    return None


def create_folder(folder_path: Path) -> Path:
    """
    Creates a folder from the given path.

    Args:
        folder_path (path): The folder path for the folder to create.

    Returns:
        Path: The created, or pre-existing, folder path.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def create_dated_folder(folder_path: Path) -> Path:
    """
    Creates a folder with today's date as the name.

    Args:
        folder_path (Path): The path, with base folder name, to place the folder.

    Returns:
        str: The full path of the created folder with date.
    """
    date_path = Path(folder_path, get_date())
    create_folder(date_path)

    return date_path


def delete_folder(folder_path: Path) -> None:
    """
    Removes folder path from V:/shows/ downward.

    Args:
        folder_path (Path): the path to the folder to delete. Will throw exception if
        path does not start with lucid.config.PROJECTS_PATH.
    """
    if lucid.config_paths.PROJECTS_PATH in list(folder_path.parents):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                filename = Path(root, name)
                os.remove(filename)
            for name in dirs:
                os.rmdir(Path(root, name))

        os.rmdir(folder_path)
    else:
        raise ValueError(f'Path must be within {lucid.config_paths.PROJECTS_PATH.as_posix()}')


def delete_file(filepath: Path) -> None:
    """
    Removes specified file from V:/shows/.

    Args:
        filepath (Path): the path to the file to delete. Will throw exception if
        path does not start with lucid.config.PROJECTS_PATH.
    """
    if lucid.config_paths.PROJECTS_PATH in list(filepath.parents):
        os.remove(filepath)
    else:
        raise ValueError(f'Path must be within {lucid.config_paths.PROJECTS_PATH.as_posix()}')


def copy_file(source: Path, destination: Path, new_name: Optional[str] = None) -> None:
    """
    Copy file into destination folder.

    Args:
        source (Path): full path of the file to copy.

        destination (Path): folder path of where to copy the file to.

        new_name (Optional[str]): new name for the file.
    """
    if new_name:
        if '.' in new_name:
            new_base_name = new_name.split('.')[0]
        else:
            new_base_name = new_name

        ext = source.suffix
        replace_name = f'{new_base_name}{ext}'
        target = Path(source.parent, replace_name)
    else:
        target = destination

    if source.parent == destination:
        if source.is_dir():
            return
    else:
        create_folder(destination)

    shutil.copy(source, target)


def copy_folder_contents(source: Path, destination: Path) -> None:
    """
    Copy contents of a folder to the given destination.

    Args:
        source (Path): folder path to the folder that is to be copied.

        destination (Path): folder path to copy the folder + contents to.
    """
    shutil.copytree(source, destination, dirs_exist_ok=True)


def get_date() -> str:
    """Returns str: 'YYYYMMDD'"""
    today = datetime.date.today()
    return today.strftime("%Y%m%d")


def get_time() -> str:
    """Returns str: 'HH:MM:SS:XX', X is microsecond."""
    return datetime.datetime.now().time().isoformat()[:-4]


def get_os_info() -> tuple[str, str, str]:
    """Returns tuple[str, str, str]: OS name, release number, and version number."""
    return platform.system(), platform.release(), platform.version()


def export_data_to_json(path: Path, data, overwrite: bool = False) -> None:
    """
    Export dict to json file path.

    Args:
        path (Path): the file path to place the .json file.

        data (dict|list): the data to export into the .json file.

        overwrite(bool): to overwrite json file if it already exists in path.
            Defaults to False.
    """
    if not path.exists() or overwrite:
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4)
    else:
        return


def import_data_from_json(filepath: Path) -> Optional[dict]:
    """
    Import data from a .json file.

    Args:
        filepath (Path): the filepath to the json file to extract data from.

    Returns:
        any: will return data if json file exists, None if it doesn't.
    """
    if filepath.exists():
        with open(filepath) as f:
            return json.load(f)
    else:
        return None


def get_next_version_from_dir(filepath: Path, extension: str, substring: str = None, padding: int = 3) -> str:
    """
    Gets the string representation of the latest version number of versioned files in a path.

    Args:
        filepath(Path): The folder to search.

        extension(str): The file extension to search against.

        substring(str): An optional substring the file name must contain. Defaults to None.

        padding(int): The number of digits to make the version number,
        defaults to 3.

    Returns:
        str: Will return the string representation of the version number (e.g. '005').
        Will return '001' if there is no version '001' within the folder.
    """
    ext = extension
    if not extension.startswith('.'):
        ext = f'.{extension}'

    contents = list_folder_contents(filepath)
    latest = None

    if contents:
        if substring:
            for file in contents:
                if file.endswith(ext) and substring in file:
                    if file.split('.')[0][-1].isnumeric():
                        latest = file
        else:
            for file in contents:
                if file.endswith(ext):
                    if file.split('.')[0][-1].isnumeric():
                        latest = file

    if latest:
        current_version = re.search('_v(\d*)\..*$', latest)
        if current_version:
            return str(int(current_version.group(1)) + 1).zfill(padding)
        else:
            return '1'.zfill(padding)
    else:
        return '1'.zfill(padding)


def user_data_dir(appname: str, app_author: str = None, version: str = None, roaming: bool = False) -> Path:
    """
    Returns a windows full path to the user-specific data dir for this application.

    Typical user data directories are:
        roaming: C:/Users/<username>>/AppData/Roaming/<AppAuthor>/<AppName>
        not roaming: C:/Users/<username>>/AppData/Local/<AppAuthor>/<AppName>

    Args:
        appname (str): The name of the application. If None, just the system directory is returned.

        app_author (str): Only used on Windows, is the name fo teh application author or distributing
        body for the application. Typically, it is the owning company name. This falls back to
        appname. Defaults to None, and will be disabled if is None.

        version (str): An optional version path element to append to the path. You might want to use this if
        you want multiple versions of your app to be able to run independently. If used, this would typically be
        '<major>.<minor>'. Defaults to None, and will be disabled if is None.

        roaming (bool): can be set True to use the Windows roaming appdata directory. This means that for users
        on a Windows network setup for roaming profiles, this user data will be sync'd on login. See
        <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx> for a discussion of issues.

    Returns:
        Path: The user's data path for this application.
    """
    if roaming:
        base_path = Path(os.getenv('APPDATA'))
    else:
        base_path = Path(os.getenv('LOCALAPPDATA'))

    if app_author:
        app_path = Path(base_path, app_author, appname)
    else:
        app_path = Path(base_path, appname)

    if version:
        path = Path(app_path, version)
    else:
        path = app_path

    return path


def convert_size(size_bytes: int) -> tuple[float, str]:
    """
    Converts pure byte count to commonly named size.
    Will convert to the most concise number, e.g.
    1.1 GB, not 1100 MB.

    Args:
        size_bytes(int): How many bytes to rename.

    Returns:
        tuple[float, str]: The new unit size and the new
        unit label.
    """
    if size_bytes == 0:
        return 0, 'B'
    size_name: list[str] = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return s, size_name[i]

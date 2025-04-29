"""
# IO Utilities

* Description:

    Various IO utilities and namespace shorteners.
"""


import datetime
import json
import math
import os
import platform
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Sequence
from typing import Union

from lucid import const


CHECK_PATH = Path('does/not/exist')  # TODO: make this configurable


def list_folder_contents(path: Path, full_path: bool = False) -> Union[list[Path], list[str], None]:
    """
    Lists the contents, or full path for contents, of a folder.

    Args:
        path (pathlib.Path): Folder path to list contents of.

        full_path (bool): To return string names or paths of folder contents. Defaults to False.

    Returns:
        String names of folder contents if full_path = False,
        Paths for folder contents if full_path = True.
    """
    if path.exists():
        if full_path:
            contents = list(path.glob('*'))
        else:
            contents = os.listdir(path)
        return contents

    return None


def create_folder(path: Path) -> Path:
    """
    Creates a folder from the given path.

    Args:
        path (path): The folder path for the folder to create.

    Returns:
        str: The created, or pre-existing, folder path.
    """
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def create_dated_folder(path: Path) -> Path:
    """
    Creates a folder with today's date as the name.

    Args:
        path (str): The path, with base folder name, to place the folder.

    Returns:
        str: The full path of the created folder with date.
    """
    date_path = Path(path, get_date())
    create_folder(date_path)

    return date_path


def delete_folder(path: Path) -> None:
    """
    Removes folder path from V:/shows/ downward, or linux equivalent if on linux.

    Args:
        path (Path): the path to the folder to delete. Will throw exception if
            path does not start with 'V:/shows/', or linux equivalent if on linux.
    """
    if CHECK_PATH in list(path.parents):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.remove(filename)
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(path)
    else:
        raise ValueError(f'Path must be within {CHECK_PATH.as_posix()}!')


def delete_file(filepath: Path) -> None:
    """
    Removes specified file from V:/shows/, or linux equivalent if on linux.

    Args:
        filepath (Path): the path to the file to delete. Will throw exception if
            path does not start with 'V:/shows/', or linux equivalent if on linux.
    """
    if CHECK_PATH in list(filepath.parents):
        os.remove(filepath)
    else:
        raise ValueError(f'Path must be within {CHECK_PATH.as_posix()}')


def delete_files_in_directory(directory_path: Path) -> None:
    """
    Delete all files in a directory.

    Args:
        directory_path (Path): Path to the directory.
    """
    try:
        files = Path.iterdir(directory_path)
        for file in files:
            file_path = Path(directory_path, file)
            delete_file(filepath=file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


def copy_file(source: Path, destination: Path, new_name: Optional[str] = '') -> None:
    """
    Copy file into a separate destination folder.

    Args:
        source (Path): file path of the file to copy.

        destination (Path): folder path of where to copy the file to.

        new_name (Optional[str]): an optional argument to rename the file.
    """
    if destination.suffix:
        create_folder(destination.parent)
    else:
        create_folder(destination)

    if source.parent == destination:
        if source.is_dir():
            return
        else:
            if '.' in new_name and not new_name.split('.')[-1].isnumeric():
                new_base_name = os.path.splitext(new_name)[0]
            else:
                new_base_name = new_name

            ext = source.name.split('.')[-1]
            replace_name = f'{new_base_name}.{ext}'
            shutil.copy(source, Path(source.parent, replace_name))
    else:
        if new_name:
            target = Path(destination, new_name)
        else:
            target = destination

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
    now = datetime.datetime.now().time().isoformat()[:-4]
    return now


def get_os_info() -> tuple[str, str, str]:
    """Returns tuple[str, str, str]: OS name, release number, and version number."""
    system  = platform.system()
    release = platform.release()
    version = platform.version()
    return system, release, version


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
    if os.path.exists(filepath):
        with open(filepath) as file:
            data = json.load(file)
            return data

    return None


def get_next_version_from_dir(filepath: Path, extension: str, substring: Optional[str] = None,
                              padding: int = const.VERSION_PADDING) -> str:
    """
    Gets the string representation of the next version number of versioned files in a path.

    Args:
        filepath(Path): The folder to search.

        extension(str): The file extension to search against.

        substring(Optional[str]): An optional substring the file name must contain.

        padding(int): The number of digits to make the version number, defaults to
         const.VERSION_PADDING.

    Returns:
        str: Will return the string representation of the version number (e.g. '005').

        Will return '001' if there is no version '001' within the folder.
    """
    ext = extension
    if not extension.startswith('.'):
        ext = f'.{extension}'

    contents = list_folder_contents(filepath)
    if not contents:
        return '1'.zfill(padding)

    versions = []

    def get_lucid_file_version_numbers(filename: str) -> Optional[str]:
        temp = re.search(r'_v(\d*)\..*$', filename)
        return temp.group(1) if temp else None

    for i in contents:
        if not str(i).endswith(ext):
            continue

        # if (no substring) or (if there is a substring AND it is in the filename)
        if not substring or (bool(substring) and substring in i):
            if suffix := get_lucid_file_version_numbers(str(i)):
                versions.append(suffix)

    if not versions:
        return str(1).zfill(padding)

    versions.sort(key=lambda s: (int(s), len(s)))  # in-case padding length changes mid project
    if padding == 0:
        padding = len(versions[-1])
    latest = int(versions[-1]) if versions else 0
    next_ver = latest + 1

    return str(next_ver).zfill(padding)


def get_latest_version_file_from_dir(filepath: Path, extension: str, substring: Optional[str] = None) -> Optional[str]:
    """
    Gets the string name of the latest version file in a directory.

    Args:
        filepath (path): The folder to search.

        extension(str): The file extension to search against.

        substring(Optional[str]): An optional substring the file name must contain.

    Returns:
        Optional[str]: The filename of the latest versioned file in the directory,
        else returns None if base file could not be found.
    """
    ext = extension
    if not extension.startswith('.'):
        ext = f'.{extension}'

    contents = list_folder_contents(filepath)
    latest = None
    if not contents:
        return latest

    if substring:
        for file in contents:
            if ext in file and substring in file:
                if file.split('.')[0][-1].isnumeric():
                    latest = file
    else:
        for file in contents:
            if ext in file:
                if file.split('.')[0][-1].isnumeric():
                    latest = file

    return latest


def get_next_dir_version_from_dir(filepath: Path,  substring: Optional[str] = None,
                                  padding: int = const.VERSION_PADDING) -> str:
    """
    Gets the string representation of the latest version number of versioned files in a path.

    Args:
        filepath(Path): The folder to search.

        substring(Optional[str]): An optional substring the file name must contain.

        padding(int): The number of digits to make the version number, defaults to
         const.VERSION_PADDING.

    Returns:
        str: Will return the string representation of the version number (e.g. '005').

        Will return '001' if there is no version '001' within the folder.
    """
    if filepath:
        contents = list_folder_contents(filepath)
        latest = None
        if contents:
            if substring:
                for file in contents:
                    if os.path.isdir(file) and substring in file:
                        if file[-padding:].isdigit():
                            latest = file
            else:
                for file in contents:
                    full_dir_path = Path(filepath, file)
                    if full_dir_path.is_dir():
                        if file[-padding:].isdigit():
                            latest = file

        if latest:
            current_version = latest[-padding:]  # strips all but digits
            if current_version:
                return str(int(current_version) + 1).zfill(padding)
            else:
                return '1'.zfill(padding)
        else:
            return '1'.zfill(padding)
    else:
        return '1'.zfill(padding)


def sort_path_list(path_objs: list[Path] = None) -> Optional[list[Path]]:
    """
    Alpha-numerically sorts a list of pathlib.Paths.

    Args:
        path_objs(list[Path]): The list of paths to sort.

    Returns:
        Optional[list[Path]]: The sorted list of paths or None if no
        list was provided.
    """
    if path_objs is None:
        return None

    if len(path_objs) == 1:
        return path_objs

    sort_strings = []
    for p in path_objs:
        sort_strings.append(p.as_posix())

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    sort_strings.sort(key=alphanum_key)

    sorted_paths = []
    for s in sort_strings:
        sorted_paths.append(Path(s))

    return sorted_paths


def print_center_header(title: str, header_char: str = '-') -> None:
    """Prints a header line with the title, surrounded by spaces and a
    line of the header_char. Will dynamically size to the terminal width,
    if able, otherwise will default to width 80.

    Args:
        title (str): The header title, or what to put in the header.
        header_char (str): The character to make the header line.
         Defaults to '-'.
    """
    msg = title.strip()
    width, _ = shutil.get_terminal_size()
    print(f' {msg} '.center(width, header_char))


def _print_msg(header: str, msg: str, custom_tag: Optional[str] = None) -> None:
    """ >> [HEADER][TAG] - msg """
    tag = custom_tag.upper() or ''
    if custom_tag and not custom_tag.startswith('['):
        tag = f'[{custom_tag}]'
    print(f'[{header}]{tag} - {msg}')


def print_lucid_msg(msg: str, custom_tag: Optional[str] = None) -> None:
    """Simple print wrapper with [LUCID] header."""
    _print_msg('LUCID', msg, custom_tag)


def print_error_msg(msg: str, custom_tag: Optional[str] = None) -> None:
    """Simple print wrapper with [ERROR] header and timestamp."""
    _print_msg('ERROR', msg, custom_tag)


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
    size_name: list[str] = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return s, size_name[i]


class ProgressBar(object):
    """
    A progress bar that outputs to stderr for tracking progress
    when looping.

    Example usages:
    >>> for _ in ProgressBar(range(11)):
    >>>     ...

    Args:
        data(sequence): Any sequence data type that can be looped through.
    """
    def __init__(self, data: Sequence[Any]):
        self.data = data
        self.index = 0
        self.start_time = time.perf_counter()
        self.last_time = self.start_time
        self.iteration_time = time.perf_counter()

    def __iter__(self) -> 'ProgressBar':
        return self

    def __next__(self) -> Any:
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1

            current_time = time.perf_counter()
            self.iteration_time = current_time - self.last_time
            self.last_time = current_time

            self.draw_progress_bar()
            return result
        else:
            raise StopIteration

    def draw_progress_bar(self) -> None:
        """Outputs the progress bar to stderr, with percentage filled based on the current
        index of the sequence data item.
        Will flush stderr each time the progress bar is drawn.
        """
        percent = self.index / len(self.data)
        bar_len = 20
        sys.stderr.write("\r")
        progress = ""
        for i in range(bar_len):
            if i < int(bar_len * percent):
                progress += "█"
            else:
                progress += " "
        sys.stderr.write("|%s| %.2f%% - Iteration time: %.4f seconds" % (progress, percent * 100, self.iteration_time))
        sys.stderr.flush()

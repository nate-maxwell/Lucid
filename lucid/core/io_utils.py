"""
# IO Utilities

* Description:

    Various IO utilities and namespace shorteners.
"""


from __future__ import annotations
import datetime
import enum
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


_CHECK_PATH = Path('does/not/exist')  # TODO: make this configurable
"""When a destructive workflow invokes an io_utils function, it first checks if
_CHECK_PATH does not exist or if the path to perform the destructive action on
is under the _CHECK_PATH.

If the _CHECK_PATH does not exist, then the pipeline does not care about
checking whether a path can be used in destructive workflows.

If _CHECK_PATH does exist, then the functions check if the path given to the
function is a child of _CHECK_PATH. If it is a child, it can be subjected to
destructive workflows, if it isn't, a ValueError is raised.
"""


def list_folder_contents(path: Path, full_path: bool = False) -> list[Path] | list[str] | None:
    """
    Lists the contents, or full path for contents, of a folder.

    Args:
        path (pathlib.Path): Folder path to list contents of.

        full_path (bool): To return string names or paths of folder contents. Defaults to False.

    Returns:
        String names of folder contents if full_path = False,
        Paths for folder contents if full_path = True.
        Else None if nothing if the path does not exist.
    """
    if not path.exists():
        return None

    if full_path:
        return list(path.glob('*'))
    return os.listdir(path)


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


def _create_structure(structure: dict, destination: Optional[Path] = None) -> None:
    """Recursively creates a folder form a nested dict."""
    if not destination.exists():
        create_folder(destination)
    for k, v in structure.items():
        _create_structure(v, Path(destination, k))


def create_structure(structure: dict, destination: Path) -> None:
    """Create a directory structure from a given dict outline.
    Example:
    {
        'assets': {
            'model': {},
            'texture': {},
            'anim': {}
        },
        'config': {}
    }
    """
    # Separated from _create_structure as to require a destination path,
    # whereas it is optional in the _recursive one.
    _create_structure(structure, destination)
    print(f'{structure} written to {destination}.')


def delete_folder(path: Path) -> None:
    """
    Removes folder path from V:/shows/ downward, or linux equivalent if on linux.

    Args:
        path (Path): the path to the folder to delete. Will throw exception if
            path does not start with 'V:/shows/', or linux equivalent if on linux.
    """
    if not _CHECK_PATH.exists() or _CHECK_PATH in list(path.parents):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.remove(filename)
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(path)
    else:
        raise ValueError(f'Path must be within {_CHECK_PATH.as_posix()}!')


def delete_file(filepath: Path) -> None:
    """
    Removes specified file from V:/shows/, or linux equivalent if on linux.

    Args:
        filepath (Path): the path to the file to delete. Will throw exception if
            path does not start with 'V:/shows/', or linux equivalent if on linux.
    """
    if not _CHECK_PATH.exists() or _CHECK_PATH in list(filepath.parents):
        os.remove(filepath)
    else:
        raise ValueError(f'Path must be within {_CHECK_PATH.as_posix()}')


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
    return str(today)


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


def serialize_object_json(obj: Any) -> dict:
    """
    Serializes the items in an object's __dict__ into a dictionary after
    converting all enums to values and paths to as_posix strings.

    If a value is not a Path object, enum, string, int, float, dict, list,
    bool, or None, it will be converted to string before insertion.

    Args:
        obj (any): The object to serialize.
    Returns:
        dict: A json (hopefully) friendly dict.
    """
    data = {}
    json_types = [str, int, float, dict, list, bool, None]
    for k, v in obj.__dict__.items():
        if isinstance(v, Path):
            data[k] = v.as_posix()
        elif isinstance(v, enum.Enum):
            data[k] = v.value
        elif type(v) not in json_types:
            data[k] = str(v)
        else:
            data[k] = v

    return data


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
    tag = custom_tag.upper() if custom_tag else ''
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
        progress = ''
        for i in range(bar_len):
            if i < int(bar_len * percent):
                progress += '█'
            else:
                progress += ' '

        progress_bar_str = '|%s| %.2f%% - Iteration time: %.4f seconds'
        sys.stderr.write(progress_bar_str % (progress, percent * 100, self.iteration_time))
        sys.stderr.flush()

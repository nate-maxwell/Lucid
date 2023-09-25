"""
# Unreal Directory Structure Construction

* Description

    A recursive method to create a directory structure from a json schema.

* Update History

    `2023-09-24` - Init
"""


from pathlib import Path

import lucid.io_utils


def main(structure: dict, content_folder: Path):
    """
    Create a directory structure from a given json outline.

    Args:
        structure(dict): A dictionary representing the desired directory structure.
        content_folder(Path): The path to the unreal project content directory.l
        Can most commonly be gotten using unreal.SystemLibrary.get_project_content_directory().
    """
    _recurse(structure, content_folder)
    print(f'{structure} written to {content_folder}.')


def _recurse(structure: dict, destination: Path = None):
    """
    Recursively creates a folder form a nested dict.

    Args:
        structure(dict): The folder structure, in dictionary format, to create.
        destination(Path): The path designating where to create the folders.
        Empty paths will count as the current working path and return true for
        path.exists().
    """
    if not destination.exists():
        lucid.io_utils.create_folder(destination)
    for k, v in structure.items():
        _recurse(v, Path(destination, k))

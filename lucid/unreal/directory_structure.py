"""
# Unreal Directory Structure Construction

* Description

    A recursive method to create a directory structure from a json schema.
"""


from pathlib import Path
from typing import Optional

import lucid.core.io_utils


def main(structure: dict, content_folder: Path) -> None:
    """Create a directory structure from a given json outline."""
    _recurse(structure, content_folder)
    print(f'{structure} written to {content_folder}.')


def _recurse(structure: dict, destination: Optional[Path] = None) -> None:
    """Recursively creates a folder form a nested dict."""
    if not destination.exists():
        lucid.core.io_utils.create_folder(destination)
    for k, v in structure.items():
        _recurse(v, Path(destination, k))

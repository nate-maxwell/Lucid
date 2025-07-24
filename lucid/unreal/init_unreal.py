"""
# Init Unreal

* Description

    The startup script for unreal, when launched through the Lucid core.
"""


from pathlib import Path

import unreal

import lucid.core.io_utils
import lucid.unreal.directory_structure
import lucid.unreal.paths


unreal.log('[LUCID PIPELINE INITIALIZATION] - Hello Dreamworld.')

structure_file = Path(Path(__file__).parent, 'directory_structure.json')
structure = lucid.core.io_utils.import_data_from_json(structure_file)


def main() -> None:
    """The primary function for executing code on project startup within the
    Lucid core. Any additional functions should be added here.
    """
    lucid.unreal.directory_structure.main(structure, lucid.unreal.paths.CONTENT_DIR)


main()

"""
# Init Unreal

* Description

    The startup script for unreal, when launched through the Lucid pipeline.

* Update History

    `2023-09-24` - Init
"""


from pathlib import Path

import unreal

import lucid.io_utils
import lucid.constants
import lucid.unreal.paths
import lucid.unreal.directory_structure
import lucid.unreal.editor_buttons


unreal.log('[LUCID PIPELINE INITIALIZATION] - Hello Dreamworld.')

structure = lucid.io_utils.import_data_from_json(Path(lucid.constants.CONFIG_PATH, 'unreal_directory_structure.json'))


def main() -> None:
    """
    The primary function for executing code on project startup within the Lucid pipeline.
    Any additional functions should be added here.
    """
    lucid.unreal.directory_structure.main(structure, lucid.unreal.paths.CONTENT_DIR)
    lucid.unreal.editor_buttons.main()


main()

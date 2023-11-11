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


unreal.log('[LUCID PIPELINE INITIALIZATION] - Hello Dreamworld.')

structure = lucid.io_utils.import_data_from_json(Path(lucid.constants.CONFIG_PATH, 'unreal_directory_structure.json'))


def launch_lucid_toolbar() -> None:
    """Runs the Lucid plugin toolbar UI."""
    lucid_toolbar = unreal.load_asset('/Lucid/UI/Lucid_Toolbar')
    unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem).spawn_and_register_tab(lucid_toolbar)


def main() -> None:
    """
    The primary functino for executing code on project startup within the Lucid pipeline.
    Any additional functions should be added here.
    """
    lucid.unreal.directory_structure.main(structure, lucid.unreal.paths.CONTENT_DIR)
    launch_lucid_toolbar()


main()

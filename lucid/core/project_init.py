"""
# Lucid Project Initialization

* Description:

    Creates all necessary files and directories for new projects.
"""


import os
from pathlib import Path

from lucid.core import const
from lucid.core import database
from lucid.core import exceptions
from lucid.core import io_utils
from lucid.core import plugins
from lucid.core import project_paths
from lucid.core.config import Config


# -----------------------------------------------------------------------------
# !! const.ENV_PROJECT environ var must be set before running !!
# -----------------------------------------------------------------------------

if not os.getenv(const.ENV_PROJECT) is None:
    raise exceptions.InvalidProjectException()


def install_base_dirs() -> None:
    """Ensures base project directories are created.
    Some are remade in other funcs but the redundancy here is so that the base
    project dirs are all made together, in the event that a section hasn't been
    spun up yet by installation features of a specific system.
    """
    for i in [
        project_paths.ASSET_DIR,
        project_paths.CONFIG_DIR,
        project_paths.PROJECT_USER_DIR,
        project_paths.ENGINE_DIR
    ]:
        io_utils.create_folder(i)


def install_all_engine_dirs() -> None:
    """!! These are not to be confused with the engine project's directory
    structure!

    This creates all engine related directories in the project's directory
    structure.
    """
    for i in [
        project_paths.ENGINE_DIR,
        project_paths.ENGINE_OUTGOING_DIR,
        project_paths.ENGINE_SIM_DIR,
        project_paths.ENGINE_RENDERS_DIR
    ]:
        io_utils.create_folder(i)


def install_project_plugin_dirs() -> None:
    """Ensures plugin dirs exist at project level for each supported DCC."""
    for i in const.Dcc:
        dcc_path = plugins.get_plugins_dir(i.value)
        io_utils.create_folder(dcc_path)


def install_domain_dirs() -> None:
    """Installs const.Domain member dirs, model, texture, etc."""
    for i in const.Domain:
        dir_name = i.value.lower()
        path = Path(project_paths.PROJECT_ROOT, 'asset', dir_name)
        io_utils.create_folder(path)


def install_project_configs() -> None:
    """Ensures all project level configs exist within the project."""
    for config_ in Config.project_configs:
        config_file = config_.get_config_filepath(Config.project)
        if not config_file.exists():
            config_file.parent.mkdir(parents=True, exist_ok=True)
            config_.export_data(Config.project)


def initialize_database() -> None:
    """Creates and initializes the various database files."""
    io_utils.create_folder(project_paths.DATABASE_DIR)


def initialize_show_paths() -> None:
    """Ensures all necessary project paths for the currently loaded show
    have been created.
    A show must be set for this to function.
    """
    install_base_dirs()
    install_all_engine_dirs()
    install_project_plugin_dirs()
    install_domain_dirs()
    install_project_configs()
    initialize_database()

    # Import to trigger DB creation, var to keep from being marked as
    # unused import
    _ = database.SESSION

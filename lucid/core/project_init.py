"""
# Lucid Project Initialization

* Description:

    Creates all necessary files and directories for new projects.
"""


import os
from pathlib import Path

from lucid.core import const
from lucid.core import exceptions
from lucid.core import io_utils
from lucid.core import project_paths
from lucid.core import work
from lucid.core.config import Config


def install_all_engine_dirs() -> None:
    """!! These are not to be confused with the engine project's directory
    structure!

    This creates all engine related directories in the project's directory
    structure.
    """
    for i in [
        project_paths.engine_dir,
        project_paths.engine_outgoing_dir,
        project_paths.engine_sim_dir,
        project_paths.engine_renders_dir
    ]:
        io_utils.create_folder(i)


def install_project_plugin_dirs() -> None:
    """Ensures plugin dirs exist at project level for each supported DCC."""
    for i in const.Dcc:
        dcc_path = Path(project_paths.plugins_dir, i.value)
        io_utils.create_folder(dcc_path)


def install_domain_dirs() -> None:
    """Installs const.Domain member dirs, model, texture, etc."""
    exclude = [const.Role.SYSTEM, const.Role.UNASSIGNED]

    for i in const.Role:
        if i in exclude:
            continue

        dir_name = i.value.lower()
        path = Path(project_paths.work_dir, dir_name)
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
    io_utils.create_folder(project_paths.database_dir)


def initialize_vendor() -> None:
    """Creates all various vendor or outsourced directories."""
    for i in [
        project_paths.vendor_dir,
        project_paths.vendor_outgoing_dir,
        project_paths.vendor_incoming_dir
    ]:
        io_utils.create_folder(i)


def initialize_show_paths() -> None:
    """Ensures all necessary project paths for the currently loaded show
    have been created.
    A show must be set for this to function.
    """
    # install_base_dirs()
    install_all_engine_dirs()
    install_project_plugin_dirs()
    install_domain_dirs()
    install_project_configs()
    initialize_database()
    initialize_vendor()

    # Import to trigger DB creation, var to keep from being marked as
    # unused import
    _ = work.SESSION


def create_project(project_code: str) -> None:
    """Creates a project at the given path and uses the lowest folder name, or
    path stem, as the project name.
    """
    os.environ[const.ENV_PROJECT] = project_code

    # Maybe not needed, but more checks are good.
    if Config.project == const.UNASSIGNED:
        raise exceptions.InvalidProjectException()

    project_path = Path(const.PROJECTS_DIR, project_code.upper())
    io_utils.create_folder(project_path)
    initialize_show_paths()

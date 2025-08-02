"""
# Lucid Installation

* Description:

    This is a decoupling of const/path declaration and any side-effectful
    operations. Herein is a launch procedure that ensures all necessary
    paths and files exist, either on the user's system, or a network drive
    location on behalf of the user or the pipeline itself.

    Additionally sets up base systems, like the root logger.
"""


import logging
import uuid
from pathlib import Path

import lucid.core.logger
from lucid.core import const
from lucid.core import io_utils
from lucid.core import plugins
from lucid.core.auth import setup_user_default


lucid.core.logger.setup_root_logger()
_logger = logging.getLogger('lucid.core.install')


# --------Project--------------------------------------------------------------

def install_project_plugin_dirs() -> None:
    """Ensures plugin dirs exist at project level for each supported DCC."""
    for i in const.Dcc:
        dcc_path = plugins.get_plugins_dir(i.value)
        io_utils.create_folder(dcc_path)


def install_project_sub_dirs() -> None:
    """Ensures all necessary project paths for the currently loaded show
    have been created.
    """
    install_project_plugin_dirs()


# --------Facility-------------------------------------------------------------

def _setup_integrity_system() -> None:
    _logger.info('Starting [integrity] system initialization')
    io_utils.create_folder(const.FACILITY_SYSTEMS_DIR)
    file_path = Path(const.FACILITY_SYSTEMS_DIR, '_integrity.json')
    data = {'SYSTEM_TOKEN': str(uuid.uuid4())}
    io_utils.export_data_to_json(file_path, data, overwrite=False)


def _add_admin_default() -> None:
    # ! Must come after _setup_integrity_system()
    _logger.info('Starting [integrity] admin default user creation')
    setup_user_default()


def install_default_user() -> None:
    """Ensures an admin user is always present."""
    _setup_integrity_system()
    _add_admin_default()


def install_user_dirs() -> None:
    """Install core user directories."""
    _logger.info('Starting [user] dir install')
    io_utils.create_folder(const.USER_APPDATA_DIR)
    io_utils.create_folder(const.USER_LOG_DIR)
    io_utils.create_folder(const.USER_HOME_DIR)


def install_facility_dirs() -> None:
    """Ensure core facility directories exist."""
    _logger.info('Starting [facility] dir install')
    io_utils.create_folder(const.FACILITY_DIR)
    io_utils.create_folder(const.FACILITY_PIPE_CONFIGS_DIR)
    io_utils.create_folder(const.USER_DETAILS_DIR)
    io_utils.create_folder(const.PROJECTS_DIR)


def install_user_facility() -> None:
    """Create all necessary pipeline directories."""
    install_default_user()
    install_user_dirs()
    install_facility_dirs()

    _logger.info('Install complete')


if __name__ == '__main__':
    install_user_facility()

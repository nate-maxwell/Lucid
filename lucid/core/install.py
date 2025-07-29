"""
# Lucid Installation

* Description:

    This is a decoupling of const/path declaration and the side-effectful
    operations. Herein is a launch procedure that ensures all necessary
    paths and files exist, either on the user's system, or a network drive
    location on behalf of the user.

    Additionally sets up the root logger.
"""


import logging

import lucid.core.logging
from lucid.core import const
from lucid.core import io_utils


lucid.core.logging.main()
_logger = logging.getLogger('lucid.core.install')


def install_user_dirs() -> None:
    """Install core user directories."""
    io_utils.create_folder(const.USER_APPDATA_DIR)
    io_utils.create_folder(const.USER_LOG_DIR)


def install_facility_dirs() -> None:
    """Ensure core facility directories exist."""
    io_utils.create_folder(const.FACILITY_DIR)
    io_utils.create_folder(const.FACILITY_PIPE_CONFIGS_DIR)
    io_utils.create_folder(const.USER_DETAILS_DIR)
    io_utils.create_folder(const.PROJECTS_DIR)


def install_all() -> None:
    """Create all necessary pipeline directories."""
    _logger.info('Starting [user] dir install')
    install_user_dirs()

    _logger.info('Starting [facility] dir install')
    install_facility_dirs()

    _logger.info('Install complete')


def main() -> None:
    install_all()


if __name__ == '__main__':
    main()

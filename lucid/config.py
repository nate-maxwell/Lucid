"""
# Lucid Config Management

* Description:

    Herein are getter + setters for config values for a project in the
    lucid pipeline.
"""


import os
from pathlib import Path

import lucid.const
import lucid.exceptions
import lucid.io_utils


class _Config(object):
    """Config value management class."""
    _instance: '_Config' = None

    def __new__(cls) -> '_Config':
        """Singleton handling."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._data: dict = {}
        self.refresh()
        _config = self

    @property
    def project(self) -> str:
        """The currently loaded project."""
        proj = os.getenv(lucid.const.ENV_PROJECT, lucid.const.UNASSIGNED).replace(';', '')
        if proj == lucid.const.UNASSIGNED:
            raise lucid.exceptions.InvalidProjectException()

        return proj

    @property
    def general(self) -> dict:
        return self._data['general']

    def refresh(self) -> None:
        config_path = Path(lucid.const.PROJECTS_PATH, self.project, 'config')
        config_files = lucid.io_utils.list_folder_contents(config_path, True)
        if not config_files:
            raise lucid.exceptions.MissingConfigsException()

        for i in config_files:
            file_data = lucid.io_utils.import_data_from_json(i)
            if not file_data:
                raise lucid.exceptions.MissingConfigsException()

            self._data[i.stem.lower()] = file_data


Config = _Config()
"""The canonical config class interface."""

"""
# Lucid Config Management

* Description:

    Herein are getter + setters for config values for a project in the
    lucid pipeline.
"""


import os
from dataclasses import dataclass
from pathlib import Path

from lucid.core import io_utils
from lucid.core import const
from lucid.core import regex_utils


@dataclass
class _ConfigObject(object):
    """Small dataclass object with refresh methods that checks for project
    config files.
    """

    def get_config_file(self, project: str) -> Path:
        config_path = Path(const.PROJECTS_DIR, project, 'config')
        config_file = Path(config_path, f'{self.__class__.__name__.lower()}.json')

        return config_file

    def refresh(self, project: str) -> None:
        file = self.get_config_file(project)
        file_data = io_utils.import_data_from_json(file)
        if not file_data:
            return

        for k, v in file_data.items():
            if regex_utils.is_path_like(v):
                self.__dict__[k] = Path(v)
            else:
                self.__dict__[k] = v

    def export_data(self, project: str) -> None:
        file_path = self.get_config_file(project)
        serialized = {
            key: value.as_posix() if isinstance(value, Path) else value
            for key, value in self.__dict__.items()
        }
        io_utils.export_data_to_json(file_path, serialized, True)


@dataclass
class GeneralConfig(_ConfigObject):
    ...


@dataclass
class ApplicationConfig(object):
    # -----Maya-----
    MAYA_EXEC: Path = Path(const.UNASSIGNED)
    MAYA_BASE_DIR: Path = MAYA_EXEC.parent.parent
    MAYA_SITE_PACKAGES: Path = Path(MAYA_BASE_DIR, 'Python/Lib/site-packages')
    MAYA_USER_SETUP_DIR = Path(const.LUCID_DIR, 'maya', '_userSetup')

    # -----Unreal-----
    UNREAL_EXEC: Path = Path(const.UNASSIGNED)
    LUCID_UE_DIR: Path = Path(const.LUCID_DIR, 'unreal')

    # -----Substance Painter-----
    PAINTER_EXEC: Path = Path(const.UNASSIGNED)
    PAINTER_PLUGINS_DIR = Path(const.LUCID_DIR, 'painter')

    # -----Substance Designer-----
    DESIGNER_EXEC: Path = Path(const.UNASSIGNED)

    def refresh(self) -> None:
        if not const.USER_SETTINGS_FILE.exists():
            return
        data = io_utils.import_data_from_json(const.USER_SETTINGS_FILE)
        self.MAYA_EXEC = Path(data['Maya']) if data['Maya'] else const.UNASSIGNED
        self.UNREAL_EXEC = Path(data['Unreal']) if data['Unreal'] else const.UNASSIGNED
        self.PAINTER_EXEC = Path(data['Painter']) if data['Painter'] else const.UNASSIGNED
        self.DESIGNER_EXEC = Path(data['Designer']) if data['Designer'] else const.UNASSIGNED


class _Config(object):
    """Primary config value management class."""
    _instance: '_Config' = None

    def __new__(cls) -> '_Config':
        """Singleton handling."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._general = GeneralConfig()
        self._applications = ApplicationConfig()
        self._objects: list = [
            self._general,
            self._applications
        ]
        self.refresh()

    @property
    def project(self) -> str:
        """The currently loaded project."""
        proj = os.getenv(const.ENV_PROJECT, const.UNASSIGNED).replace(';', '')

        return proj

    @property
    def general(self) -> _ConfigObject:
        return self._general

    @property
    def applications(self) -> ApplicationConfig:
        return self._applications

    def refresh(self) -> None:
        for i in self._objects:
            if isinstance(i, _ConfigObject):
                i.refresh(self.project)
            else:
                i.refresh()

            msg = f'Updated {i.__class__.__name__} config data!'
            io_utils.print_lucid_msg(msg, 'config')


Config = _Config()
"""The canonical config singleton class interface."""

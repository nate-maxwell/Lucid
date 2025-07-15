"""
# Base Pipeline Class

Pipeline objects are the file io and database handlers for saving, opening, and
saving files within the pipeline. They handle both database asset registration
and the disk file operations.
"""


import enum
import logging
from typing import Callable

from lucid.work import WorkUnit


hook_func_type = Callable[[WorkUnit], None]


@enum.unique
class Hook(enum.Enum):
    """Most common file io hook types."""
    PRE_PUBLISH = 'pre_publish'
    POST_PUBLISH = 'post_publish'
    PRE_OPEN = 'pre_open'
    POST_OPEN = 'post_open'
    PRE_IMPORT = 'pre_import'
    POST_IMPORT = 'post_import'


class Pipeline(object):
    """Base class for all pipeline domain handlers."""

    _hooks: dict[str, list[hook_func_type]] = {
        Hook.PRE_PUBLISH: [],
        Hook.POST_PUBLISH: [],
        Hook.PRE_OPEN: [],
        Hook.POST_OPEN: [],
        Hook.PRE_IMPORT: [],
        Hook.POST_IMPORT: []
    }

    # --------File IO Methods--------------------------------------------------

    @classmethod
    def publish_file(cls, unit: WorkUnit) -> None:
        """Publish a file using domain-specific logic, then register
        it in the database.
        """
        cls.log_debug(f'Publishing file: {WorkUnit.task_name}')
        cls.run_hooks(Hook.PRE_PUBLISH.value, unit)
        cls.dcc_publish(unit)
        cls.register_in_database(unit)
        cls.run_hooks(Hook.POST_PUBLISH.value, unit)
        cls.log_info('Publish complete.')

    @classmethod
    def open_file(cls, unit: WorkUnit) -> None:
        """Open a file using the application's API."""
        cls.log_debug(f'Opening file: {unit.task_name}')
        cls.run_hooks(Hook.PRE_OPEN.value, unit)
        cls.dcc_open(unit)
        cls.run_hooks(Hook.POST_OPEN.value, unit)

    @classmethod
    def import_file(cls, unit: WorkUnit) -> None:
        """Import a file using the application's API."""
        cls.log_debug(f'Importing file: {unit.task_name}')
        cls.run_hooks(Hook.PRE_IMPORT.value, unit)
        cls.dcc_import(unit)
        cls.run_hooks(Hook.POST_IMPORT.value, unit)

    # --------Abstract Methods-------------------------------------------------

    @classmethod
    def dcc_publish(cls, unit: WorkUnit) -> None:
        raise NotImplemented

    @classmethod
    def dcc_open(cls, unit: WorkUnit) -> None:
        raise NotImplemented

    @classmethod
    def dcc_import(cls, unit: WorkUnit) -> None:
        raise NotImplemented

    @classmethod
    def register_in_database(cls, unit: WorkUnit) -> None:
        raise NotImplemented

    # --------Event Hooks------------------------------------------------------

    @classmethod
    def register_hook(cls, event_name: str, hook_func: hook_func_type) -> None:
        if event_name not in cls._hooks:
            raise ValueError(f'Unknown hook event: {event_name}')
        cls._hooks[event_name].append(hook_func)
        cls.log_debug(f'Registered hook: {hook_func.__name__} to {event_name}')

    @classmethod
    def run_hooks(cls, event_name: str, unit: WorkUnit) -> None:
        for hook in cls._hooks.get(event_name, []):
            cls.log_debug(f'Running {event_name} hook: {hook.__name__}')
            hook(unit)

    # --------Logging Methods--------------------------------------------------

    @classmethod
    def _logger(cls) -> logging.Logger:
        return logging.getLogger(f'{cls.__module__}.{cls.__name__}')

    @classmethod
    def log_debug(cls, message: str) -> None:
        cls._logger().debug(message)

    @classmethod
    def log_info(cls, message: str) -> None:
        cls._logger().info(message)

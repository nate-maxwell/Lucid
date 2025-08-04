"""
# Base Pipeline Class

* Description:

    Pipeline objects are the file io and database handlers for saving, opening, and
    saving files within the core. They handle both database asset registration
    and the disk file operations.
"""


import json
import logging
from typing import Callable

from lucid.core.unit.work import WorkUnit


HOOK_FUNC_TYPE = Callable[[WorkUnit], None]
"""A function that takes a work unit and pre or post processes the DCC
workspace to prepare for, or clean up, data for publishing.
"""


class BasePipeline(object):
    """Base class for all core domain handlers."""

    _hooks: dict[str, list[HOOK_FUNC_TYPE]] = {}
    """The list of processes registered by name.
    These are usually pre/post processes sorted by label - like 'pre-publish'.
    """

    # --------Event Hooks------------------------------------------------------

    @classmethod
    def register_hook(cls, event_name: str, hook_func: HOOK_FUNC_TYPE) -> None:
        """Adds a hook to the given event name, typically 'pre/post-event_type'."""
        if event_name not in cls._hooks:
            raise ValueError(f'Unknown hook event: {event_name}')
        cls._hooks[event_name].append(hook_func)
        cls.log_debug(f'Registered hook: {hook_func.__name__} to {event_name}')

    @classmethod
    def run_hooks(cls, event_name: str, unit: WorkUnit) -> None:
        """Sends the given work unit through all hooks registered to the
        event name.
        """
        for hook in cls._hooks.get(event_name, []):
            cls.log_debug(f'Running {event_name} hook: {hook.__name__}')
            hook(unit)

    # --------Logging Methods--------------------------------------------------

    @classmethod
    def _logger(cls) -> logging.Logger:
        return logging.getLogger(f'lucid.pipeline.{cls.__module__}.{cls.__name__}')

    @classmethod
    def log_debug(cls, message: str) -> None:
        cls._logger().debug(message)

    @classmethod
    def log_info(cls, message: str) -> None:
        cls._logger().info(message)

    @classmethod
    def log_with_context(cls, wu: WorkUnit, message: str) -> None:
        """Log info with attached WorkUnit context."""
        cls._logger().info(
            f'{message} | context: '
            f'project={wu.project}, task={wu.task_name}, '
            f'user={wu.user}, dcc={wu.dcc}'
        )

    @staticmethod
    def pretty_format_dict(d: dict) -> str:
        return json.dumps(d, indent=4)

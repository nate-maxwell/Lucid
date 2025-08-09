"""
# Lucid Pipeline Plugin Management

* Description:

    Herein is a library for pipeline developers to create plugins to modify
    pipeline actions on the project level.
"""


import sys
import importlib.util
import logging
from pathlib import Path

from lucid.core import const
from lucid.core import environment
from lucid.core import io_utils
from lucid.core.config import Config
from lucid.core import project_paths


# -----------------------------------------------------------------------------

__example_plugin_authoring__ = 'doc string'
"""
Example Plugin Authoring

-------------------------------------------------------------------------------

>>> # WorkUnit handling

>>> def check_naming(unit: WorkUnit) -> None:
>>>     if not unit.domain_details.base_name.islower():
>>>         raise ValueError('Asset names must be lowercase.')

>>> MayaModelPipeline.register_hook('pre-publish', check_naming)

-------------------------------------------------------------------------------

>>> # Or non-WorkUnit centric code

>>> from my_code.maya.shelf_builder import ShelfBuilder

>>> ShelfBuilder().build_shelves()
"""

# -----------------------------------------------------------------------------

_logger = logging.getLogger('lucid.plugins')


def _import_module_from_path(path: Path) -> None:
    """Attempts to load the plugin module spec from the given path."""
    spec = importlib.util.spec_from_file_location(path.stem, path.as_posix())

    if spec and spec.loader:
        try:
            module = importlib.util.module_from_spec(spec)
            sys.modules[path.stem] = module
            spec.loader.exec_module(module)
            _logger.debug(f'Loaded external plugin: {path.stem}')
        except Exception as e:
            _logger.warning(f'Failed to load plugin {path.as_posix()}: {e}')


def load_external_plugins() -> None:
    """Loads all plugin modules within the loaded project's plugin directory.
    """
    # Really unsure if this should instead load paths from an environment
    # variable and cache which ones are already loaded.

    dcc = environment.get_clean_var(const.ENV_DCC)
    if environment.var_is_unassigned(dcc):
        _logger.debug(
            f'No loaded DCC found - Plugin loading aborted.'
        )
        return

    plugins_dir = Path(project_paths.plugins_dir, dcc)
    if not plugins_dir.exists():
        _logger.debug(
            f'No plugins folder found for {Config.project}'
            f' - Plugin loading aborted.'
        )
        return

    for plugin in io_utils.list_folder_contents(plugins_dir, True):
        _logger.info(f'Looking for plugins in: {plugin}')
        for pyfile in Path(plugin).rglob('*.py'):
            _import_module_from_path(pyfile)

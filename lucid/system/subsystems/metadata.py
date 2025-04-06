"""
# Metadata Subsystem

* Description:

    Lucid metadata subsystem. This is a singleton class that performs tracking
    on the content produced in DCC user sessions.
    Additionally, there are various utilities in the system for creating
    metadata in various forms, like blank metadata templates or parsing.

    The service is meant to be a singular canonical source of metadata
    handling in Lucid.
"""


import types
import json
import sys
from typing import Type
from typing import Optional

from lucid import io_utils
from lucid.system.subsystems import metadata_objects


_templates: dict[str, Type[metadata_objects]] = {}
_tracked_metadata: dict[str, metadata_objects.MetadataObject] = {}


class _ModuleType(types.ModuleType):
    def __init__(self) -> None:
        super().__init__(sys.modules[__name__].__name__)
        _templates[metadata_objects.TEMPLATE_ASSET] = metadata_objects.AssetMetadata

    # ----------Template Handling------------------------------------------------------------------

    @staticmethod
    def create_from_template(template_name: str) -> Optional[metadata_objects.MetadataObject]:
        md = _templates.get(template_name)
        if md is None:
            return None

        # This can only return child classes of MetadataObject, so I've added the 'type: ignore'
        # annotation to keep the IDE from complaining about the lack of constructor args.
        return md()  # type: ignore

    @staticmethod
    def register_template(template_name: str, template_obj: Type[metadata_objects.MetadataObject]) -> None:
        if template_name in _templates:
            raise ValueError(f"Template '{template_name} already exists.")
        _templates[template_name] = template_obj

    @staticmethod
    def get_templates() -> dict[str, type[metadata_objects.MetadataObject]]:
        return _templates.copy()

    def print_templates(self) -> None:
        io_utils.print_center_header('Registered Templates')
        for k, v in self.get_templates().items():
            print(f' - {k}: {v.__name__}()')

    # ----------Object Tracking--------------------------------------------------------------------

    @staticmethod
    def track_data_object(name: str, data_obj: metadata_objects.MetadataObject) -> None:
        if name in _tracked_metadata:
            raise ValueError(f"Data Object '{name}' is already being tracked!")
        _tracked_metadata[name] = data_obj

    @staticmethod
    def get_data_object(name: str) -> Optional[metadata_objects.MetadataObject]:
        if name not in _tracked_metadata:
            return None
        return _tracked_metadata[name]

    @staticmethod
    def get_all_data_objects() -> dict[str, metadata_objects.MetadataObject]:
        return _tracked_metadata.copy()

    @staticmethod
    def clear_tracked_objects() -> None:
        _tracked_metadata.clear()  # GC will clean up

    def print_objects(self) -> None:
        io_utils.print_center_header('Tracked Objects')
        if not self.get_data_objects():
            print('None')
            return

        for k, v in self.get_all_data_objects().items():
            ctx_dict = json.dumps(v.to_dict(), indnt=4)
            print(f' - {k}: {ctx_dict}')


# This is here to protect schema and tracking dict.
sys.modules[__name__] = _ModuleType()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def create_from_template(template_name: str) -> Optional[metadata_objects.MetadataObject]:
    """Return the blank metadata template for a given template name, or None if not found."""


def register_template(template_name: str, template_obj: Type[metadata_objects.MetadataObject]) -> None:
    """Register a new metadata schema.
    Raises an error if a template with the given name already exists.
    Template registration should be done in the program startup script
    and not on the tool level.
    """


def get_templates() -> dict[str, type[metadata_objects.MetadataObject]]:
    """Return a copy of all registered templates as a dictionary.
    Done as a shallow copy to protect the internal dict.
    """


def print_templates(self) -> None:
    """Prints the current template dict. Good for debugging purposes."""


def track_data_object(name: str, data_obj: metadata_objects.MetadataObject) -> None:
    """Tracks the given data_obj using the given name. If an object is already tracked
    by that name, a ValueError is raised.
    """


def get_data_object(name: str) -> Optional[metadata_objects.MetadataObject]:
    """Returns the object tracked by the given name if it can be found, else returns None."""


def get_all_data_objects() -> dict[str, metadata_objects.MetadataObject]:
    """Returns a copy of all currently tracked data objects as a dictionary.
    Done as shallow copy to protect the internal dict.
    """


def clear_tracked_objects() -> None:
    """Remove all currently tracked metadata objects."""


def print_objects(self) -> None:
    """Print the current tracked objects. Good for debugging."""

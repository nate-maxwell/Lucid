"""
# Metadata Objects

* Descriptions:

    Library of metadata objects + base class.
"""


from pathlib import Path

from lucid import const
from lucid import io_utils
from lucid.system.subsystems import context


# Template type names
TEMPLATE_ASSET = 'TEMPLATE_ASSET'
TEMPLATE_ANIM = 'TEMPLATE ANIM'
TEMPLATE_TEXTURE = 'TEMPLATE_TEXTURE'
TEMPLATE_RENDER = 'TEMPLATE_RENDER'


class MetadataObject(object):
    def __init__(self, template_name: str) -> None:
        self.template_type_name = template_name
        self.date = '-----Will Update On Data Export-----'
        self.time = '-----Will Update On Data Export-----'
        self.context = context.blank_context
        self.user = const.USERNAME

    def __str__(self) -> str:
        return str(self.to_dict())

    def add_kwargs_metadata(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def to_dict(self) -> dict:
        d = self.__dict__.copy()
        d['context'] = self.context.to_dict()
        return d

    def write_metadata(self, json_file_path: Path) -> None:
        """Writes out the metadata to the given path. Sets the date + time in the data."""
        self.date = io_utils.get_date()
        self.time = io_utils.get_time()
        self.context = context.current_context
        io_utils.export_data_to_json(json_file_path, self.to_dict(), True)


class AssetMetadata(MetadataObject):
    def __init__(self) -> None:
        super().__init__(TEMPLATE_ASSET)
        self.note = const.UNASSIGNED
        self.variant = const.UNASSIGNED

"""
# Lucid Metadata Library

* Description:

    The basic metadata workflow and utility library.

* Update History:

    `2024-01-21` - Init
"""


from pathlib import Path

import lucid.io_utils


class MetaData(object):
    def __init__(self):
        self.path: Path = Path('does/not/exist')
        self.username: str = ''
        self.date: str = ''
        self.note: str = ''
        self.context: str = ''
        self.version: int = 1

    def add_kwarg_metadata(self, **kwargs):
        self.__dict__.update(kwargs)


class GeoMetadata(MetaData):
    def __init__(self):
        super().__init__()


class AnimMetadata(MetaData):
    def __init__(self):
        super().__init__()
        self.asset: str = ''
        self.start_frame: int = 1001
        self.end_frame: int = 1100
        self.sequence: bool = False
        self.direction: str = ''
        self.root_motion: bool = False


def export_metadata(data: MetaData, overwrite: bool = False):
    d = data.__dict__
    d.pop('path')
    lucid.io_utils.export_data_to_json(data.path, d, overwrite)

"""
# Compositing Domain Pipeline

* Description:

    Base class for all compositing pipelines.
    This handles composite database registration.
    DCCs must implement application API specific file IO.
"""


from dataclasses import dataclass
from typing import Optional

from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


@dataclass
class CompDetails(AssetDetails):
    nuke_script_path: Optional[str] = None
    resolution: tuple[int, int] = (1920, 1080)

    @classmethod
    def from_dict(cls, data: dict) -> 'CompDetails':
        return cls(
            nuke_script_path=data['nuke_script_path'],
            resolution=data['resolution']
        )


class CompositingPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

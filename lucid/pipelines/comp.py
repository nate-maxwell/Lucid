"""
# Compositing Domain Pipeline

* Description:

    Base class for all compositing pipelines.
    This handles composite database registration.
    DCCs must implement application API specific file IO.
"""


from dataclasses import dataclass
from typing import Optional

import lucid.work
from lucid.pipelines.asset import AssetPipeline
from lucid.details import DomainDetails


@dataclass
class CompDetails(DomainDetails):
    nuke_script_path: Optional[str] = None
    resolution: tuple[int, int] = (1920, 1080)

    @classmethod
    def from_dict(cls, data: dict) -> 'CompDetails':
        return cls(
            data['nuke_script_path'],
            data['resolution']
        )


class CompositingPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

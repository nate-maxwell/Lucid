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
from lucid.pipeline.base import Pipeline


@dataclass
class CompDetails(lucid.work.DomainDetails):
    nuke_script_path: Optional[str] = None
    resolution: tuple[int, int] = (1920, 1080)

    @classmethod
    def from_dict(cls, data: dict) -> 'CompDetails':
        return cls(
            data['nuke_script_path'],
            data['resolution']
        )


class CompositingPipeline(Pipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print()
        print(f'Registering data: {uow.to_dict()}')

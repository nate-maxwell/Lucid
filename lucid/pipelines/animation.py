"""
# Animation Domain Pipeline

* Description:

    Base class for all animation pipelines.
    This handles animation database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass
from typing import Optional

import lucid.work
from lucid.pipelines.asset import AssetDetails
from lucid.pipelines.asset import AssetPipeline


@enum.unique
class AnimDirection(enum.Enum):
    FORWARD = 'FWD'
    BACKWARD = 'BWD'
    LEFT = 'LFT'
    RIGHT = 'RGT'

    FORWARD_LEFT = 'FWDL'
    FORWARD_RIGHT = 'FWDR'
    BACKWARD_LEFT = 'BWDL'
    BACKWARD_RIGHT = 'BWDR'


@dataclass
class AnimDetails(AssetDetails):
    directional: bool = False
    root_motion: bool = False
    direction: Optional[AnimDirection] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'AnimDetails':
        return cls(
            data['base_name'],
            data['variation'],
            data['version'],
            data['file_type'],
            data['directional'],
            data['root_motion'],
            AnimDirection[data['direction']]
        )


class AnimPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

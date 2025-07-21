"""
# Animation Domain Pipeline

* Description:

    Base class for all animation core.
    This handles animation database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass
from typing import Optional

import lucid.core.work
from lucid.core.asset import AssetDetails
from lucid.core.asset import AssetPipeline


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
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            directional=data['directional'],
            root_motion=data['root_motion'],
            direction=AnimDirection[data['direction']]
        )


class AnimPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.core.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

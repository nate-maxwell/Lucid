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
from lucid.pipeline.base import Pipeline


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
class AnimDetails(lucid.work.AssetDetails):
    directional: bool = False
    root_motion: bool = False
    direction: Optional[AnimDirection] = None


class AnimPipeline(Pipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print()
        print(f'Registering data: {uow.to_dict()}')

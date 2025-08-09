"""
# Animation Domain Pipeline

* Description:

    Base class for all animation pipelines.
    This handles animation database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass

import lucid.core.const
import lucid.core.work
from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


# --------Animation Details----------------------------------------------------

@enum.unique
class AnimDirection(enum.Enum):
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    FORWARD_LEFT = 'FORWARD_LEFT'
    FORWARD_RIGHT = 'FORWARD_RIGHT'
    BACKWARD_LEFT = 'BACKWARD_LEFT'
    BACKWARD_RIGHT = 'BACKWARD_RIGHT'

    UNASSIGNED = lucid.core.const.UNASSIGNED


@dataclass
class AnimDetails(AssetDetails):
    directional: bool = False
    root_motion: bool = False
    direction: AnimDirection = AnimDirection.UNASSIGNED

    @classmethod
    def from_dict(cls, data: dict) -> 'AnimDetails':
        return cls(
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            directional=data['directional'],
            root_motion=data['root_motion'],
            direction=AnimDirection(data['direction'])
        )


# --------Pipeline Object------------------------------------------------------

class AnimPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

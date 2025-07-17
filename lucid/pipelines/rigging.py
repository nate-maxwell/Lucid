"""
# Rigging Domain Pipeline

* Description:

    Base class for all rigging pipelines.
    This handles rigging database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass

import lucid.work
from lucid.pipelines.asset import AssetPipeline


@dataclass
class RigDetails(lucid.work.AssetDetails):
    is_control_rig: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'RigDetails':
        return cls(
            data['set_name'],
            data['asset_name'],
            data['is_control_rig']
        )


class RiggingPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

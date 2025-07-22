"""
# Rigging Domain Pipeline

* Description:

    Base class for all rigging core.
    This handles rigging database registration.
    DCCs must implement application API specific file IO.
"""


from dataclasses import dataclass

import lucid.core.work
from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline


@dataclass
class RigDetails(AssetDetails):
    is_control_rig: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'RigDetails':
        return cls(
            domain_name=data['domain_name'],
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            is_control_rig=data['is_control_rig']
        )


class RiggingPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.core.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

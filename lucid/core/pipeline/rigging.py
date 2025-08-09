"""
# Rigging Domain Pipeline

* Description:

    Base class for all rigging pipelines.
    This handles rigging database registration.
    DCCs must implement application API specific file IO.
"""


from dataclasses import dataclass
from typing import cast

from lucid.core import const
from lucid.core import work
from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


# --------Rig Details----------------------------------------------------------

@dataclass
class RigDetails(AssetDetails):
    is_control_rig: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'RigDetails':
        return cls(
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            is_control_rig=data['is_control_rig']
        )


# --------Pipeline Object------------------------------------------------------

class RiggingPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

    @classmethod
    def attach_rig(cls, parent_wu: WorkUnit, rig_wu: WorkUnit) -> None:
        d = cast(RigDetails, rig_wu.domain_details)
        parent_wu.components[f'{const.Role.RIG.value}.{d.base_name}'] = rig_wu

    @classmethod
    def get_rig(cls, parent_wu: WorkUnit) -> WorkUnit:
        return parent_wu.components[const.Role.RIG.value]


work.register_attach_method(namespace=const.Role.RIG.value,
                            method=RiggingPipeline.attach_rig,
                            domain_cls=RigDetails)

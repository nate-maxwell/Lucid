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
from lucid.pipeline.base import Pipeline


@dataclass
class RigDetails(lucid.work.AssetDetails):
    is_control_rig: bool = False


class RiggingPipeline(Pipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print()
        print(f'Registering data: {uow.to_dict()}')

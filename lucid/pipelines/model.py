"""
# Model Domain Pipeline

* Description:

    Base class for all model pipelines.
    This handles model database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass
from typing import Optional

import lucid.work
from lucid.pipelines.asset import AssetPipeline


@enum.unique
class ModelCategory(enum.Enum):
    VEH = 'VEH'
    CHAR = 'CHAR'
    PROP = 'PROP'
    CREATURE = 'CREA'
    ENV = 'ENV'
    FOLIAGE = 'FOLIAGE'


@dataclass
class ModelDetails(lucid.work.AssetDetails):
    category: Optional[ModelCategory] = None
    lod: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'ModelDetails':
        return cls(
            data['set_name'],
            data['asset_name'],
            ModelCategory[data['category']],
            data['lod']
        )


class ModelPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

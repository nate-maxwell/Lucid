"""
# Shader Domain Pipeline

* Description:

    Base class for all shader pipelines.
    This handles shader database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass

from lucid.core import const
from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


@enum.unique
class ShaderCategory(enum.Enum):
    HARD_SURFACE = 'HARD_SURFACE'
    WATER = 'WATER'
    SKIN = 'SKIN'
    EYE = 'EYE'
    GROOM = 'GROOM'
    FOLIAGE = 'FOLIAGE'
    FX = 'FX'
    DECAL = 'DECAL'
    LIGHT = 'LIGHT'
    VOLUME = 'VOLUME'
    UNASSIGNED = const.UNASSIGNED


@dataclass
class ShaderDetails(AssetDetails):
    category: ShaderCategory = ShaderCategory.UNASSIGNED

    @classmethod
    def from_dict(cls, data: dict) -> 'ShaderDetails':
        return cls(
            domain_name=data['domain_name'],
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            category=ShaderCategory(data['category'])
        )


class ShaderPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

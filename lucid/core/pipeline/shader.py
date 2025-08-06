"""
# Shader Domain Pipeline

* Description:

    Base class for all shader pipelines.
    This handles shader database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass
from typing import cast

from lucid.core import const
from lucid.core import work
from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


# --------Shader Details-------------------------------------------------------

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
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            category=ShaderCategory(data['category'])
        )


# --------Pipeline Object------------------------------------------------------

class ShaderPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

    @classmethod
    def attach_shader(cls, parent_wu: WorkUnit, shader_wu: WorkUnit) -> None:
        d = cast(ShaderDetails, shader_wu.domain_details)
        parent_wu.components[f'{const.Role.SHADER.value}.{d.base_name}'] = shader_wu

    @classmethod
    def get_shader(cls,
                   parent_wu: WorkUnit,
                   shader_base_name: str) -> WorkUnit:
        prefix = const.Role.SHADER.value
        return parent_wu.components[f'{prefix}.{shader_base_name}']


work.register_attach_method(namespace=const.Role.SHADER.value,
                            method=ShaderPipeline.attach_shader,
                            domain_cls=ShaderDetails)

"""
# Texture Domain Pipeline

* Description:

    Base class for all texture pipelines.
    This handles texture database registration.
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


# --------Texture Details-------------------------------------------------------

@enum.unique
class TextureType(enum.Enum):
    BASECOLOR = 'BC'
    NORMAL = 'N'
    ALPHA = 'A'
    EMISSIVE = 'E'

    CHANNEL_PACKED = 'ORM'
    """Occlusion(r), Roughness(g), Metallic(b) channel packed."""

    UNASSIGNED = 'UNASSIGNED'


@dataclass
class TextureDetails(AssetDetails):
    texture_type: TextureType = TextureType.UNASSIGNED
    colorspace: str = 'sRGB'
    power_of_two: bool = True
    channel_packed: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'TextureDetails':
        return cls(
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            texture_type=TextureType(data['texture_type']),
            colorspace=data['colorspace'],
            power_of_two=data['power_of_two'],
            channel_packed=data['channel_packed']
        )


# --------Pipeline Object------------------------------------------------------

class TexturePipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

    # ! Texture work units are attached to shader work units to preserve map
    # relation for each texture. This could be doubled up by base_name naming
    # convention, but it is done here at minimum.

    @classmethod
    def attach_texture(cls, shader_wu: WorkUnit, texture_wu: WorkUnit) -> None:
        d = cast(TextureDetails, texture_wu.domain_details)
        component_key = f'{const.Role.TEXTURE.value}.{d.texture_type.value}'
        shader_wu.components[component_key] = texture_wu

    @classmethod
    def get_texture(cls,
                    shader_wu: WorkUnit,
                    texture_type: TextureType) -> WorkUnit:
        component_key = f'{const.Role.TEXTURE.value}.{texture_type.value}'
        return shader_wu.components[component_key]


work.register_attach_method(namespace=const.Role.TEXTURE.value,
                            method=TexturePipeline.attach_texture,
                            domain_cls=TextureDetails)

"""
# Texture Domain Pipeline

* Description:

    Base class for all texture pipelines.
    This handles texture database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass

import lucid.work
from lucid.pipelines.asset import AssetPipeline


@enum.unique
class TextureType(enum.Enum):
    BASECOLOR = 'BC'
    NORMAL = 'N'
    ALPHA = 'A'
    CHANNEL_PACKED = 'ORM'
    """Occlusion(r), Roughness(g), Metallic(b) channel packed."""


@dataclass
class TextureDetails(lucid.work.AssetDetails):
    texture_type: TextureType = TextureType.BASECOLOR
    colorspace: str = 'sRGB'
    power_of_two: bool = True
    channel_packed: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'TextureDetails':
        return cls(
            data['set_name'],
            data['asset_name'],
            TextureType[data['texture_type']],
            data['colorspace'],
            data['power_of_two'],
            data['channel_packed']
        )


class TexturePipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

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
from lucid.pipeline.base import Pipeline


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


class TexturePipeline(Pipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print()
        print(f'Registering data: {uow.to_dict()}')

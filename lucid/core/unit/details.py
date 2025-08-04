"""
# Work Unit Domain Details

* Description:

    Work units are descriptors of work for any pipeline action, these
    descriptors could cover models, rigs, textures, etc. Each of those domains
    have different specific details that describe their respective unit of
    work. Domain details are those specifics, and are component classes of
    work units.

    All domain details are defined here so that builder can understand fields
    from domain specific details components to correctly attach component work
    units to each other.
"""


import enum
from dataclasses import dataclass
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import cast

import lucid.core.exceptions
import lucid.core.io_utils
from lucid.core import const


# --------Base Definition------------------------------------------------------

T_DOM_DETAILS = TypeVar('T_DOM_DETAILS', bound='DomainDetails')
"""Upper bounds type for all DomainDetails derived types."""


@dataclass
class DomainDetails(object):
    """Base domain details type.
    Domain details are the metadata items for specific core.
    For example if a texture domain file is a power of 2 or repeating.
    """

    domain_name: const.Domain = const.Domain.UNASSIGNED

    def __eq__(self, other: 'DomainDetails') -> bool:
        if not isinstance(other, DomainDetails):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def validate_tokens(self) -> bool:
        """Returns False if WU has required fields that are unassigned."""
        for i in self.__dict__.keys():
            if i == const.UNASSIGNED:
                return False
            if isinstance(i, enum.Enum) and i.value == const.UNASSIGNED:
                return False

        return True

    def to_dict(self) -> dict:
        return lucid.core.io_utils.serialize_object_json(self)

    @classmethod
    def from_dict(cls, data: dict) -> T_DOM_DETAILS:
        raise NotImplemented


def verify_details_type(type_: Type[T_DOM_DETAILS],
                        detail: DomainDetails) -> T_DOM_DETAILS:
    """Verifies if the given ctx_dom object is of the dom_type, cast to the
    given type for type checking. If the domain details is not of the given
    type, a DomDetailsError exception is raised.
    """
    if not isinstance(detail, type_):
        err_msg = f'Got {type(detail)}, expected {type_}!'
        raise lucid.core.exceptions.DomainDetailsException(err_msg)

    details = cast(type_, detail)
    return details


# --------Asset Details--------------------------------------------------------

@dataclass
class AssetDetails(DomainDetails):
    """Any file that would make its way into engine or shot files."""
    # spaceship_damaged_v001.fbx
    base_name: str = const.UNASSIGNED
    variation: str = const.UNASSIGNED
    version: Optional[int] = None
    file_type: str = const.UNASSIGNED


# --------Model Details--------------------------------------------------------

@enum.unique
class ModelCategory(enum.Enum):
    VEH = 'VEH'
    CHAR = 'CHAR'
    PROP = 'PROP'
    CREATURE = 'CREA'
    ENV = 'ENV'
    UNASSIGNED = lucid.core.const.UNASSIGNED


@dataclass
class ModelDetails(AssetDetails):
    rigged: bool = False
    category: ModelCategory = ModelCategory.UNASSIGNED
    lod: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'ModelDetails':
        return cls(
            domain_name=data['domain_name'],
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            rigged=data['rigged'],
            category=ModelCategory(data['category']),
            lod=data['lod']
        )


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
            domain_name=data['domain_name'],
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            category=ShaderCategory(data['category'])
        )


# --------Texture Details------------------------------------------------------

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
            domain_name=data['domain_name'],
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            texture_type=TextureType(data['texture_type']),
            colorspace=data['colorspace'],
            power_of_two=data['power_of_two'],
            channel_packed=data['channel_packed']
        )


# --------Rig Details----------------------------------------------------------

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


# --------Animation Details----------------------------------------------------

@enum.unique
class AnimDirection(enum.Enum):
    FORWARD = 'FWD'
    BACKWARD = 'BWD'
    LEFT = 'LFT'
    RIGHT = 'RGT'

    FORWARD_LEFT = 'FWDL'
    FORWARD_RIGHT = 'FWDR'
    BACKWARD_LEFT = 'BWDL'
    BACKWARD_RIGHT = 'BWDR'

    UNASSIGNED = lucid.core.const.UNASSIGNED


@dataclass
class AnimDetails(AssetDetails):
    directional: bool = False
    root_motion: bool = False
    direction: AnimDirection = AnimDirection.UNASSIGNED

    @classmethod
    def from_dict(cls, data: dict) -> 'AnimDetails':
        return cls(
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            directional=data['directional'],
            root_motion=data['root_motion'],
            direction=AnimDirection(data['direction'])
        )


# --------Composition Details--------------------------------------------------

@dataclass
class CompDetails(AssetDetails):
    nuke_script_path: Optional[str] = None
    resolution: tuple[int, int] = (1920, 1080)

    @classmethod
    def from_dict(cls, data: dict) -> 'CompDetails':
        return cls(
            data['nuke_script_path'],
            data['resolution']
        )

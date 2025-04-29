"""
# Context Object

* Description:

    A context object is an object with attrs + values in the context os environ
    structure. They can be attached to something or used to represent the
    would-be context of various items in a scene e.g. multiple character assets
    for a paired animation.
"""


from typing import Any
from typing import Optional
from typing import TypeVar

from lucid import const


class ContextType(object):
    def __init__(self) -> None:
        self.ext = const.UNASSIGNED
        self.filename = const.UNASSIGNED

    def __eq__(self, other: Any) -> bool:
        return self.__dict__ == other.__dict__

    def to_dict(self) -> dict[str, str]:
        return {k: str(v) for k, v in self.__dict__}


T_CTX_TYPE = TypeVar('T_CTX_TYPE', bound=ContextType)


class AssetContext(ContextType):
    def __init__(self) -> None:
        super().__init__()
        self.category = const.UNASSIGNED
        self.set = const.UNASSIGNED
        self.name = const.UNASSIGNED


class ModelContext(AssetContext):
    def __init__(self) -> None:
        super().__init__()
        self.lod = 1


class RigContext(AssetContext):
    # Doesn't use name field but inherits it form AssetContext.
    # Rigs work on sets rather than named assets.

    def __init__(self) -> None:
        super().__init__()


class TextureContext(AssetContext):
    def __init__(self) -> None:
        super().__init__()
        self.lod = 1
        self.power_of_two = False
        self.colorspace = const.UNASSIGNED
        self.channel_packed = False
        self.texture_type = const.UNASSIGNED  # BC, N, ORM, etc.


class AnimContext(AssetContext):
    # Doesn't use name field but inherits it form AssetContext
    # Animations work on rigs which work on sets rather than named assets.

    def __init__(self) -> None:
        super().__init__()
        self.direction = const.UNASSIGNED
        self.directional = False
        self.root_motion = False


class CompContext(ContextType):
    def __init__(self) -> None:
        super().__init__()
        raise NotImplemented


class LucidContext(object):
    """A packaged context that can be used to represent artificial contexts."""

    def __init__(self) -> None:
        self.project = const.UNASSIGNED
        self.dcc = const.UNASSIGNED
        self.role = const.UNASSIGNED
        self.subcontext: Optional[T_CTX_TYPE] = None

    def __eq__(self, other: Any) -> bool:
        return self.__dict__ == other.__dict__

    def to_dict(self) -> dict[str, str]:
        data = self.__dict__
        data['subcontext'] = self.subcontext.to_dict()
        return data

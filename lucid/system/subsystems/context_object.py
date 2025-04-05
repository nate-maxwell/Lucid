"""
# Context Object

* Description:

    A context object is an object with attrs + values in the context os environ
    structure. They can be attached to something or used to represent the
    would-be context of various items in a scene e.g. multiple character assets
    for a paired animation.
"""


from typing import Any

from lucid import const


class LucidContext(object):
    """A packaged context that can be used to represent artificial contexts."""

    def __init__(self) -> None:
        self.project = const.UNASSIGNED
        self.dcc = const.UNASSIGNED
        self.role = const.UNASSIGNED
        self.filetype = const.UNASSIGNED
        self.filename = const.UNASSIGNED
        self.category = const.UNASSIGNED
        self.subcategory = const.UNASSIGNED
        self.directional = const.UNASSIGNED
        self.root_motion = const.UNASSIGNED
        self.power_of_two = const.UNASSIGNED
        self.colorspace = const.UNASSIGNED
        self.channel_packed = const.UNASSIGNED

    def __eq__(self, other: Any) -> bool:
        return self.__dict__ == other.__dict__

    def to_dict(self) -> dict[str, str]:
        return self.__dict__

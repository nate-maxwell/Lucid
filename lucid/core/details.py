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

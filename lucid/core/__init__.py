"""
# Lucid Domain Pipelines

* Description:

    Pipeline objects are the file io and database handlers for saving, opening, and
    saving files within the core. They handle both database asset registration
    and the disk file operations.
"""


import enum


def contains_enum_to_dict(obj: object) -> dict:
    """Converts the __dict__ of an object that contains an enum field to
    something json serializable.
    """
    return {
        key: value.value if isinstance(value, enum.Enum) else value
        for key, value in obj.__dict__.items()
    }


@enum.unique
class Domain(enum.Enum):
    UNASSIGNED = 'UNASSIGNED'
    ANIM = 'anim'
    COMP = 'comp'
    LAYOUT = 'layout'
    MODEL = 'model'
    RIG = 'rig'
    SHADER = 'shader'
    TEXTURE = 'texture'
    SYSTEM = 'system'

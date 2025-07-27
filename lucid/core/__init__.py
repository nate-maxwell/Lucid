"""
# Lucid Domain Pipelines

* Description:

    Pipeline objects are the file io and database handlers for saving, opening, and
    saving files within the core. They handle both database asset registration
    and the disk file operations.
"""


import enum


@enum.unique
class Domain(enum.Enum):
    # Seriously unsure if this should be here, in const, or in pipeline.__init__.

    UNASSIGNED = 'UNASSIGNED'  # literal instead of circular const dependency
    ANIM = 'anim'
    COMP = 'comp'
    LAYOUT = 'layout'
    MODEL = 'model'
    RIG = 'rig'
    SHADER = 'shader'
    TEXTURE = 'texture'
    SYSTEM = 'system'

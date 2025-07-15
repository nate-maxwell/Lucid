"""
# Unit of Work

* Description:

    A Unit of Work is a representation of what kind of data the artist is
    currently producing, or how they are producing it.
"""


import enum
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import cast

from lucid import const
from lucid import exceptions


def _contains_enum_to_dict(obj: object) -> dict:
    """Converts the __dict__ of an object that contains an enum field to
    something json serializable.
    """
    return {
        key: value.value if isinstance(value, enum.Enum) else value
        for key, value in obj.__dict__.items()
    }


# ----------Session------------------------------------------------------------

@enum.unique
class Role(enum.Enum):
    UNASSIGNED = const.UNASSIGNED
    MODEL = 'ROLE_MODEL'
    RIG = 'ROLE_RIG'
    TEXTURE = 'ROLE_TEXTURE'
    ANIM = 'ROLE_ANIM'
    COMP = 'ROLE_COMP'
    LEVEL = 'ROLE_LEVEL'


@enum.unique
class Domain(enum.Enum):
    UNASSIGNED = const.UNASSIGNED
    ANIM = 'ANIM'
    COMP = 'COMP'
    LAYOUT = 'LAYOUT'
    MODEL = 'MODEL'
    RIG = 'RIG'
    SHADER = 'SHADER'
    TEXTURE = 'TEXTURE'


# --------Domain Details-------------------------------------------------------

@dataclass
class DomainDetails(object):
    """Base domain details type.
    Domain details are the metadata items for specific domains.
    For example if a texture domain file is a power of 2 or repeating.
    """

    def to_dict(self) -> dict:
        return _contains_enum_to_dict(self)


@dataclass
class AssetDetails(DomainDetails):
    """Any file that would make its way into engine or shot files."""
    set_name: Optional[str] = None
    asset_name: str = const.UNASSIGNED


# --------Base Work Unit-------------------------------------------------------

@enum.unique
class WorkStatus(enum.Enum):
    DRAFT = 'DRAFT'
    REGISTERED = 'REGISTERED'
    PUBLISHED = 'PUBLISHED'
    IMPORTED = 'IMPORTED'
    ERROR = 'ERROR'


@dataclass
class WorkUnit:
    """A first-class representation of a unit of work in the pipeline.
    A work unit can represent the work the user is doing, work previously
    done by another use that is being imported into the current user work
    session, details of work to be done, etc.
    """

    status: WorkStatus = WorkStatus.DRAFT
    project: str = const.UNASSIGNED
    user: str = const.USERNAME
    role: Role = Role.UNASSIGNED
    domain: Domain = Domain.UNASSIGNED
    task_name: str = const.UNASSIGNED
    input_path: Optional[Path] = None
    output_path: Optional[Path] = None
    metadata: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            'status': self.status.value,
            'project': self.project,
            'user': self.user,
            'role': self.role.value,
            'domain': self.domain.value,
            'task_name': self.task_name,
            'input_path': self.input_path.as_posix() if self.input_path else None,
            'output_path': self.input_path.as_posix() if self.output_path else None,
            'metadata': self.metadata or {},
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'WorkUnit':
        return cls(
            status=WorkStatus[data['status']],
            project=data['project'],
            user=data['user'],
            role=Role[data['role']],
            domain=Domain[data['domain']],
            task_name=data['task_name'],
            input_path=Path(data['input_path']) if data['input_path'] else None,
            output_path=Path(data['output_path']) if data['output_path'] else None,
            metadata=data.get('metadata')
        )

    def validate(self) -> bool:
        """Returns True/False if UOW values are valid."""
        # Currently only checks input path. Should perhaps also validate if
        # output path is a legal disk path.
        if not self.input_path or not self.input_path.exists():
            raise FileNotFoundError(f'Invalid input: {self.input_path}')
        return True


# --------Globals--------------------------------------------------------------

T_DOM_DETAILS = TypeVar('T_DOM_DETAILS', bound=DomainDetails)
"""Upper bounds type for all DomainDetails derived types."""


def verify_subcontext_domain(type_: Type[T_DOM_DETAILS],
                             detail: DomainDetails) -> T_DOM_DETAILS:
    """Verifies if the given ctx_dom object is of the dom_type, cast to the
    given type for type checking. If the domain details is not of the given
    type, a DomDetailsError exception is raised.
    """
    if not isinstance(detail, type_):
        err_msg = f'Got {type(detail)}, expected {type_}!'
        raise exceptions.DomDetailsError(err_msg)

    details = cast(type_, detail)
    return details

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

import lucid.const
from lucid.pipelines import details
from lucid import const


@enum.unique
class Role(enum.Enum):
    UNASSIGNED = const.UNASSIGNED
    MODEL = 'ROLE_MODEL'
    RIG = 'ROLE_RIG'
    TEXTURE = 'ROLE_TEXTURE'
    ANIM = 'ROLE_ANIM'
    COMP = 'ROLE_COMP'
    LEVEL = 'ROLE_LEVEL'
    SYSTEM = 'ROLE_SYSTEM'


@enum.unique
class WorkStatus(enum.Enum):
    DRAFT = 'DRAFT'
    REGISTERED = 'REGISTERED'
    PUBLISHED = 'PUBLISHED'
    IMPORTED = 'IMPORTED'
    ERROR = 'ERROR'


@dataclass
class WorkUnit:
    """A first-class representation of a unit of work in the pipelines.
    A work unit can represent the work the user is doing, work previously
    done by another use that is being imported into the current user work
    session, details of work to be done, etc.
    """

    status: WorkStatus = WorkStatus.DRAFT
    project: str = const.UNASSIGNED
    dcc: str = const.UNASSIGNED
    user: str = const.USERNAME
    role: Role = Role.UNASSIGNED
    domain: details.Domain = details.Domain.UNASSIGNED
    task_name: str = const.UNASSIGNED
    input_path: Optional[Path] = None
    output_path: Optional[Path] = None
    metadata: Optional[dict] = None
    domain_details: Optional[details.DomainDetails] = None

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
            'domain_details': self.domain_details.to_dict() if self.domain_details else None
        }

    @classmethod
    def from_dict(cls, data: dict, details_cls: Type[details.T_DOM_DETAILS]) -> 'WorkUnit':
        return cls(
            status=WorkStatus[data['status']],
            project=data['project'],
            user=data['user'],
            role=Role[data['role']],
            domain=details.Domain[data['domain']],
            task_name=data['task_name'],
            input_path=Path(data['input_path']) if data['input_path'] else None,
            output_path=Path(data['output_path']) if data['output_path'] else None,
            metadata=data.get('metadata'),
            domain_details=details_cls(**data['domain_detail']) if data.get('domain_details') else None
        )

    def validate_tokens(self) -> bool:
        """Returns False if WU has required fields that are unassigned."""
        for i in [self.project, self.role, self.domain, self.task_name]:
            if i == lucid.const.UNASSIGNED:
                return False
            if isinstance(i, enum.Enum) and i.value == lucid.const.UNASSIGNED:
                return False

        return True

    def validate_paths(self) -> bool:
        """Returns True/False if WU values are valid."""
        # TODO: Currently only checks input path. Should perhaps also validate
        #  if output path is a legal disk path.
        if not self.input_path or not self.input_path.exists():
            raise FileNotFoundError(f'Invalid input: {self.input_path}')
        return True

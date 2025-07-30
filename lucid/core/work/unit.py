"""
# Unit of Work

* Description:

    A Unit of Work is a representation of what kind of data the artist is
    currently producing, or how they are producing it.

    Work Units are 'first class' (or as close as they can be) within the
    lucid pipeline.
"""


import enum
import json
import uuid
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Optional
from typing import Type

import lucid
import lucid.core.exceptions
from lucid.core import const
from lucid.core.work import details
from lucid.core.config import Config


# --------Work Unit Definition-------------------------------------------------

@enum.unique
class WorkStatus(enum.Enum):
    DRAFT = 'DRAFT'
    REGISTERED = 'REGISTERED'
    PUBLISHED = 'PUBLISHED'
    IMPORTED = 'IMPORTED'
    ERROR = 'ERROR'


@dataclass
class WorkUnit(object):
    """A first-class representation of a unit of work in the core.
    A work unit can represent the work the user is doing, work previously
    done by another user that is being imported into the current user work
    session, details of work to be done, etc.
    """
    uid: uuid.UUID = field(default_factory=uuid.uuid4)
    status: WorkStatus = WorkStatus.DRAFT
    project: str = Config.project
    dcc: const.Dcc = const.Dcc.UNASSIGNED
    user: str = const.USERNAME
    role: const.Role = const.Role.UNASSIGNED

    domain_details: Optional[details.DomainDetails] = None
    task_name: str = const.UNASSIGNED

    components: dict[str, 'WorkUnit'] = field(default_factory=dict)
    """Nested work units for assets that are comprised of components, represented by
    other work units.
    """

    input_path: Optional[Path] = None
    output_path: Optional[Path] = None

    metadata: Optional[dict] = field(default_factory=dict)

    def __post_init__(self) -> None:
        register_work_unit(self)

    def __str__(self) -> str:
        data = self.to_dict()
        return json.dumps(data, indent=4)

    # --------Serialization----------------------------------------------------

    def to_dict(self) -> dict:
        return {
            'id': str(self.uid),
            'status': self.status.value,
            'project': self.project,
            'dcc': self.dcc,
            'user': self.user,
            'role': self.role.value,
            'domain_details': self.domain_details.to_dict() if self.domain_details else None,
            'task_name': self.task_name,
            'input_path': self.input_path.as_posix() if self.input_path else None,
            'output_path': self.output_path.as_posix() if self.output_path else None,
            'metadata': self.metadata or {}
        }

    @classmethod
    def from_dict(cls, data: dict, details_cls: Type[details.T_DOM_DETAILS]) -> 'WorkUnit':
        return cls(
            status=WorkStatus(data['status']),
            project=data['project'],
            dcc=data['dcc'],
            user=data['user'],
            role=const.Role(data['role']),
            domain_details=details_cls(**data['domain_detail']) if data.get('domain_details') else None,
            task_name=data['task_name'],
            input_path=Path(data['input_path']) if data['input_path'] else None,
            output_path=Path(data['output_path']) if data['output_path'] else None,
            metadata=data.get('metadata')
        )

    def to_deep_dict(self) -> dict:
        data = self.to_dict()
        data['components'] = {}

        for k, unit in self.components.items():
            data['components'][k] = unit.to_deep_dict()

        return data

    # --------Validation-------------------------------------------------------

    def validate_tokens(self) -> bool:
        """Returns False if work unit has required fields that are unassigned."""
        for i in [self.project, self.role, self.domain_details.domain_name, self.task_name]:
            if i == const.UNASSIGNED:
                return False
            if isinstance(i, enum.Enum) and i.value == const.UNASSIGNED:
                return False

        return True

    def validate_paths(self) -> bool:
        """Returns True/False if WU values are valid."""
        # TODO: Currently only checks input path. Should perhaps also validate
        #  if output path is a legal disk path.
        if not self.input_path or not self.input_path.exists():
            raise FileNotFoundError(f'Invalid input: {self.input_path}')
        return True

    def validate_data(self) -> None:
        """Raises exceptions if unit tokens or domain detail tokens are
        invalid.
        """
        if not self.validate_tokens():
            raise lucid.core.exceptions.WorkUnitTokenException()
        if not self.domain_details.validate_tokens():
            raise lucid.core.exceptions.DomainDetailsTokenException()

    # --------Components-------------------------------------------------------

    # Work units can describe an asset that is composed of various components,
    # in the form of other nested work units.
    # Still not sure if this is the best place for these getters.

    @property
    def rig(self) -> Optional['WorkUnit']:
        if 'rig' in self.components:
            return self.components['rig']
        return None

    @property
    def shaders(self) -> list['WorkUnit']:
        return self.components.get('shaders', [])

    @property
    def textures(self) -> list['WorkUnit']:
        return self.components.get('textures', [])


# --------Tracking + Registration----------------------------------------------

_registry: dict[uuid.UUID, WorkUnit] = {}
"""A 'registry' of all created work units for tracking / debugging purposes.
Work units may have a lifetime, and therefore may not show up in the registry
at all times.
"""


def register_work_unit(wu: WorkUnit) -> None:
    _registry[wu.uid] = wu


def get_work_unit(uid: uuid.UUID) -> WorkUnit:
    return _registry[uid]


def all_work_units() -> list[WorkUnit]:
    return list(_registry.values())


def clear() -> None:
    _registry.clear()

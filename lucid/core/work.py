"""
# Unit of Work

* Description:

    A Unit of Work is a representation of what kind of data the artist is
    currently producing, or how they are producing it.

    Work Units are 'first class' (or as close as they can be) within the
    lucid pipeline.

    When an artist commits a unit of work to disk, i.e. publish, the work unit
    is serialized and stored with the asset to act as provenance.
"""


import enum
import json
import uuid
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Optional
from typing import Type
from typing import cast

import lucid
import lucid.core.exceptions
from lucid.core import const
from lucid.core import details
from lucid.core import io_utils
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
    """The asset file path. Where the work unit json and corresponding asset
    file will be written out.
    """

    metadata: Optional[dict] = field(default_factory=dict)

    def __str__(self) -> str:
        # Does not serialize component work units; shallow copy.
        data = self.to_dict()
        return json.dumps(data, indent=4)

    # --------Serialization----------------------------------------------------

    def to_dict(self) -> dict:
        return {
            'uid': str(self.uid),
            'status': self.status.value,
            'project': self.project,
            'dcc': self.dcc.value,
            'user': self.user,
            'role': self.role.value,
            'domain_details': self.domain_details.to_dict() if self.domain_details else None,
            'task_name': self.task_name,
            'components': {key: str(cls.uid) for key, cls in self.components.items()},
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

    def print_stack(self, unit_name: str) -> None:
        io_utils.print_center_header('Work Unit Structure')
        print(unit_name)
        self._print_stack()
        io_utils.print_center_header('-')

    def _print_stack(self, wu: Optional['WorkUnit'] = None, _in: int = 1) -> None:
        unit = self
        if wu is not None:
            unit = wu

        for k, v in unit.components.items():
            prefix = '    ' * _in
            print(f'{prefix}{k}')
            self._print_stack(v, _in + 1)

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
        """Returns True/False if WU paths are valid."""
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


# --------Serialization--------------------------------------------------------

def load_work_unit(path: Path, details_cls: Type[details.T_DOM_DETAILS]) -> WorkUnit:
    """Loads a WorkUnit from disk from a given JSON file.

    Args:
        path (Path): The path to the serialized WorkUnit JSON file.
        details_cls (Type[T_DOM_DETAILS]): The class used to deserialize the domain_details.
    Returns:
        WorkUnit: The loaded WorkUnit instance.
    """
    if not path.is_file():
        raise FileNotFoundError(f'WorkUnit file does not exist: {path}')

    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    unit = WorkUnit.from_dict(data, details_cls=details_cls)

    components_data = data.get('components', {})
    for key, component_dict in components_data.items():
        # Recursively build each component using same domain detail class
        unit.components[key] = WorkUnit.from_dict(component_dict, details_cls=details_cls)

    return unit


def save_work_unit(wu: WorkUnit, path: Path) -> None:
    """Serializes a WorkUnit and saves it to disk.

    Args:
        wu (WorkUnit): The work unit to serialize.
        path (Path): Where to store the data.
    """
    data = wu.to_dict()
    io_utils.export_data_to_json(path, data)


# --------Component Attachment-------------------------------------------------

# -----Model-----

def attach_model(parent_wu: WorkUnit, shader_wu: WorkUnit) -> None:
    d = cast(details.ShaderDetails, shader_wu.domain_details)
    parent_wu.components[f'shader.{d.base_name}'] = shader_wu


def get_model(parent_wu: WorkUnit, shader_base_name: str) -> WorkUnit:
    return parent_wu.components[f'shader.{shader_base_name}']


# -----Shader-----

def attach_shader(parent_wu: WorkUnit, shader_wu: WorkUnit) -> None:
    d = cast(details.ShaderDetails, shader_wu.domain_details)
    parent_wu.components[f'shader.{d.base_name}'] = shader_wu


def get_shader(parent_wu: WorkUnit, shader_base_name: str) -> WorkUnit:
    return parent_wu.components[f'shader.{shader_base_name}']


# -----Texture-----

# ! Texture work units are attached to shader work units to preserve map
# relation for each texture. This could be doubled up by base_name naming
# convention, but it is done here at minimum.

def attach_texture(shader_wu: WorkUnit, texture_wu: WorkUnit) -> None:
    d = cast(details.TextureDetails, texture_wu.domain_details)
    shader_wu.components[f'texture.{d.texture_type.value}'] = texture_wu


def get_texture(shader_wu: WorkUnit,
                texture_type: details.TextureType) -> WorkUnit:
    return shader_wu.components[f'texture.{texture_type.value}']


# -----Rig-----

def attach_rig(parent_wu: WorkUnit, rig_wu: WorkUnit) -> None:
    parent_wu.components[f'rig'] = rig_wu


def get_rig(parent_wu: WorkUnit) -> WorkUnit:
    return parent_wu.components[f'rig']

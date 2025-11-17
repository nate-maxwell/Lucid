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
import os
import uuid
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Callable
from typing import Optional
from typing import Type
from typing import Union

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.orm import mapped_column

from lucid.core import const
from lucid.core import details
from lucid.core import exceptions
from lucid.core import io_utils
from lucid.core import project_paths
from lucid.core.auth import Auth
from lucid.core.config import Config


# --------Work Unit Orchestration----------------------------------------------

_ATTACH_FUNC_TYPE = Callable[['WorkUnit', 'WorkUnit'], None]
"""The function signature for funcs that take a parent and child work unit
and attach the child to the parent under the correct namespace.
"""

_ATTACH_FUNCS: dict[str, _ATTACH_FUNC_TYPE] = {}
"""String component namespace to method for attaching component work unit
to the current work unit.
"""

_DOMAIN_MAPPINGS: dict[str, Type[details.T_DOM_DETAILS]] = {}
"""Mapping of const.Domain to details class."""


# --------Work Unit Definition-------------------------------------------------

def register_attach_method(namespace: str,
                           method: _ATTACH_FUNC_TYPE,
                           domain_cls: Type[details.T_DOM_DETAILS]) -> None:
    """Allows pipelines to specify how a work unit can be nested into another
    work unit based on a namespace (key) value. This also takes a domain class
    type to inform deserialization of which domain class to attack when
    reconstructing a work unit.

    Args:
        namespace (str): The namespace the work unit will be attached to a
         parent work unit by in its components' dict.
        method (Callable[['WorkUnit', 'WorkUnit'], None]): The function that
         attaches a work unit to another.
        domain_cls (Type[details.T_DOM_DETAILS]): The domain details class
         that the child work unit will use.
    """
    _ATTACH_FUNCS[namespace] = method
    _DOMAIN_MAPPINGS[namespace] = domain_cls


@dataclass
class WorkUnit(object):
    """A first-class representation of a unit of work in the core.

    A work unit can represent the work the user is doing, work previously
    done by another user that is being imported into the current user work
    session, details of work to be done, etc.

    WorkUnits are immutable.
    """
    dcc: const.Dcc
    project: str
    role: const.Role
    domain_details: Optional[details.DomainDetails]

    task_name: str

    upstream_uid: Optional[uuid.UUID] = None
    """The uid of the work unit that led to this unit's creation."""
    output_path: Optional[Path] = None
    """The asset file path. Where the work unit json and corresponding asset
    file will be written out.
    """

    uid: uuid.UUID = field(default_factory=uuid.uuid4)
    user: str = const.USERNAME

    components: dict[str, 'WorkUnit'] = field(default_factory=dict)
    """Nested work units for assets that are comprised of components,
    represented by other work units.
    """

    metadata: Optional[dict] = field(default_factory=dict)

    def __str__(self) -> str:
        # Does not serialize component work units; shallow copy.
        data = self.to_dict()
        return json.dumps(data, indent=4)

    # --------Serialization----------------------------------------------------

    def to_dict(self) -> dict:
        return {
            'dcc': self.dcc.value,
            'project': self.project,
            'role': self.role.value,
            'domain_details': self.domain_details.to_dict() if self.domain_details else None,
            'upstream_uid': self.upstream_uid,
            'task_name': self.task_name,
            'output_path': self.output_path.as_posix() if self.output_path else None,
            'uid': str(self.uid),
            'user': self.user,
            'components': {key: str(cls.uid) for key, cls in self.components.items()},
            'metadata': self.metadata or {}
        }

    @classmethod
    def from_dict(cls, data: dict, details_cls: Type[details.T_DOM_DETAILS]) -> 'WorkUnit':
        return cls(
            dcc=data['dcc'],
            project=data['project'],
            role=const.Role(data['role']),
            domain_details=details_cls.from_dict(data['domain_detail']) if data.get('domain_details') else None,
            upstream_uid=Path(data['upstream_uid']) if data.get('upstream_uid') else None,
            task_name=data['task_name'],
            output_path=Path(data['output_path']) if data.get('output_path') else None,
            uid=data['uid'],
            user=data['user'],
            # skipping components dict for now
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
        """Returns False if work unit has required fields that
        are unassigned.
        """
        for i in [self.project, self.role, self.task_name]:
            if i == const.UNASSIGNED:
                return False
            if isinstance(i, enum.Enum) and i.value == const.UNASSIGNED:
                return False

        return True

    def output_path_is_valid(self) -> bool:
        """Returns True/False if WU paths are valid."""
        if not self.output_path or not self.output_path.exists():
            raise FileNotFoundError(f'Invalid output: {self.output_path}')
        return True

    def validate_data(self) -> None:
        """Raises exceptions if unit tokens or domain detail tokens are
        invalid.
        """
        if not self.validate_tokens():
            raise exceptions.WorkUnitTokenException()
        if not self.domain_details.validate_tokens():
            raise exceptions.DomainDetailsTokenException()


# --------Database-------------------------------------------------------------

_Base = sqlalchemy.orm.declarative_base()

_echo_var = os.environ.get(const.ENV_SQLALCHEMY_ECHO, 'False').replace(';', '')
_ECHO: bool = _echo_var == 'True'

T_orm_str = sqlalchemy.orm.Mapped[str]


class UnitRecord(_Base):
    """The table class for work unit recording within the work database."""
    __tablename__ = 'wu_filepaths'
    unit_uid: T_orm_str = mapped_column(sqlalchemy.String(36), primary_key=True)
    filepath: T_orm_str = mapped_column(sqlalchemy.String, nullable=False)
    upstream_uid: T_orm_str = mapped_column(sqlalchemy.String(36), primary_key=True)


def _create_engine(database_url: Path) -> sqlalchemy.Engine:
    """Bind client session to database file."""
    if not Auth.systems_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    db_path = f'sqlite:///{database_url.resolve().as_posix()}'
    return sqlalchemy.create_engine(db_path, echo=_ECHO)


def create_database(database_url: Path) -> sqlalchemy.orm.Session:
    """Initializes the database and returns a session."""
    if not Auth.systems_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    engine = _create_engine(database_url)
    _Base.metadata.create_all(engine)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    return Session()


# TODO: Figure out how to move directory creation
io_utils.create_folder(project_paths.database_dir)
SESSION = create_database(project_paths.work_db_file)


def add_work_unit_to_db(wu: WorkUnit) -> None:
    """Adds a new file row to the database.

    Args:
        wu (WorkUnit): The work unit to log in the db.
    """
    if not Auth.artist_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    unit_id = wu.uid
    upstream_id = wu.upstream_uid
    output_path = wu.output_path.with_suffix('.json').as_posix()
    row = UnitRecord(
        unit_uid=str(unit_id),
        filepath=output_path,
        upstream_uid=upstream_id
    )
    SESSION.add(row)
    SESSION.commit()


def get_work_unit_filepath_by_uid(uid: str) -> Path:
    """Fetches the filepath for a work unit by its UID.

    Args:
        uid (str): The UID of the work unit.
    Returns:
        Path: The associated file path.
    Raises:
        KeyError: If no matching UID is found.
        InvalidPermissionLevelException: If permission is denied.
    """
    if not Auth.artist_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    record = SESSION.query(UnitRecord).filter(UnitRecord.unit_uid == uid).first()

    if not record:
        raise KeyError(f'No record found for UID: {uid}')

    return Path(record.filepath)


def get_source_chain(wu: WorkUnit) -> list[UnitRecord]:
    """Follows the upstream_uid chain for a given work unit.

    Args:
        wu (WorkUnit): The work unit to get upstream ids for.
    Returns:
        List[UnitRecord]: List of UnitRecords from the input UID up to the root.
            Ordered from most recent (start_uid) to the oldest (root).
    Raises:
        InvalidPermissionLevelException: If permission is denied.
    """
    if not Auth.artist_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    chain: list[UnitRecord] = []
    current_uid = wu.uid

    while current_uid:
        result = SESSION.query(UnitRecord).filter(UnitRecord.unit_uid == current_uid).first()
        if result is None:
            break

        chain.append(result())
        current_uid = result.upstream_uid

    return chain


def get_child_chain(root: Union[str, WorkUnit]) -> list[UnitRecord]:
    """Recursively finds all UnitRecords that descend from the given root UID.

    Args:
        root (Union[str, WorkUnit]): The string UID or WorkUnit to trace
         downstream from.
    Returns:
        List[UnitRecord]: All downstream UnitRecords in traversal order.
    Raises:
        InvalidPermissionLevelException: If permission is denied.
    """
    if not Auth.artist_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    if type(root) is str:
        root_uid = root
    elif type(root) is WorkUnit:
        root_uid = root.uid
    else:
        raise ValueError('Root given is not string uid or WorkUnit!')

    visited: set[str] = set()
    downstream: list[UnitRecord] = []

    def _traverse(uid: str) -> None:
        if uid in visited:
            return
        visited.add(uid)

        children = SESSION.query(UnitRecord).filter(UnitRecord.upstream_uid == uid).all()
        for child in children:
            downstream.append(child())
            _traverse(child.unit_uid)

    _traverse(root_uid)
    return downstream


def print_database_entries() -> None:
    """Prints all records from the 'wu_filepaths' table of the asset db.
    Raises:
        InvalidPermissionLevelException: If permission is denied.
    """
    if not Auth.artist_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    records = SESSION.query(UnitRecord).all()
    io_utils.print_center_header('Asset.db WU Filepaths')
    for record in records:
        print(f'Entry: {record.filepath}')
        print(f'\tunit_uid: {record.unit_uid}')
        print(f'\tdomain_type: {record.domain_type}')
        print(f'\tupstream_uid: {record.upstream_uid}')
    io_utils.print_center_header('-')


# --------Serialization--------------------------------------------------------

def load_work_unit(path: Path) -> WorkUnit:
    """Loads a WorkUnit from disk from a given JSON file.
    Will load all saved component's by uid in JSON file data.

    Args:
        path (Path): The path to the serialized WorkUnit JSON file.
    Returns:
        WorkUnit: The loaded WorkUnit instance.
    """
    if not path.is_file():
        raise FileNotFoundError(f'WorkUnit file does not exist: {path.as_posix()}')
    if not path.suffix == '.json':
        raise ValueError(f'Invalid WorkUnit file type: {path.as_posix()}')

    data = io_utils.import_data_from_json(path)

    role = data['role']
    details_cls: Type[details.T_DOM_DETAILS] = _DOMAIN_MAPPINGS[role]()
    cur_unit = WorkUnit.from_dict(data, details_cls)

    comp_data = data.get('components', {})
    for key, comp_uid in comp_data.items():
        comp_header = key.split('.')[0]
        attach_method = _ATTACH_FUNCS[comp_header]
        comp_filepath = get_work_unit_filepath_by_uid(comp_uid)
        comp_unit = load_work_unit(comp_filepath)
        attach_method(cur_unit, comp_unit)

    return cur_unit


def save_work_unit(wu: WorkUnit) -> None:
    """Serializes a WorkUnit and saves it to disk.
    This creates a 'shallow' work unit dict, saving components by uid.

    Args:
        wu (WorkUnit): The work unit to serialize.
    """
    data = wu.to_dict()
    io_utils.export_data_to_json(wu.output_path.with_suffix('.json'), data)
    add_work_unit_to_db(wu)

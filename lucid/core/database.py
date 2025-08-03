"""
# Lucid Database Management

* Description:

    Primary database management library.
"""


import os
from pathlib import Path

import sqlalchemy
import sqlalchemy.orm

from lucid.core import const
from lucid.core import exceptions
from lucid.core import io_utils
from lucid.core import project_paths
from lucid.core import work
from lucid.core.auth import Auth


_Base = sqlalchemy.orm.declarative_base()

_echo_var = const.ENV_SQLALCHEMY_ECHO
_ECHO: bool = os.environ.get(_echo_var, 'False').replace(';', '') == 'True'


class FileRecord(_Base):
    __tablename__ = 'wu_filepaths'

    uid = sqlalchemy.Column(sqlalchemy.String(36), primary_key=True)
    filepath = sqlalchemy.Column(sqlalchemy.String, nullable=False)


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


io_utils.create_folder(project_paths.DATABASE_DIR)
SESSION = create_database(project_paths.ASSET_DB_FILE)


def add_work_unit_filepath(wu: work.WorkUnit) -> None:
    """Adds a new file row to the database.

    Args:
        wu (WorkUnit): The work unit to log in the db.
    """
    if not Auth.artist_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    unit_id, output_path = wu.uid, wu.output_path.with_suffix('.json')
    row = FileRecord(uid=str(unit_id), filepath=output_path.as_posix())
    SESSION.add(row)
    SESSION.commit()


def print_work_unit_filepaths() -> None:
    """Prints all records from the 'wu_filepaths' table of the asset db."""
    if not Auth.artist_or_higher():
        raise exceptions.InvalidPermissionLevelException()

    records = SESSION.query(FileRecord).all()
    io_utils.print_center_header('Asset.db WU Filepaths')
    for record in records:
        print(f'uid: {record.uid}, filepath: {record.filepath}')

"""
# Model Domain Pipeline

* Description:

    Base class for all model pipelines.
    This handles model database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from dataclasses import dataclass
from pathlib import Path

import lucid.const
import lucid.event_broker
import lucid.exceptions
import lucid.work
from lucid import details
from lucid.pipelines.asset import AssetDetails
from lucid.pipelines.asset import AssetPipeline


@enum.unique
class ModelCategory(enum.Enum):
    UNASSIGNED = lucid.const.UNASSIGNED
    VEH = 'VEH'
    CHAR = 'CHAR'
    PROP = 'PROP'
    CREATURE = 'CREA'
    ENV = 'ENV'
    FOLIAGE = 'FOLIAGE'


@dataclass
class ModelDetails(AssetDetails):
    category: ModelCategory = ModelCategory.UNASSIGNED
    lod: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'ModelDetails':
        return cls(
            data['base_name'],
            data['variation'],
            data['version'],
            data['file_type'],
            ModelCategory[data['category']],
            data['lod']
        )


class ModelPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

    @classmethod
    def to_filename(cls, unit: lucid.work.WorkUnit) -> str:
        """Returns filename based on version. Master if version is None, else
        versioned file name. Adds Variation if one is present.
        Details that do not pass token validation will raise an exception.
        """
        if not unit.domain_details.validate_tokens():
            raise lucid.exceptions.DomainDetailsTokenError()

        d = details.verify_domain_details(
            lucid.pipelines.asset.AssetDetails,
            unit.domain_details
        )

        parts = [d.base_name]
        if not d.variation == lucid.const.UNASSIGNED:
            parts.append(d.variation)
        if d.version is not None:
            parts.append(str(d.version).zfill(lucid.const.VERSION_PADDING))

        name_stem = '_'.join(parts)

        return f'{name_stem}.{d.file_type}'

    @classmethod
    def _generate_output_path(cls, unit: lucid.work.WorkUnit) -> Path:
        if not unit.validate_tokens():
            raise lucid.exceptions.WorkUnitTokenError()
        if not unit.domain_details.validate_tokens():
            raise lucid.exceptions.DomainDetailsTokenError()

        details = lucid.work.verify_domain_details(
            lucid.pipelines.asset.AssetDetails,
            unit.domain_details
        )

        return Path(
            lucid.const.PROJ_PATH,
            unit.project,
            'asset',
            unit.domain.value,
            details.base_name,
            details.file_type,
            str(details.version),
            cls.to_filename(unit)
        )

    @classmethod
    def dcc_publish(cls, unit: lucid.work.WorkUnit) -> None:
        unit.output_path = cls._generate_output_path(unit)
        lucid.event_broker.trigger_event(unit)

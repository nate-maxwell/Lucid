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

import lucid.core.const
import lucid.core.event_broker
import lucid.core.exceptions
import lucid.core.work
from lucid.core import details
from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline


@enum.unique
class ModelCategory(enum.Enum):
    UNASSIGNED = lucid.core.const.UNASSIGNED
    VEH = 'VEH'
    CHAR = 'CHAR'
    PROP = 'PROP'
    CREATURE = 'CREA'
    ENV = 'ENV'


@dataclass
class ModelDetails(AssetDetails):
    category: ModelCategory = ModelCategory.UNASSIGNED
    lod: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'ModelDetails':
        return cls(
            domain_name=data['domain_name'],
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            category=ModelCategory[data['category']],
            lod=data['lod']
        )


class ModelPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: lucid.core.work.WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

    @classmethod
    def to_filename(cls, unit: lucid.core.work.WorkUnit) -> str:
        """Returns filename based on version. Master if version is None, else
        versioned file name. Adds Variation if one is present.
        Details that do not pass token validation will raise an exception.
        """
        if not unit.domain_details.validate_tokens():
            raise lucid.core.exceptions.DomainDetailsTokenException()

        d = details.verify_details_type(
            lucid.core.pipeline.asset.AssetDetails,
            unit.domain_details
        )

        parts = [d.base_name]
        if not d.variation == lucid.core.const.UNASSIGNED:
            parts.append(d.variation)
        if d.version is not None:
            parts.append(str(d.version).zfill(lucid.core.const.VERSION_PADDING))

        name_stem = '_'.join(parts)

        return f'{name_stem}.{d.file_type}'

    @classmethod
    def generate_output_path(cls, unit: lucid.core.work.WorkUnit) -> Path:
        unit.validate_data()

        d = lucid.core.details.verify_details_type(
            lucid.core.pipeline.asset.AssetDetails,
            unit.domain_details
        )

        return Path(
            lucid.core.const.PROJECTS_DIR,
            unit.project,
            'asset',
            unit.domain_details.domain_name.value,
            d.base_name,
            d.file_type,
            str(d.version),
            cls.to_filename(unit)
        )

    @classmethod
    def dcc_publish(cls, unit: lucid.core.work.WorkUnit) -> None:
        unit.output_path = cls.generate_output_path(unit)
        lucid.core.event_broker.emit(unit)

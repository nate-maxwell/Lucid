"""
# Model Domain Pipeline

* Description:

    Base class for all model pipelines.
    This handles model database registration.
    DCCs must implement application API specific file IO.
"""


import enum
from pathlib import Path

import lucid.core.broker
import lucid.core.const
import lucid.core.exceptions
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core import details
from lucid.core.work import WorkUnit


class ModelPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

    @classmethod
    def to_filename(cls, wu: WorkUnit) -> str:
        """Returns filename based on version. Master if version is None, else
        versioned file name. Adds Variation if one is present.
        Details that do not pass token validation will raise an exception.
        """
        if not wu.domain_details.validate_tokens():
            raise lucid.core.exceptions.DomainDetailsTokenException()

        d = details.verify_details_type(
            details.AssetDetails,
            wu.domain_details
        )

        parts = [d.base_name]
        if not d.variation == lucid.core.const.UNASSIGNED:
            parts.append(d.variation)
        if d.version is not None:
            parts.append(str(d.version).zfill(lucid.core.const.VERSION_PADDING))

        name_stem = '_'.join(parts)

        return f'{name_stem}.{d.file_type}'

    @classmethod
    def generate_output_path(cls, wu: WorkUnit) -> Path:
        wu.validate_data()

        d = details.verify_details_type(
            details.AssetDetails,
            wu.domain_details
        )

        return Path(
            lucid.core.const.PROJECTS_DIR,
            wu.project,
            'asset',
            wu.domain_details.domain_name.value,
            d.base_name,
            d.file_type,
            str(d.version),
            cls.to_filename(wu)
        )

    @classmethod
    def dcc_publish(cls, wu: WorkUnit) -> None:
        wu.output_path = cls.generate_output_path(wu)
        lucid.core.broker.emit(wu)

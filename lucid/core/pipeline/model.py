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
from typing import cast

import lucid.core.broker
import lucid.core.exceptions
from lucid.core import const
from lucid.core import details
from lucid.core import project_paths
from lucid.core import work
from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


# --------Model Details--------------------------------------------------------

@enum.unique
class ModelCategory(enum.Enum):
    VEH = 'VEH'
    CHAR = 'CHAR'
    PROP = 'PROP'
    CREATURE = 'CREA'
    ENV = 'ENV'
    UNASSIGNED = const.UNASSIGNED


@dataclass
class ModelDetails(AssetDetails):
    rigged: bool = False
    category: ModelCategory = ModelCategory.UNASSIGNED
    lod: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> 'ModelDetails':
        return cls(
            base_name=data['base_name'],
            variation=data['variation'],
            version=data['version'],
            file_type=data['file_type'],
            rigged=data['rigged'],
            category=ModelCategory(data['category']),
            lod=data['lod']
        )


# --------Pipeline Object------------------------------------------------------

class ModelPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

    @classmethod
    def attach_model(cls, parent_wu: WorkUnit, model_wu: WorkUnit) -> None:
        d = cast(ModelDetails, model_wu.domain_details)
        prefix = const.Role.MODEL.value
        parent_wu.components[f'{prefix}.{d.base_name}'] = model_wu

    @classmethod
    def get_model(cls, parent_wu: WorkUnit) -> WorkUnit:
        # TODO: This should probably be gotten through schema or concept work unit.
        raise NotImplemented

    @classmethod
    def to_filename(cls, wu: WorkUnit) -> str:
        """Returns filename based on version. Master if version is None, else
        versioned file name. Adds Variation if one is present.
        Details that do not pass token validation will raise an exception.
        """
        if not wu.domain_details.validate_tokens():
            raise lucid.core.exceptions.DomainDetailsTokenException()

        d = details.verify_details_type(
            AssetDetails,
            wu.domain_details
        )

        parts = [d.base_name]
        if not d.variation == const.UNASSIGNED:
            parts.append(d.variation)
        if d.version is not None:
            parts.append(str(d.version).zfill(const.VERSION_PADDING))

        name_stem = '_'.join(parts)

        return f'{name_stem}.{d.file_type}'

    @classmethod
    def generate_output_path(cls, wu: WorkUnit) -> Path:
        wu.validate_data()

        d = details.verify_details_type(
            AssetDetails,
            wu.domain_details
        )

        return Path(
            project_paths.work_dir,
            wu.role.value.lower(),
            d.base_name,
            d.file_type,
            str(d.version),
            cls.to_filename(wu)
        )

    @classmethod
    def dcc_publish(cls, wu: WorkUnit) -> None:
        wu.output_path = cls.generate_output_path(wu)
        lucid.core.broker.emit(wu)


work.register_attach_method(namespace=const.Role.MODEL.value,
                            method=ModelPipeline.attach_model,
                            domain_cls=ModelDetails)

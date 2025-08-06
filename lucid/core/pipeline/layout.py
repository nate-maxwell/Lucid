"""
# Layout Domain Pipeline

* Description:

    Base class for all layout pipelines.
    This handles layout database registration.
    DCCs must implement application API specific file IO.
"""


from dataclasses import dataclass

from lucid.core.pipeline.asset import AssetDetails
from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


@dataclass
class LayoutDetails(AssetDetails):

    @classmethod
    def from_dict(cls, data: dict) -> 'LayoutDetails':
        return cls()


class LayoutPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

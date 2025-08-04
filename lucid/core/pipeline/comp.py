"""
# Compositing Domain Pipeline

* Description:

    Base class for all compositing pipelines.
    This handles composite database registration.
    DCCs must implement application API specific file IO.
"""


from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


class CompositingPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

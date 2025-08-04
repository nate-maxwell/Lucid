"""
# Rigging Domain Pipeline

* Description:

    Base class for all rigging pipelines.
    This handles rigging database registration.
    DCCs must implement application API specific file IO.
"""


from lucid.core.pipeline.asset import AssetPipeline
from lucid.core.work import WorkUnit


class RiggingPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, wu: WorkUnit) -> None:
        print(f'Registering file: {wu.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(wu.to_dict())}')

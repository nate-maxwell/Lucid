"""
# Layout Domain Pipeline

* Description:

    Base class for all layout pipelines.
    This handles layout database registration.
    DCCs must implement application API specific file IO.
"""


from lucid.pipelines.asset import AssetPipeline
from lucid.work import WorkUnit


class LayoutPipeline(AssetPipeline):

    @classmethod
    def register_in_database(cls, uow: WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print(f'Registering data: {cls.pretty_format_dict(uow.to_dict())}')

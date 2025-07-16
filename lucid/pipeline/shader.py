"""
# Shader Domain Pipeline

* Description:

    Base class for all shader pipelines.
    This handles shader database registration.
    DCCs must implement application API specific file IO.
"""


from lucid.pipeline.base import Pipeline
from lucid.work import WorkUnit


class ShaderPipeline(Pipeline):

    @classmethod
    def register_in_database(cls, uow: WorkUnit) -> None:
        print(f'Registering file: {uow.output_path.as_posix()}')
        print()
        print(f'Registering data: {uow.to_dict()}')

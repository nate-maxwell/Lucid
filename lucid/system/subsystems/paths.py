"""
# File Path Subsystem

* Description:

    Understood file paths of the opened file based on current context values.
"""


import sys
import types
from pathlib import Path

from lucid import const
from lucid import exceptions
from lucid import io_utils
from lucid.system.subsystems import context
from lucid.system.subsystems import context_object


_templates = {
    const.Role.MODEL: '{project}/asset/{category}/{set}/{name}/model/{lod}/{dcc}/{ext}/{filename}',
    const.Role.RIG: '{project}/asset/{category}/{set}/{name}/rig/{dcc}/{ext}/{filename}',
    const.Role.TEXTURE: '{project}/asset/{category}/{set}/{name}/texture/{lod}/{dcc}/{ext}/{filename}',
    const.Role.ANIM: '{project}/anim/{category}/{set}/{name}/{direction}/{dcc}/{ext}/{filename}',
    const.Role.COMP: const.UNASSIGNED
}


class _ModuleType(types.ModuleType):
    """Path management service. Generates paths from current context tokens."""

    def __init__(self) -> None:
        super().__init__(sys.modules[__name__].__name__)
        io_utils.print_lucid_msg('Enabling Subsystem: Path Management')

    @staticmethod
    def get_path_from_context(ctx: context_object.LucidContext) -> Path:
        template = _templates[ctx.role]
        roles = const.Role

        if ctx.role == roles.MODEL:
            subcon = context.verify_subcontext(context_object.ModelContext, ctx.subcontext)
            rel_path = template.format(project=ctx.project, category=subcon.category,
                                       set=subcon.set, name=subcon.name, lod=f'lod{subcon.lod}',
                                       dcc=ctx.dcc, ext=subcon.ext, filename=subcon.filename)
        elif ctx.role == roles.RIG:
            subcon = context.verify_subcontext(context_object.RigContext, ctx.subcontext)
            rel_path = template.format(project=ctx.project, category=subcon.category,
                                       set=subcon.set, name=subcon.name,
                                       dcc=ctx.dcc, ext=subcon.ext,
                                       filename=subcon.filename)
        elif ctx.role == roles.TEXTURE:
            subcon = context.verify_subcontext(context_object.TextureContext, ctx.subcontext)
            rel_path = template.format(project=ctx.project, category=subcon.category,
                                       set=subcon.set, name=subcon.name, lod=f'lod{subcon.lod}',
                                       dcc=ctx.dcc, ext=subcon.ext, filename=subcon.filename)
        elif ctx.role == roles.ANIM:
            subcon = context.verify_subcontext(context_object.AnimContext, ctx.subcontext)
            rel_path = template.format(project=ctx.project, category=subcon.category,
                                       set=subcon.set, name=subcon.name,
                                       direction=subcon.direction, dcc=ctx.dcc, ext=subcon.ext,
                                       filename=subcon.filename)
        elif ctx.role == roles.COMP:
            raise NotImplemented
        else:
            raise exceptions.SubContextError('Could not determine subcontext.')

        return Path(const.PROJ_PATH, rel_path)

    @property
    def context_path(self) -> Path:
        return self.get_path_from_context(context.current_context)


# This is here to protect path schema dict.
sys.modules[__name__] = _ModuleType()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Required for static type checkers to accept these names as members of this module
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

context_path: Path


def get_path_from_context(ctx: context_object.LucidContext) -> Path:
    """Builds a path from the given context.
    Raises a SubContextError if one could not be built.
    """

"""
# Asset Builder

* Description:

    A system for orchestrating work units and their work unit components.

    This system ensures that component work units are added to parent work
    units in an organized and predictable fashion, and eliminates the
    necessity for memorizing raw string key names.
"""


from typing import cast

from lucid.core.work.unit import WorkUnit
from lucid.core.work import details


def attach_shader(model_wu: WorkUnit, shader_wu: WorkUnit) -> None:
    d = cast(details.ShaderDetails, shader_wu.domain_details)
    model_wu.components[f'shader.{d.base_name}'] = shader_wu


def get_shader(model_wu: WorkUnit, shader_base_name: str) -> WorkUnit:
    return model_wu.components[f'shader.{shader_base_name}']


def attach_texture(shader_wu: WorkUnit, texture_wu: WorkUnit) -> None:
    d = cast(details.TextureDetails, texture_wu.domain_details)
    shader_wu.components[f'texture.{d.texture_type.value}'] = texture_wu


def get_texture(shader_wu: WorkUnit,
                texture_type: details.TextureType) -> WorkUnit:
    return shader_wu.components[f'texture.{texture_type.value}']

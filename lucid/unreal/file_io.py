"""
# Unreal Import

* Description:

    Import functions for assets into unreal.

* Notes:

    Most import option values are currently hard-coded but could easily be hooked up to UI.

* UE Path types:

    !Seriously, why does UE have so many path types?

    Display Name & Asset Name = AssetName
    Path Name & Object Path   = /Game/dir/dir/AssetName.AssetName
    Package Path              = /Game/dir/dir
    Package Name              = /Game/dir/dir/AssetName
"""


import collections
from dataclasses import dataclass
from functools import partial
from typing import cast
from typing import Optional
from typing import TypeVar
from pathlib import Path

import unreal

from lucid.unreal import short


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Import options and task fat structs
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class ImportAssetOptions(object):
    """Lucid import options - The import settings used when importing an asset
    into the engine.

    An ImportAssetOptions is a component of 'ImportTaskOptions' and used to
    define the asset type specific attributes on import.
    """


@dataclass
class ImportSMOptions(ImportAssetOptions):
    """Lucid Options object used to define how a static mesh will be imported
    into the engine.
    """
    loc: unreal.Vector = (0.0, 0.0, 0.0)
    rot: unreal.Rotator = (0.0, 0.0, 0.0)
    scale: float = 1.0
    merge: bool = True
    remove_degenerates: bool = False
    generate_lightmaps: bool = True
    auto_gen_collisions: bool = True
    normal_gen_method: short.fbx_normal_gen_method = short.fbx_normal_mikk_t_space
    normal_import_method: short.fbx_normal_imp_method = short.fbx_import_normals_tangents
    one_convex_hull: bool = False


@dataclass
class ImportSKOptions(ImportAssetOptions):
    """Lucid options object used to define how a skeletal mesh will be imported
    into the engine.
    """
    skeleton: Optional[unreal.Skeleton] = None
    loc: unreal.Vector = (0.0, 0.0, 0.0)
    rot: unreal.Rotator = (0.0, 0.0, 0.0)
    scale: float = 1.0
    create_physics_asset: bool = False
    import_morph_targets: bool = True
    preserve_smoothing_groups: bool = True
    convert_scene: bool = True
    normal_gen_method: short.fbx_normal_gen_method = short.fbx_normal_mikk_t_space
    normal_import_method: short.fbx_normal_imp_method = short.fbx_import_normals_tangents


@dataclass
class ImportAnimOptions(ImportAssetOptions):
    """Lucid options object used to define how an animation will be imported
    into the engine.
    """
    skeleton: unreal.Skeleton
    fps: int = 30
    loc: unreal.Vector = (0.0, 0.0, 0.0)
    rot: unreal.Rotator = (0.0, 0.0, 0.0)
    scale: float = 1.0
    convert_scene: bool = True
    del_morph_targets: bool = False


@dataclass
class ImportTextureOptions(ImportAssetOptions):
    """Lucid options object used to define how a texture will be imported
    into the engine.
    """
    compression_override: int = 0
    """Override value for the texture compression settings.
    If non-zero, this value will be used instead of the default compression
    settings inferred from the source file name suffix. Defaults to 0.
    """


T_ImportAssetOptions = TypeVar('T_ImportAssetOptions', bound=ImportAssetOptions)


@dataclass
class ImportTaskOptions(object):
    """Lucid Options object used to define an unreal.AssetImportTask."""
    options: T_ImportAssetOptions
    source_path: Path
    destination_package_path: str
    import_name: str = ''
    reimport: bool = True


def import_static_mesh(task: ImportTaskOptions) -> str:
    """
    Imports a static mesh asset into Unreal Engine.

    Args:
        task (ImportTaskOptions): The task options defining how to import the
         static mesh.
    Returns:
        str: The path name of the imported asset.
    """
    fbx_ui_options = _import_sm_options(task.options)
    static_mesh = _import_task(task, fbx_ui_options)
    asset_task = _execute_import_tasks([static_mesh])

    return asset_task[0]


def import_skeletal_mesh(task: ImportTaskOptions) -> str:
    """
    Imports a skeletal mesh asset into Unreal Engine.

    Args:
        task (ImportTaskOptions): The task options defining how to import the
         static mesh.
    Returns:
        str: The path name of the imported asset.
    """
    fbx_ui_options = _import_sk_options(task.options)
    skeletal_mesh = _import_task(task, fbx_ui_options)
    asset_task = _execute_import_tasks([skeletal_mesh])

    return asset_task[0]


def import_animation(task: ImportTaskOptions) -> str:
    """
    Imports a skeletal mesh animation into Unreal Engine.

    Args:
        task (ImportTaskOptions): The task options defining how to import the
         static mesh.
    Returns:
        str: The path name of the imported asset.
    """
    fbx_ui_options = _import_anim_options(task.options)
    anim = _import_task(task, fbx_ui_options)
    anim_task = _execute_import_tasks([anim])

    return anim_task[0]


def import_texture(task: ImportTaskOptions) -> str:
    """
    Imports a texture asset into Unreal Engine from the given source file path.

    Notes:
        The compression settings for the imported texture are set based on the suffix of the source
        file name, unless a compression_override value is provided.

        The following suffixes are recognized:
            - '_BC' : sRGB color space
            - '_N'  : normal map
            - '_ORM': non-sRGB color space
            - other : default compression settings
    Args:
        task (ImportTaskOptions): The task options defining how to import the
         static mesh.
    Returns:
        str: The path name of the imported asset.
    """
    file_name = task.source_path.as_posix().split('/')[-1].split('.')[0]
    texture = _import_task(task)

    unreal_path = _execute_import_tasks([texture])[0]
    asset = unreal.load_asset(str(unreal_path))

    # Texture type settings
    compression_val = task.options.compression_override
    if compression_val:
        asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.cast(compression_val))
    else:
        if file_name.endswith('_BC'):
            asset.set_editor_property('srgb', True)
        elif file_name.endswith('_N'):
            asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_NORMALMAP)
        elif file_name.endswith('_ORM'):
            asset.set_editor_property('srgb', False)
        else:
            asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_DEFAULT)

    unreal.EditorAssetLibrary.save_asset(unreal_path, True)

    return unreal_path


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Import task declaration and execution
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def _import_task(
        task: ImportTaskOptions,
        options: Optional[unreal.FbxImportUI] = None
) -> unreal.AssetImportTask:
    """
    Sets the import task settings when importing an asset.

    Args:
        task (ImportTaskOptions): The task options defining how to import the
         static mesh.
    Returns:
        unreal.AssetImportTask: The asset import task with the specified settings.
    """
    ue_task = unreal.AssetImportTask()

    # Task settings
    ue_task.set_editor_property('automated', True)
    ue_task.set_editor_property('destination_name', task.import_name)
    ue_task.set_editor_property('destination_path', task.destination_package_path)
    ue_task.set_editor_property('filename', task.source_path.as_posix())
    ue_task.set_editor_property('replace_existing', task.reimport)
    ue_task.set_editor_property('save', True)

    # Additional settings
    ue_task.set_editor_property('options', options)

    return ue_task


def _execute_import_tasks(import_tasks: list[unreal.AssetImportTask]) -> list:
    """
    Imports a single asset from disk in Unreal.

    Args:
        import_tasks (unreal.AssetImportTask): The import task settings for the asset to

        be imported. Function will convert list[unreal.AssetImportTask] to

        unreal.Array(unreal.AssetImportTask).

    Returns:
        list: The file paths of the imported assets.
    """
    is_reload = []
    tasks = unreal.Array(unreal.AssetImportTask)

    for i in import_tasks:
        # Convert list of import tasks to unreal.Array of import tasks
        # and mark the pre-existing assets as re-imported for log.
        tasks.append(i)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    asset_paths = []
    for i in import_tasks:
        paths = cast(collections.Iterable, i.get_editor_property('imported_object_paths'))
        for path in paths:
            asset_paths.append(path)
            if not path.split('.')[0] in is_reload:
                unreal.log_warning(f'\nImported: {path}\n')
            else:
                unreal.log_warning(f'\nReImported: {path}s\n')

    return asset_paths


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Import options by import type
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def _import_sm_options(options: ImportSMOptions) -> unreal.FbxImportUI:
    """
    Creates the import options for static meshes.

    Args:
        options (ImportSMOptions): The import options object with static mesh
         editor properties.

    Returns:
        unreal.FbxImportUI: The import options for the static mesh.
    """
    ui_options = unreal.FbxImportUI()

    # FBX generic import data
    ui_options.set_editor_property('import_mesh', True)
    ui_options.set_editor_property('import_textures', True)
    ui_options.set_editor_property('import_materials', True)
    ui_options.set_editor_property('import_as_skeletal', False)
    ui_options.set_editor_property('import_animations', False)
    ui_options.set_editor_property('create_physics_asset', False)

    # FBX mesh import data
    _set_property = partial(short.set_staticmesh_property, ui_options)
    _set_property('import_translation', options.loc)
    _set_property('import_rotation', options.rot)
    _set_property('import_uniform_scale', options.scale)
    _set_property('combine_meshes', options.merge)
    _set_property('remove_degenerates', options.remove_degenerates)
    _set_property('generate_lightmap_u_vs', options.generate_lightmaps)
    _set_property('auto_generate_collision', options.auto_gen_collisions)
    _set_property('convert_scene', True)
    _set_property('force_front_x_axis', False)
    _set_property('convert_scene_unit', False)
    _set_property('normal_generation_method', options.normal_gen_method)
    _set_property('normal_import_method', options.normal_import_method)
    _set_property('one_convex_hull_per_ucx', options.one_convex_hull)
    _set_property('transform_vertex_to_absolute', True)
    _set_property('build_reversed_index_buffer', True)

    unreal.log('IMPORTING STATIC MESH')

    return ui_options


def _import_sk_options(options: ImportSKOptions) -> unreal.FbxImportUI:
    """
    Creates the import options for skeletal meshes.

    Args:
        options (ImportSKOptions): The task options defining how to import the
         skeletal mesh.
    Returns:
        unreal.FbxImportUI: The import options for the skeletal mesh.
    """
    ui_options = unreal.FbxImportUI()

    # Fbx generic import data
    ui_options.set_editor_property('import_mesh', True)
    ui_options.set_editor_property('import_textures', True)
    ui_options.set_editor_property('import_materials', True)
    ui_options.set_editor_property('import_as_skeletal', True)
    ui_options.set_editor_property('import_animations', False)
    ui_options.set_editor_property('create_physics_asset', options.create_physics_asset)

    # Fbx skeletal import data
    _set_property = partial(short.set_skel_property, ui_options)
    _set_property('import_translation', options.loc)
    _set_property('import_rotation', options.rot)
    _set_property('import_uniform_scale', options.scale)
    _set_property('import_morph_targets', options.import_morph_targets)
    _set_property('use_t0_as_ref_pose', True)
    _set_property('preserve_smoothing_groups', options.preserve_smoothing_groups)
    _set_property('import_meshes_in_bone_hierarchy', True)
    _set_property('threshold_position', 0.00002)
    _set_property('threshold_tangent_normal', 0.00002)
    _set_property('threshold_uv', 0.000977)
    _set_property('convert_scene', options.convert_scene)
    _set_property('force_front_x_axis', False)
    _set_property('convert_scene_unit', False)
    _set_property('transform_vertex_to_absolute', True)
    _set_property('normal_generation_method', options.normal_gen_method)
    _set_property('normal_import_method', options.normal_import_method)

    # Skeleton for imported mesh, if none specified, import skeleton in fbx
    if options.skeleton:
        ui_options.skeleton = options.skeleton

    unreal.log('IMPORTING SKEL MESH')

    return ui_options


def _import_anim_options(options: ImportAnimOptions) -> unreal.FbxImportUI:
    """
    Import options for skel mesh animations. Will import skeleton in fbx if none provided.

    Args:
        options (ImportAnimOptions): The task options defining how to import the
         animation.
    Returns:
        unreal.FbxImportUI: The import options for the skeletal mesh animation.
    """
    ui_options = unreal.FbxImportUI()

    # Fbx generic import data
    ui_options.set_editor_property('import_animations', True)
    ui_options.set_editor_property('import_materials', False)
    ui_options.set_editor_property('import_textures', False)
    ui_options.set_editor_property('create_physics_asset', False)

    if options.skeleton:
        ui_options.set_editor_property('import_mesh', False)
        ui_options.skeleton = options.skeleton
    else:
        ui_options.set_editor_property('import_mesh', True)
        short.set_skel_property(ui_options, 'import_morph_targets', True)

    if options.fps != 30:
        short.set_anim_property(ui_options, 'use_default_sample_rate', False)
    else:
        short.set_anim_property(ui_options, 'use_default_sample_rate', True)

    _set_property = partial(short.set_skel_property, ui_options)

    # Fbx skel mesh import data
    _set_property('import_translation', options.loc)
    _set_property('import_rotation', options.rot)
    _set_property('import_uniform_scale', options.scale)
    _set_property('convert_scene', options.convert_scene)
    _set_property('force_front_x_axis', False)
    _set_property('convert_scene_unit', False)
    _set_property('import_meshes_in_bone_hierarchy', True)

    # Fbx anim sequence import data
    _set_property('delete_existing_morph_target_curves', options.del_morph_targets)
    _set_property('import_custom_attribute', True)
    _set_property('import_bone_tracks', True)
    _set_property('custom_sample_rate', options.fps)
    _set_property('do_not_import_curve_with_zero', True)
    _set_property('remove_redundant_keys', True)
    _set_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)

    unreal.log('IMPORTING SKELETAL MESH ANIMATION')

    return ui_options

"""
# Unreal Import

* Description:

    Import functions for assets/animations into unreal.

* Notes:

    Most import option values are currently hard-coded but could easily be hooked up to UI.

    This file would have been called io.py but that name seems to be reserved in Unreal,
    causing it to crash if found on the path on startup.

* UE Path types:

    ! Seriously why does UE have so many path 'types'?

    Display Name & Asset Name = AssetName
    Path Name & Object Path   = /Game/dir/dir/AssetName.AssetName
    Package Path              = /Game/dir/dir
    Package Name              = /Game/dir/dir/AssetName
"""


import functools
from typing import Optional

import unreal

from lucid import const
from lucid.unreal import asset_messages
from lucid.unreal import ImportTask


# ----------Shorthands-----------------------------------------------------------------------------

# The unreal module has very large names for functions.
# Some of which have been shorthanded, or aliased, here.

# -----Functions-----

def _set_skel_property(import_options: unreal.FbxImportUI, string_name: str, value=None) -> None:
    """Simple to type func to set skel mesh import option."""
    import_options.skeletal_mesh_import_data.set_editor_property(string_name, value)


def _set_sm_property(import_options: unreal.FbxImportUI, string_name: str, value=None) -> None:
    """Simple to type func to set static mesh import option."""
    import_options.static_mesh_import_data.set_editor_property(string_name, value)


def _set_anim_property(import_options: unreal.FbxImportUI, string_name: str, value=None) -> None:
    """Simple to type func to set skel anim import options."""
    import_options.anim_sequence_import_data.set_editor_property(string_name, value)


# -----Variable Types-----

NORMAL_GEN_METHOD = unreal.FBXNormalGenerationMethod
NORMAL_IMP_METHOD = unreal.FBXNormalImportMethod


# ----------Primary Import Functions---------------------------------------------------------------

def import_static_mesh(message: asset_messages.ImportSMAsset) -> str:
    """
    Imports a static mesh asset into Unreal Engine.

    Args:
        message (ImportSMAsset): The ImportSMAsset command containing all
         relevant values.
    Returns:
        str: The path name fo the imported asset.
    """
    options = _import_sm_options(message)
    static_mesh = _import_task(options, message.body.import_task)
    asset_task = _execute_import_tasks([static_mesh])

    return asset_task[0]


def import_skeletal_mesh(message: asset_messages.ImportSKAsset) -> str:
    """
    Imports a skeletal mesh asset into Unreal Engine.

    Args:
        message (ImportSKAsset): The ImportSKAsset command containing all
         relevant values.

    Returns:
        str: The path name fo the imported asset.
    """
    options = _import_sk_options(message)
    skeletal_mesh = _import_task(options, message.body.import_task)
    asset_task = _execute_import_tasks([skeletal_mesh])

    return asset_task[0]


def import_animation(message: asset_messages.ImportAnim) -> str:
    """
    Imports a skeletal mesh animation into Unreal Engine.

    Args:
        message (ImportAnim): The ImportAnim command containing all
         relevant values.

    Returns:
        str: The path name fo the imported asset.
    """
    options = _import_anim_options(message)
    anim = _import_task(options, message.body.import_task)
    anim_task = _execute_import_tasks([anim])

    return anim_task[0]


def import_texture(message: asset_messages.ImportTexture) -> str:
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
        message (ImportTexture): The ImportTexture command containing all
         relevant values.

    Returns:
        str: The path name fo the imported asset.
    """
    file_name = message.body.import_task.source_path.split('/')[-1].split('.')[0]
    texture = _import_task(None, message.body.import_task)

    unreal_path = _execute_import_tasks([texture])[0]
    asset = unreal.load_asset(unreal_path)

    # Texture type settings
    if message.body.compression_override:
        override = message.body.compression_override
        val = unreal.TextureCompressionSettings.cast(override)
        asset.set_editor_property('compression_settings', val)
    else:
        if file_name.endswith(const.SUFFIX_BASECOLOR):
            asset.set_editor_property('srgb', True)
        elif file_name.endswith(const.SUFFIX_NORMAL):
            asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_NORMALMAP)
        elif file_name.endswith(const.SUFFIX_CHANNEL_PACKED):
            asset.set_editor_property('srgb', False)
        else:
            asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_DEFAULT)

    unreal.EditorAssetLibrary.save_asset(unreal_path, True)

    return unreal_path


def import_texture_batch(message: asset_messages.BatchImportTextures):
    """
    Batch importer for multiple textures in TGA format.

    This function imports multiple textures from the given source directory and
    saves them as Unreal Engine assets in the given destination directory.

    Notes:
        - This function calls the import_texture function for each texture in the texture_list,
        using the same reimport argument for all imports.

        - The texture files in the source directory should be in TGA format and named after
        their corresponding asset name (without extension).

    Args:
        message (BatchImportTextures): The BatchImportTextures command containing all
         relevant values.
    """
    for body in message.body.textures:
        import_texture(body)


# ----------Import Tasks---------------------------------------------------------------------------

def _import_task(options: Optional[unreal.FbxImportUI], import_task: ImportTask) -> unreal.AssetImportTask:
    """
    Sets the import task settings when importing an asset.

    Args:
        options (Optional[unreal.FbxImportUI]): The import options for the asset.
         Can be set to None if importing textures or other objects that do not
         use the fbx import ui.
        import_task (lucid.unreal.ImportTask): The task object for asset path
         management.

    Returns:
        unreal.AssetImportTask: The asset import task with the specified settings.
    """
    engine_task = unreal.AssetImportTask()

    # Task settings
    _set = engine_task.set_editor_property
    _set('automated', True)
    _set('destination_name', import_task.import_name)
    _set('destination_path', import_task.destination_package_path.as_posix())
    _set('filename', import_task.source_path.as_posix())
    _set('replace_existing', import_task.reimport)
    _set('save', True)

    # Additional settings
    engine_task.set_editor_property('options', options)

    return engine_task


def _execute_import_tasks(import_tasks: list[unreal.AssetImportTask]) -> list[str]:
    """
    Imports a single asset from disk in Unreal.

    Args:
        import_tasks (list[unreal.AssetImportTask]): The import task settings
         for the asset to be imported. Function will convert
         list[unreal.AssetImportTask] to unreal.Array(unreal.AssetImportTask).
    Returns:
        list[str]: The asset path names of the imported assets.
    """
    tasks = unreal.Array(unreal.AssetImportTask)

    for i in import_tasks:
        # Convert list of import tasks to unreal.Array of import tasks
        # and mark the pre-existing assets as re-imported for log.
        tasks.append(i)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    asset_path_names = []
    for i in import_tasks:
        for path in i.get_editor_property('imported_object_paths'):
            asset_path_names.append(path)

    return asset_path_names


# ----------Import Options-------------------------------------------------------------------------

def _import_sm_options(message: asset_messages.ImportSMAsset) -> unreal.FbxImportUI:
    """
    Creates the import options for static meshes.

    Args:
        message (ImportSMAsset): The ImportSMAsset command containing all
         relevant values.
    Returns:
        unreal.FbxImportUI: The import options for the static mesh.
    """
    # Import Options
    options = unreal.FbxImportUI()

    # FBX generic import data
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', True)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', False)
    options.set_editor_property('import_animations', False)
    options.set_editor_property('create_physics_asset', False)

    # FBX mesh import data
    _set = functools.partial(_set_sm_property, options)
    _set('import_translation', message.body.loc)
    _set('import_rotation', message.body.rot)
    _set('import_uniform_scale', message.body.scale)
    _set('combine_meshes', message.body.merge)
    _set('remove_degenerates', message.body.remove_degenerates)
    _set('generate_lightmap_u_vs', message.body.generate_lightmaps)
    _set('auto_generate_collision', message.body.auto_gen_collisions)
    _set('convert_scene', True)
    _set('force_front_x_axis', False)
    _set('convert_scene_unit', False)
    _set('normal_generation_method', message.body.normal_gen_method)
    _set('normal_import_method', message.body.normal_import_method)
    _set('one_convex_hull_per_ucx', message.body.one_convex_hull)
    _set('transform_vertex_to_absolute', True)
    _set('build_reversed_index_buffer', True)

    unreal.log('IMPORTING STATIC MESH'.center(80, '-'))

    return options


def _import_sk_options(message: asset_messages.ImportSKAsset) -> unreal.FbxImportUI:
    """
    Creates the import options for skeletal meshes.

    Args:
        message (ImportSMAsset): The ImportSMAsset command containing all
         relevant values.
    Returns:
        unreal.FbxImportUI: The import options for the skeletal mesh.
    """
    # Import Options
    options = unreal.FbxImportUI()

    # Fbx generic import data
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', True)
    options.set_editor_property('import_materials', True)
    options.set_editor_property('import_as_skeletal', True)
    options.set_editor_property('import_animations', False)
    options.set_editor_property('create_physics_asset', message.body.create_physics_asset)

    # Fbx skeletal import data
    _set = functools.partial(_set_skel_property, options)
    _set(options, 'import_translation', message.body.loc)
    _set(options, 'import_rotation', message.body.rot)
    _set(options, 'import_uniform_scale', message.body.scale)
    _set(options, 'import_morph_targets', message.body.import_morph_targets)
    _set(options, 'use_t0_as_ref_pose', True)
    _set(options, 'preserve_smoothing_groups', message.body.preserve_smoothing_groups)
    _set(options, 'import_meshes_in_bone_hierarchy', True)
    _set(options, 'threshold_position', 0.00002)
    _set(options, 'threshold_tangent_normal', 0.00002)
    _set(options, 'threshold_uv', 0.000977)
    _set(options, 'convert_scene', message.body.convert_scene)
    _set(options, 'force_front_x_axis', False)
    _set(options, 'convert_scene_unit', False)
    _set(options, 'transform_vertex_to_absolute', True)
    _set(options, 'normal_generation_method', message.body.normal_gen_method)
    _set(options, 'normal_import_method', message.body.normal_imp_method)

    # Skeleton for imported mesh, if none specified, import skeleton in fbx
    if message.body.skeleton:
        options.skeleton = message.body.skeleton

    unreal.log('IMPORTING SKEL MESH'.center(80, '-'))

    return options


def _import_anim_options(message: asset_messages.ImportAnim) -> unreal.FbxImportUI:
    """
    Import options for skel mesh animations. Will import skeleton in fbx if none provided.

    Args:
        message (ImportAnim): The ImportSKAsset command containing all
         relevant values.

    Returns:
        unreal.FbxImportUI: The import options for the skeletal mesh animation.
    """
    # Import Options
    options = unreal.FbxImportUI()
    options.set_editor_property('import_animations', True)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('create_physics_asset', False)

    if message.body.skeleton:
        options.set_editor_property('import_mesh', False)
        options.skeleton = message.body.skeleton
    else:
        options.set_editor_property('import_mesh', True)
        _set_skel_property(options, 'import_morph_targets', True)

    _set_anim_property(options, 'use_default_sample_rate', message.body.fps == 30)

    _set = functools.partial(_set_skel_property, options)
    # Fbx skel mesh import data
    _set(options, 'import_translation', message.body.loc)
    _set(options, 'import_rotation', message.body.rot)
    _set(options, 'import_uniform_scale', message.body.scale)
    _set(options, 'convert_scene', message.body.convert_scene)
    _set(options, 'force_front_x_axis', False)
    _set(options, 'convert_scene_unit', False)
    _set(options, 'import_meshes_in_bone_hierarchy', True)

    # Fbx anim sequence import data
    _set(options, 'delete_existing_morph_target_curves', message.body.del_morph_targets)
    _set(options, 'import_custom_attribute', True)
    _set(options, 'import_bone_tracks', True)
    _set(options, 'custom_sample_rate', message.body.fps)
    _set(options, 'do_not_import_curve_with_zero', True)
    _set(options, 'remove_redundant_keys', True)
    _set(options, 'animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)

    unreal.log('IMPORTING SKELETAL MESH ANIMATION'.center(80, '-'))

    return options

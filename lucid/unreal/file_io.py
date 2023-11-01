"""
# Unreal Import

* Description:

    Import functions for assets into unreal.

* Notes:

    Most import option values are currently hard-coded but could easily be hooked up to UI.

    This file would have been called io.py but that name seems to be reserved in Unreal,
    causing it to crash if found on the path on startup.

* UE Path types:

    Display Name & Asset Name = AssetName
    Path Name & Object Path   = /Game/dir/dir/AssetName.AssetName
    Package Path              = /Game/dir/dir
    Package Name              = /Game/dir/dir/AssetName

* Update History:

    `2023-09-24` - Init

    `2023-10-06` - Changed default fps in anim import.

    `2023-10-30` - Changed path handling from str to Path objects.
"""


from typing import Union
from pathlib import Path

import unreal


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Shorthands
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# The unreal module has very large names for functions.
# Some of which have been shorthanded, or aliased, here.


"""Functions"""


def _set_skel_property(import_options: unreal.FbxImportUI, string_name: str, value=None):
    """Simple to type func to set skel mesh import option."""
    import_options.skeletal_mesh_import_data.set_editor_property(string_name, value)


def _set_staticmesh_property(import_options: unreal.FbxImportUI, string_name: str, value=None):
    """Simple to type func to set static mesh import option."""
    import_options.static_mesh_import_data.set_editor_property(string_name, value)


def _set_anim_property(import_options: unreal.FbxImportUI, string_name: str, value=None):
    """Simple to type func to set skel anim import options."""
    import_options.anim_sequence_import_data.set_editor_property(string_name, value)


"""Variable Types"""


NORMAL_GEN_METHOD = unreal.FBXNormalGenerationMethod
NORMAL_IMP_METHOD = unreal.FBXNormalImportMethod


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Primary import functions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def import_static_mesh(source_path: Path, destination_package_path: str, import_name: str = '',
                       loc: unreal.Vector = (0.0, 0.0, 0.0), rot: unreal.Rotator = (0.0, 0.0, 0.0),
                       scale: float = 1.0, merge: bool = True, remove_degenerate_tris: bool = False,
                       generate_lightmaps: bool = True, auto_gen_collisions: bool = True,
                       normal_gen_method=NORMAL_GEN_METHOD.MIKK_T_SPACE,
                       normal_import_method: NORMAL_IMP_METHOD = NORMAL_IMP_METHOD.FBXNIM_IMPORT_NORMALS_AND_TANGENTS,
                       one_convex_hull: bool = False, reimport: bool = True) -> str:
    """
    Imports a static mesh asset into Unreal Engine.

    Args:
        source_path (Path): The file path of the static mesh to be imported.

        destination_package_path (str): The package path of the asset in the content browser.

        import_name (str, optional): The name of the imported asset. Defaults to an empty string.

        loc (unreal.Vector, optional): The locational offset fo the mesh. Defaults to (0,0,0).

        rot (unreal.Rotator, optional): The rotational offset fo the mesh. Defaults to (0,0,0).

        scale (float, optional): The scale of the imported asset. Defaults to 1.0.

        merge (bool, optional): Whether to merge all meshes within the imported FBX.
        Defaults to True.

        remove_degenerate_tris (bool): Whether unreal should remove what it deems to be a degenerate triangle.
        These are typically tris that are too densely packed together, but can also be non-planar tris.
        Defaults to False.

        generate_lightmaps (bool): Whether unreal should generate lightmap UVs at uv index 0 on asset import.
        Defaults to True.

        auto_gen_collisions (bool): Whether unreal should generate a collision mesh for the static mesh on
        import. Defaults to True.

        normal_gen_method (unreal.FBXNormalGenerationMethod): Which method unreal should generate normals with.
        Defaults to MIKK_T_SPACE.

        normal_import_method (unreal.FBXNormalImportMethod): Which method unreal should import existing normal
        data from the fbx with. Defaults to FBXNIM_IMPORT_NORMALS_AND_TANGENTS.

        one_convex_hull (bool): Whether one convexed collision mesh should be created for the entire asset,
        or a collision mesh should be made for each imported part. Defaults to False.

        reimport (bool, optional): Whether to reimport the asset if it already exists. Defaults to True.

    Returns:
        str: The path name of the imported asset.
    """
    options = _import_sm_options(loc, rot, scale, merge, remove_degenerate_tris, generate_lightmaps,
                                 auto_gen_collisions,
                                 normal_gen_method, normal_import_method, one_convex_hull)
    static_mesh = _import_task(options, source_path, destination_package_path, import_name,
                               reimport)
    asset_task = _execute_import_tasks([static_mesh])

    return asset_task[0]

def import_skeletal_mesh(source_path: Path, destination_package_path: str,
                         skeleton: Union[unreal.Skeleton, None],
                         import_name: str = '',
                         loc: unreal.Vector = (0.0, 0.0, 0.0), rot: unreal.Rotator = (0.0, 0.0, 0.0),
                         scale: float = 1.0, create_physics_asset: bool = False,
                         import_morph_targets: bool = True,
                         preserve_smoothing_groups: bool = True, convert_scene: bool = True,
                         normal_gen_method: NORMAL_GEN_METHOD = NORMAL_GEN_METHOD.MIKK_T_SPACE,
                         normal_import_method: NORMAL_IMP_METHOD = NORMAL_IMP_METHOD.FBXNIM_IMPORT_NORMALS_AND_TANGENTS,
                         reimport: bool = True) -> str:
    """
    Imports a skeletal mesh asset into Unreal Engine.

    Args:
        source_path (Path): The file path of the static mesh to be imported.

        destination_package_path (str): The package path of the asset in the content browser.

        skeleton (unreal.Skeleton): The skeleton for the mesh to use, skeleton in fbx will be used if one
        is not provided.

        import_name (str, optional): The name of the imported asset. Defaults to an empty string.

        loc (unreal.Vector, optional): The locational offset fo the mesh. Defaults to (0,0,0).

        rot (unreal.Rotator, optional): The rotational offset fo the mesh. Defaults to (0,0,0).

        scale (float, optional): The scale of the imported asset. Defaults to 1.0.

        create_physics_asset (bool): Whether to make a physics asset for the imported mesh. Defaults
        to False.

        import_morph_targets (bool): Whether to import any morph targets within the imported FBX file.
        Defaults to True.

        preserve_smoothing_groups (bool): Whether to preserve any smoothing groups within the imported
        FBX file. Setting to False will import with hard edges. Defaults to True.

        convert_scene (bool): Whether to import the scene from a Y up-axis scene. Defaults to True.

        normal_gen_method (unreal.FBXNormalGenerationMethod): Which method unreal should generate
        any missing normal data from the FBX file with. Defaults to MIKK_T_SPACE.

        normal_import_method (unreal.FBXNormalImportMethod): Which method unreal should import any
        existing normal data from the FBX file with. Defaults to FBXNIM_IMPORT_NORMALS_AND_TANGENTS.

        reimport (bool, optional): Whether to reimport the asset if it already exists. Defaults to True.

    Returns:
        str: The path name of the imported asset.
    """
    options = _import_sk_options(skeleton, loc, rot, scale, create_physics_asset, import_morph_targets,
                                 preserve_smoothing_groups, convert_scene,
                                 normal_gen_method, normal_import_method)
    skeletal_mesh = _import_task(options, source_path, destination_package_path, import_name, reimport)
    asset_task = _execute_import_tasks([skeletal_mesh])

    return asset_task[0]


def import_animation(source_path: Path, destination_package_path: str, skeleton: unreal.Skeleton,
                     fps: int = 30, loc: unreal.Vector = (0.0, 0.0, 0.0),
                     rot: unreal.Rotator = (0.0, 0.0, 0.0), scale: float = 1.0,
                     convert_scene: bool = True, del_morph_targets: bool = False,
                     import_name: str = '', reimport: bool = True) -> str:
    """
    Imports a skeletal mesh animation into Unreal Engine.

    Args:
        source_path (Path): The file path of the animation to be imported.

        destination_package_path (str): The package path of the asset in the content browser.

        skeleton (unreal.Skeleton): The skeleton object reference to assign the animation to.

        fps (int): The frame rate for the imported animation to play back at. If the fps is set to 30,
        'use_default_sample_rate' will be switched to True. Defaults to 24.

        loc (unreal.Vector): The locational offset of the animation. Defaults to (0.0, 0.0, 0.0).

        rot (unreal.Rotator): The rotational offset of the animation. Defaults to (0.0, 0.0, 0.0).

        scale (float): The import scale of the animation. Defaults to 1.0.

        convert_scene (bool): Whether to import the scene from a Y up-axis scene. Defaults to True.

        del_morph_targets(bool): Whether to delete any existing morph target curves on anim import.
        Defaults to False.

        import_name (str, optional): The name of the imported asset. Defaults to an empty string.

        reimport (bool, optional): Whether to reimport the asset if it already exists. Defaults to True.

    Returns:
        str: The path name of the imported asset.
    """
    options = _import_anim_options(skeleton, fps, loc, rot, scale, convert_scene, del_morph_targets)
    anim = _import_task(options, source_path, destination_package_path, import_name, reimport)
    anim_task = _execute_import_tasks([anim])

    return anim_task[0]


def import_texture(source_path: Path, destination_package_path: str, reimport: bool = True,
                   import_name: str = '', compression_override: int = 0) -> str:
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
        source_path (Path): The path of the source texture file to import.

        destination_package_path (str): The package path where the imported texture asset should be saved.

        reimport (bool, optional): Whether to reimport the texture if it already exists in the destination
        package. Defaults to True.

        import_name (str, optional): The name to use for the imported texture asset. If empty, the
        name will be derived from the source file name. Defaults to ''.

        compression_override (int, optional): Override value for the texture compression settings.
        If non-zero, this value will be used instead of the default compression settings inferred
        from the source file name suffix. Defaults to 0.

    Returns:
        str: The path name of the imported asset.
    """
    file_name = source_path.split('/')[-1].split('.')[0]
    texture = _import_task(None, source_path, destination_package_path, import_name, reimport)

    unreal_path = _execute_import_tasks([texture])[0]
    asset = unreal.load_asset(str(unreal_path))

    # Texture type settings
    if compression_override:
        asset.set_editor_property('compression_settings', unreal.TextureCompressionSettings.cast(compression_override))
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


def import_texture_batch(texture_list: list[str], source_dir: str, destination_dir: str, reimport: bool = True):
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
        texture_list (list[str]): A list of texture file names (without extension) to import.

        source_dir (str): The folder path where the source texture files are located.

        destination_dir (str): The directory path where the imported texture assets should be saved.

        reimport (bool): Whether to reimport a texture asset if it already exists
        in the destination directory. Defaults to True.
    """
    for i in texture_list:
        if i.endswith('.tga'):
            source_path_name = f'{source_dir}/{i}'
        else:
            source_path_name = f'{source_dir}/{i}.tga'

        import_texture(source_path_name, destination_dir, reimport)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Import task declaration and execution
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def _import_task(options: Union[unreal.FbxImportUI, None], source_path: Path, destination_package_path: str,
                 import_name: str = '', reimport: bool = True, ) -> unreal.AssetImportTask:
    """
    Sets the import task settings when importing an asset.

    Args:
        options (unreal.FbxImportUI): The import options for the asset.

        source_path (Path): The file path of the asset to import.

        destination_package_path (str): The destination path of the imported asset within the Unreal Engine content browser.

        import_name (str): The name to use for the imported asset. Defaults to ''.

        reimport (bool): Whether to reimport an existing asset with the same name. Defaults to True.

    Returns:
        unreal.AssetImportTask: The asset import task with the specified settings.
    """
    task = unreal.AssetImportTask()

    # Task settings
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', import_name)
    task.set_editor_property('destination_path', destination_package_path)
    task.set_editor_property('filename', source_path.as_posix())
    task.set_editor_property('replace_existing', reimport)
    task.set_editor_property('save', True)

    # Additional settings
    task.set_editor_property('options', options)

    return task


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
        for path in i.get_editor_property('imported_object_paths'):
            asset_paths.append(path)
            if not path.split('.')[0] in is_reload:
                unreal.log_warning(f'\nImported: {path}\n')
            else:
                unreal.log_warning(f'\nReImported: {path}s\n')

    return asset_paths


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Import options by import type
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def _import_sm_options(loc: unreal.Vector = (0.0, 0.0, 0.0), rot: unreal.Rotator = (0.0, 0.0, 0.0),
                       scale: float = 1.0, merge: bool = True, remove_degenerates: bool = False,
                       generate_lightmaps: bool = True, auto_gen_collisions: bool = True,
                       normal_gen_method: NORMAL_GEN_METHOD = NORMAL_GEN_METHOD.MIKK_T_SPACE,
                       normal_import_method: NORMAL_IMP_METHOD = NORMAL_IMP_METHOD.FBXNIM_IMPORT_NORMALS_AND_TANGENTS,
                       one_convex_hull: bool = False) -> unreal.FbxImportUI:
    """
    Creates the import options for static meshes.

    Args:
        loc (unreal.Vector): The locational offset of the static mesh. Defaults to (0.0, 0.0, 0.0).

        rot (unreal.Rotator): The rotational offset of the static mesh. Defaults to (0.0, 0.0, 0.0).

        scale (float): The import scale of the static mesh. Defaults to 1.0.

        merge (bool): Whether to combine meshes during import. Defaults to True.

        remove_degenerates (bool): Whether unreal should remove what it deems to be a degenerate triangle.
        These are typically tris that are too densely packed together, but can also be non-planar tris.
        Defaults to False.

        generate_lightmaps (bool): Whether unreal should generate lightmap UVs at uv index 0 on asset import.
        Defaults to True.

        auto_gen_collisions (bool): Whether unreal should generate a collision mesh for the static mesh on
        import. Defaults to True.

        normal_gen_method (unreal.FBXNormalGenerationMethod): Which method unreal should generate normals with.
        Defaults to MIKK_T_SPACE.

        normal_import_method (unreal.FBXNormalImportMethod): Which method unreal should import existing normal
        data from the fbx with. Defaults to FBXNIM_IMPORT_NORMALS_AND_TANGENTS.

        one_convex_hull (bool): Whether one convexed collision mesh should be created for the entire asset,
        or a collision mesh should be made for each imported part. Defaults to False.

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
    _set_staticmesh_property(options, 'import_translation', loc)
    _set_staticmesh_property(options, 'import_rotation', rot)
    _set_staticmesh_property(options, 'import_uniform_scale', scale)
    _set_staticmesh_property(options, 'combine_meshes', merge)
    _set_staticmesh_property(options, 'remove_degenerates', remove_degenerates)
    _set_staticmesh_property(options, 'generate_lightmap_u_vs', generate_lightmaps)
    _set_staticmesh_property(options, 'auto_generate_collision', auto_gen_collisions)
    _set_staticmesh_property(options, 'convert_scene', True)
    _set_staticmesh_property(options, 'force_front_x_axis', False)
    _set_staticmesh_property(options, 'convert_scene_unit', False)
    _set_staticmesh_property(options, 'normal_generation_method', normal_gen_method)
    _set_staticmesh_property(options, 'normal_import_method', normal_import_method)
    _set_staticmesh_property(options, 'one_convex_hull_per_ucx', one_convex_hull)
    _set_staticmesh_property(options, 'transform_vertex_to_absolute', True)
    _set_staticmesh_property(options, 'build_reversed_index_buffer', True)

    unreal.log('IMPORTING STATIC MESH')

    return options

def _import_sk_options(skeleton: Union[unreal.Skeleton, None], loc: unreal.Vector = (0.0, 0.0, 0.0),
                       rot: unreal.Rotator = (0.0, 0.0, 0.0),
                       scale: float = 1.0, create_physics_asset: bool = False, import_morph_targets: bool = True,
                       preserve_smoothing_groups: bool = True, convert_scene: bool = True,
                       normal_gen_method: NORMAL_GEN_METHOD = NORMAL_GEN_METHOD.MIKK_T_SPACE,
                       normal_imp_method: NORMAL_IMP_METHOD = NORMAL_IMP_METHOD.FBXNIM_IMPORT_NORMALS_AND_TANGENTS) -> unreal.FbxImportUI:
    """
    Creates the import options for skeletal meshes.

    Args:
        loc (unreal.Vector): The locational offset of the static mesh. Defaults to (0.0, 0.0, 0.0).

        rot (unreal.Rotator): The rotational offset of the static mesh. Defaults to (0.0, 0.0, 0.0).

        scale (float): The import scale of the static mesh. Defaults to 1.0.

        create_physics_asset (bool): Whether to make a physics asset for the imported mesh. Defaults
        to False.

        import_morph_targets (bool): Whether to import any morph targets within the imported FBX file.
        Defaults to True.

        preserve_smoothing_groups (bool): Whether to preserve any smoothing groups within the imported
        FBX file. Setting to False will import with hard edges. Defaults to True.

        convert_scene (bool): Whether to import the scene from a Y up-axis scene. Defaults to True.

        normal_gen_method (unreal.FBXNormalGenerationMethod): Which method unreal should generate
        any missing normal data from the FBX file with. Defaults to MIKK_T_SPACE.

        normal_imp_method (unreal.FBXNormalImportMethod): Which method unreal should import any
        existing normal data from the FBX file with. Defaults to FBXNIM_IMPORT_NORMALS_AND_TANGENTS.

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
    options.set_editor_property('create_physics_asset', create_physics_asset)

    # Fbx skeletal import data
    _set_skel_property(options, 'import_translation', loc)
    _set_skel_property(options, 'import_rotation', rot)
    _set_skel_property(options, 'import_uniform_scale', scale)
    _set_skel_property(options, 'import_morph_targets', import_morph_targets)
    _set_skel_property(options, 'use_t0_as_ref_pose', True)
    _set_skel_property(options, 'preserve_smoothing_groups', preserve_smoothing_groups)
    _set_skel_property(options, 'import_meshes_in_bone_hierarchy', True)
    _set_skel_property(options, 'threshold_position', 0.00002)
    _set_skel_property(options, 'threshold_tangent_normal', 0.00002)
    _set_skel_property(options, 'threshold_uv', 0.000977)
    _set_skel_property(options, 'convert_scene', convert_scene)
    _set_skel_property(options, 'force_front_x_axis', False)
    _set_skel_property(options, 'convert_scene_unit', False)
    _set_skel_property(options, 'transform_vertex_to_absolute', True)
    _set_skel_property(options, 'normal_generation_method', normal_gen_method)
    _set_skel_property(options, 'normal_import_method', normal_imp_method)

    # Skeleton for imported mesh, if none specified, import skeleton in fbx
    if skeleton:
        options.skeleton = skeleton

    unreal.log('IMPORTING SKEL MESH')

    return options


def _import_anim_options(skeleton: unreal.Skeleton = None, fps: int = 24, loc: unreal.Vector = (0.0, 0.0, 0.0),
                         rot: unreal.Rotator = (0.0, 0.0, 0.0), scale: float = 1.0, convert_scene: bool = True,
                         del_morph_targets: bool = False) -> unreal.FbxImportUI:
    """
    Import options for skel mesh animations. Will import skeleton in fbx if none provided.

    Args:
        skeleton (unreal.Skeleton): A skeleton to use for the import. If none provided, the mesh will be imported as well.
        Defaults to None.

        fps (int): The frame rate for the imported animation to play back at. If the fps is set to 30,
        'use_default_sample_rate' will be switched to True. Defaults to 24.

        loc (unreal.Vector): The locational offset of the static mesh. Defaults to (0.0, 0.0, 0.0).

        rot (unreal.Rotator): The rotational offset of the static mesh. Defaults to (0.0, 0.0, 0.0).

        scale (float): The import scale of the static mesh. Defaults to 1.0.

        convert_scene (bool): Whether to import the scene from a Y up-axis scene. Defaults to True.

        del_morph_targets(bool): Whether to delete any existing morph target curves on anim import.
        Defaults to False.

    Returns:
        unreal.FbxImportUI: The import options for the skeletal mesh animation.
    """
    # Import Options
    options = unreal.FbxImportUI()
    options.set_editor_property('import_animations', True)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('create_physics_asset', False)

    if skeleton:
        options.set_editor_property('import_mesh', False)
        options.skeleton = skeleton
    else:
        options.set_editor_property('import_mesh', True)
        _set_skel_property(options, 'import_morph_targets', True)

    if fps != 30:
        _set_anim_property(options, 'use_default_sample_rate', False)
    else:
        _set_anim_property(options, 'use_default_sample_rate', True)

    # Fbx anim sequence import data
    _set_anim_property(options, 'import_translation', loc)
    _set_anim_property(options, 'import_rotation', rot)
    _set_anim_property(options, 'import_uniform_scale', scale)
    _set_anim_property(options, 'convert_scene', convert_scene)
    _set_anim_property(options, 'force_front_x_axis', False)
    _set_anim_property(options, 'convert_scene_unit', False)
    _set_anim_property(options, 'remove_redundant_keys', True)
    _set_anim_property(options, 'animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    _set_anim_property(options, 'import_meshes_in_bone_hierarchy', True)
    _set_anim_property(options, 'import_bone_tracks', True)
    _set_anim_property(options, 'custom_sample_rate', fps)
    _set_anim_property(options, 'import_custom_attribute', True)
    _set_anim_property(options, 'do_not_import_curve_with_zero', True)
    _set_anim_property(options, 'delete_existing_morph_target_curves', del_morph_targets)

    unreal.log('IMPORTING SKELETAL MESH ANIMATION')

    return options

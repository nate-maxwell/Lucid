"""
# Unreal API Shorthands

* Description:

    The unreal module has very large names for functions.
    Some of which have been shorthanded, or aliased, here.
"""


import unreal


# --------Functions------------------------------------------------------------

def set_skel_property(import_options: unreal.FbxImportUI, string_name: str, value=None) -> None:
    """Simple to type func to set skel mesh import option."""
    import_options.skeletal_mesh_import_data.set_editor_property(string_name, value)


def set_staticmesh_property(import_options: unreal.FbxImportUI, string_name: str, value=None) -> None:
    """Simple to type func to set static mesh import option."""
    import_options.static_mesh_import_data.set_editor_property(string_name, value)


def set_anim_property(import_options: unreal.FbxImportUI, string_name: str, value=None) -> None:
    """Simple to type func to set skel anim import options."""
    import_options.anim_sequence_import_data.set_editor_property(string_name, value)


# --------Variable Types-------------------------------------------------------

fbx_normal_gen_method = unreal.FBXNormalGenerationMethod
"""unreal.FBXNormalGenerationMethod"""

fbx_normal_mikk_t_space = fbx_normal_gen_method.MIKK_T_SPACE
"""unreal.FBXNormalGenerationMethod.MIKK_T_SPACE"""


fbx_normal_imp_method = unreal.FBXNormalImportMethod
"""unreal.FBXNormalImportMethod"""

fbx_import_normals_tangents = fbx_normal_imp_method.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
"""unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS"""

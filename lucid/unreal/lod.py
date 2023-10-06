"""
# Unreal LODs

* Update History:

    `2023-05-16` - Init
"""


import unreal


def import_sk_lod(mesh_package_name: str, lod_index: int, source_path_name: str):
    """
        Function to import a specified level of detail (LOD) for a given skeletal mesh asset.

        Args:
            mesh_package_name (str): The project path of the mesh to import the LOD onto.

            lod_index (int): The index of the LOD to import to.

            source_path_name (str): The filepath, including file extension, to import the LOD from.
    """
    mesh = unreal.load_asset(mesh_package_name)
    print(mesh)
    unreal.SkeletalMeshEditorSubsystem.import_lod(mesh, lod_index, source_path_name)


def import_sm_lod(mesh_package_name: str, lod_index: int, source_path_name: str):
    """
    Function to import a specified level of detail (LOD) for a given static mesh asset.

    Args:
        mesh_package_name (str): The project path of the mesh to import the LOD onto.

        lod_index (int): The index of the LOD to import to.

        source_path_name (str): The filepath, including file extension, to import the LOD from.
    """
    mesh = unreal.load_asset(mesh_package_name)
    unreal.StaticMeshEditorSubsystem.import_lod(mesh, lod_index, source_path_name)

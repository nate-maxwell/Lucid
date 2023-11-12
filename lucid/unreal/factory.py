"""
# Unreal Factory

* Description

    Simplified or directed factories for Lucid in Unreal.

* Update History

    `2023-09-27` - Init
"""


import unreal

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()


def create_sequence(asset_name: str, package_path: str = '/Game/_generated/') -> unreal.LevelSequence:
    """
    Creates a level sequence in the content browser at the specified package path.

    Args:
        asset_name (str): The name to give the created asset.

        package_path(str): Where to place the asset within the content folder of the project.
            Package paths use /Game/ to denote the content folder within the directory, e.g.
            /Game/DD/Seq/DEF/0010/.

    Returns:
        unreal.LevelSequence: The object reference to the created level sequence asset.
    """
    factory = unreal.LevelSequenceFactoryNew()
    sequence_asset = unreal.LevelSequence(
        asset_tools.create_asset(asset_name, package_path, unreal.LevelSequence, factory))

    return sequence_asset


def create_material_instance(asset_name: str, package_path: str, parent_package_path: str) -> unreal.MaterialInstanceConstant:
    """
    Creates a material instance in the content browser at teh specified package path, inheriting
    from the specified parent.

    Args:
        asset_name(str): The name to give the created material instance.

        package_path(str): Where to place the material instance within the content folder
        of the project.

        parent_package_path(str): The unreal package path to the parent that the material
        instance should inherit from.

    Returns:
        unreal.MaterialInstanceConstant: The object reference to the created material instance.
    """
    if not package_path.endswith('/'):
        package_path += '/'

    factory = unreal.MaterialInstanceConstantFactoryNew()
    mat_inst_asset = asset_tools.create_asset(asset_name, package_path, unreal.MaterialInstanceConstant, factory)

    parent_mat = unreal.load_asset(parent_package_path)
    unreal.MaterialEditingLibrary.set_material_instance_parent(mat_inst_asset, parent_mat)

    return unreal.load_asset(f'{package_path}{asset_name}')

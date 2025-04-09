"""
# Lucid Asset Message Objects

* Description:

    The message objects used for asset IO domain.
"""


from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import unreal
from lucid import const
from lucid.system.messaging import message
from lucid.unreal import ImportTask


NORMAL_GEN_METHOD = unreal.FBXNormalGenerationMethod
MIKK_T_SPACE = NORMAL_GEN_METHOD.MIKK_T_SPACE
NORMAL_IMP_METHOD = unreal.FBXNormalImportMethod
FBXNIM_IMPORT_NORMALS_AND_TANGENTS = NORMAL_IMP_METHOD.FBXNIM_IMPORT_NORMALS_AND_TANGENTS


@dataclass
class ImportSMAssetBody(message.MessageBody):
    import_task: ImportTask

    loc: unreal.Vector = (0.0, 0.0, 0.0)
    rot: unreal.Rotator = (0.0, 0.0, 0.0)
    scale: float = 1.0

    normal_gen_method: NORMAL_GEN_METHOD = MIKK_T_SPACE
    normal_imp_method: NORMAL_IMP_METHOD = FBXNIM_IMPORT_NORMALS_AND_TANGENTS

    merge: bool = True
    remove_degenerates: bool = False
    generate_lightmaps: bool = True
    auto_gen_collisions: bool = True
    one_convex_hull: bool = False


class ImportSMAsset(message.Command):
    def __init__(
            self,
            source_path: Path,
            destination_package_path: Path,
            import_name: str = '',
            reimport: bool = True
    ) -> None:
        super().__init__(const.ASSET_CHAN)
        import_task = ImportTask(
            source_path,
            destination_package_path,
            import_name,
            reimport
        )
        self.body = ImportSMAssetBody(import_task)


@dataclass
class ImportSKAssetBody(message.MessageBody):
    import_task: ImportTask
    skeleton: Optional[unreal.Skeleton] = None

    loc: unreal.Vector = (0.0, 0.0, 0.0)
    rot: unreal.Rotator = (0.0, 0.0, 0.0)
    scale: float = 1.0
    convert_scene: bool = True

    normal_gen_method: NORMAL_GEN_METHOD = MIKK_T_SPACE
    normal_imp_method: NORMAL_IMP_METHOD = FBXNIM_IMPORT_NORMALS_AND_TANGENTS

    create_physics_asset: bool = False
    import_morph_targets: bool = True
    preserve_smoothing_groups: bool = True


class ImportSKAsset(message.Command):
    def __init__(
            self,
            source_path: Path,
            destination_package_path: Path,
            import_name: str = '',
            reimport: bool = True,
            skeleton: Optional[unreal.Skeleton] = None,
    ) -> None:
        super().__init__(const.ASSET_CHAN)
        import_task = ImportTask(
            source_path,
            destination_package_path,
            import_name,
            reimport
        )
        self.body = ImportSKAssetBody(import_task, skeleton)


@dataclass
class ImportAnimBody(message.MessageBody):
    import_task: ImportTask
    skeleton: Optional[unreal.Skeleton] = None

    loc: unreal.Vector = (0.0, 0.0, 0.0)
    rot: unreal.Rotator = (0.0, 0.0, 0.0)
    scale: float = 1.0
    convert_scene: bool = True
    del_morph_targets: bool = False


class ImportAnim(message.Command):
    def __init__(
            self,
            source_path: Path,
            destination_package_path: Path,
            import_name: str = '',
            reimport: bool = True,
            skeleton: Optional[unreal.Skeleton] = None,
    ) -> None:
        super().__init__(const.ASSET_CHAN)
        import_task = ImportTask(
            source_path,
            destination_package_path,
            import_name,
            reimport
        )
        self.body = ImportAnimBody(import_task, skeleton)


@dataclass
class ImportTextureBody(message.MessageBody):
    import_task: ImportTask
    compression_override: int = 0


class ImportTexture(message.Command):
    def __init__(
            self,
            source_path: Path,
            destination_package_path: Path,
            import_name: str = '',
            reimport: bool = True,
            compression_override: int = 0
    ) -> None:
        super().__init__(const.ASSET_CHAN)
        import_task = ImportTask(
            source_path,
            destination_package_path,
            import_name,
            reimport
        )
        self.body = ImportTextureBody(import_task, compression_override)


@dataclass
class BatchImportTextureBody(message.MessageBody):
    textures: list[ImportTextureBody]


class BatchImportTextures(message.Command):
    def __init__(
            self,
            source_paths: list[Path],
            destination_package_path: Path,
            import_name: str = '',
            reimport: bool = True,
            compression_override: int = 0
    ) -> None:
        super().__init__(const.ASSET_CHAN)
        texture_bodies = []
        for p in source_paths:
            task = ImportTask(
                p,
                destination_package_path,
                import_name,
                reimport
            )
            texture_body = ImportTextureBody(task, compression_override)
            texture_bodies.append(texture_body)

        self.body = BatchImportTextureBody(texture_bodies)

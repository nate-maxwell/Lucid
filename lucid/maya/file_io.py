"""
Lucid Maya IO Library

* Description

    A library for handling io operations in maya for the Lucid core.
"""


from pathlib import Path

# noinspection PyUnresolvedReferences
import maya.cmds
import pymel.core as pm

from lucid import const
from lucid.maya import asset_messages
from lucid.messaging import router


def open_file_dialog(message: asset_messages.OpenFileDialog) -> None:
    """
    Show Maya (.ma, .mb) file open dialog, and return path, or None if cancelled.
    Sends a document response message back over the asset channel.

    Args:
        message(OpenFileDialog): The message containing the starting path for
        the file dialog if folder is not within maya project files.
    """
    path = maya.cmds.fileDialog2(
        startingDirectory=message.body.filepath,
        fileFilter='Maya Files (*.ma *.mb)',
        fileMode=1,  # A single existing file
        dialogStyle=2,  # Maya style dialog (1 is OS style)
        setProjectBtnEnabled=False
    )

    if path is not None:
        path = Path(path[0])  # If not cancelled, fileDialog returns list[str]

    response = asset_messages.OpenFileDialog(path)
    router.route_message(response)


def open_file(message: asset_messages.OpenFile) -> None:
    """Force open a Maya (.ma, .mb) file.
    Does *not* prompt user if unsaved changes in scene.
    """
    maya.cmds.file(
        message.body.filepath.as_posix(),
        open=True,

        # Force an action to take place. Open file even if there are unsaved
        # changes in current scene.
        force=True,

        # "Used to open files with versions other than those officially supported.
        # Success is not guaranteed. Data loss, data corruption or failure to
        # open are all possible outcomes."
        ignoreVersion=True
    )


def export_fbx(message: asset_messages.ExportFBX) -> None:
    """
    Exports a fbx file with the given parameters defined in the export_options object.

    args:
        message(ExportFBX): The message containing the fbx export options. Attributes
        are called as pymel.mel.FBXExport...() args.
    """
    pm.mel.FBXResetExport()

    pm.mel.FBXExportConstraints(v=message.body.FBXExportConstraints)
    pm.mel.FBXExportCameras(v=message.body.FBXExportCameras)
    pm.mel.FBXExportInputConnections(v=message.body.FBXExportInputConnections)
    pm.mel.FBXExportUpAxis(message.body.FBXExportUpAxis)
    pm.mel.FBXExportTriangulate(v=message.body.FBXExportTriangulate)
    pm.mel.FBXExportIncludeChildren(v=message.body.FBXExportIncludeChildren)
    pm.mel.FBXExportScaleFactor(message.body.FBXExportScaleFactor)
    pm.mel.FBXExportShapes(v=message.body.FBXExportShapes)
    pm.mel.FBXExportSkins(v=message.body.FBXExportSkins)
    pm.mel.FBXExportInstances(v=message.body.FBXExportInstances)
    pm.mel.FBXExportLights(v=message.body.FBXExportLights)

    pm.mel.FBXExportEmbeddedTextures(v=message.body.FBXExportEmbeddedTextures)
    pm.mel.FBXExportFileVersion(v=message.body.FBXExportFileVersion)
    pm.mel.FBXExportGenerateLog(v=message.body.FBXExportGenerateLog)
    pm.mel.FBXExportInAscii(v=message.body.FBXExportInAscii)
    pm.mel.FBXExportReferencedAssetsContent(v=message.body.FBXExportReferencedAssetsContent)
    pm.mel.FBXExportSmoothMesh(v=message.body.FBXExportSmoothMesh)
    pm.mel.FBXExportSkeletonDefinitions(v=message.body.FBXExportSkeletonDefinitions)
    pm.mel.FBXExportUseSceneName(v=message.body.FBXExportUseSceneName)
    pm.mel.FBXExportAnimationOnly(v=message.body.FBXExportAnimationOnly)

    if message.body.export_selected:
        pm.mel.FBXExport(f=message.body.filepath.as_posix(), s=True)
    else:
        pm.mel.FBXExport(f=message.body.filepath.as_posix())


def import_fbx(message: asset_messages.ImportFBX) -> None:
    """
    Imports a fbx file with the given parameters defined in the export_options object.

    args:
        message(ImportFBX): The message containing the fbx export options. Attributes
        are called as pymel.mel.FBXImport...() args.
    """
    pm.mel.FBXResetImport()

    pm.mel.FBXImportCameras(v=message.body.FBXImportCameras)
    pm.mel.FBXImportConstraints(v=message.body.FBXImportConstraints)
    pm.mel.FBXImportLights(v=message.body.FBXImportLights)
    pm.mel.FBXImportMode(v=message.body.FBXImportMode)
    pm.mel.FBXImportMergeAnimationLayers(v=message.body.FBXImportMergeAnimationLayers)
    pm.mel.FBXImportScaleFactor(message.body.FBXImportScaleFactor)
    pm.mel.FBXImportShapes(v=message.body.FBXImportShapes)
    pm.mel.FBXImportSkins(v=message.body.FBXImportSkins)
    pm.mel.FBXImportUpAxis(message.body.FBXImportUpAxis)

    pm.mel.FBXImportCacheFile(v=message.body.FBXImportCacheFile)
    pm.mel.FBXImportFillTimeline(v=message.body.FBXImportFillTimeline)

    pm.mel.FBXImport(f=message.body.filepath.as_posix())


def export_ma(message: asset_messages.ExportMayaAscii) -> None:
    """
    Runs a maya.cmds.file export operation from the attributes of the given MayaAsciiExportOptions object.

    Args:
        message (ExportMayaAscii): The message of cmds.file() options.
    """
    file_args = {key: value for key, value in message.body.__dict__.items() if key != 'filepath'}
    maya.cmds.file(message.body.filepath.as_posix(), **file_args)


def import_ma(message: asset_messages.ImportMayaAscii) -> None:
    """
    Runs a maya.cmds.file import operation from the attributes of the given MayaAsciiImportOptions object.

    Args:
        message (ImportMayaAscii): The message of cmds.file() options.
    """
    file_args = {key: value for key, value in message.body.__dict__.items() if key != 'filepath'}
    maya.cmds.file(message.body.filepath.as_posix(), **file_args)


def export_mb(message: asset_messages.ExportMayaBinary) -> None:
    """
    Runs a maya.cmds.file export operation from the attributes of the given MayaBinaryExportOptions object.

    Args:
        message (ExportMayaBinary): The message of cmds.file() options.
    """
    file_args = {key: value for key, value in message.body.__dict__.items() if key != 'filepath'}
    maya.cmds.file(message.body.filepath.as_posix(), **file_args)


def import_mb(message: asset_messages.ImportMayaBinary) -> None:
    """
    Runes a maya.cmds.file import operation from the attributes of the given MayaBinaryImportOptions object.

    Args:
        message (ExportMayaBinary): The message of cmds.file() options.
    """
    file_args = {key: value for key, value in message.body.__dict__.items() if key != 'filepath'}
    maya.cmds.file(message.body.filepath.as_posix(), **file_args)


def reference_ma(message: asset_messages.ReferenceMayaAscii) -> None:
    """
    Runs a maya.cmds.file reference operation from the attributes of the given MayaAsciiReferenceOptions object.

    Args:
        message (ReferenceMayaAscii): The message of cmds.file() options.
    """
    file_args = {key: value for key, value in message.body.__dict__.items() if key != 'filepath'}
    maya.cmds.file(message.body.filepath.as_posix(), **file_args)


def swap_reference(message: asset_messages.SwapReferenceMayaAscii) -> None:
    """
    Runs a maya.cmds.file swap reference operation from the attributes of the given MayaAsciiReferenceOptions object.

    Args:
        message (ReferenceMayaAscii): The message of cmds.file() options.
    """
    file_args = {key: value for key, value in message.body.__dict__.items() if key != 'filepath'}
    maya.cmds.file(**file_args)


def export_abc(message: asset_messages.ExportABC) -> None:
    """
    Runs a maya.cmds.AbcExport operation from the attributes of the given ABCExportOptions object.

    Args:
        message (ExportABC): The message of cmds.file() options.
    """
    file_args = {key: value for key, value in message.body.__dict__.items() if key != 'filepath'}
    maya.cmds.file(**file_args)


def import_abc() -> None:
    raise NotImplementedError


def register_messages() -> None:
    """Subscribe related library functions to message types."""
    asset_channel = router.get_channel(const.DomainChannels.MODEL.value)
    asset_channel.register_subscriber(asset_messages.OpenFileDialog, open_file_dialog)
    asset_channel.register_subscriber(asset_messages.OpenFile, open_file)

    asset_channel.register_subscriber(asset_messages.ExportFBX, export_fbx)
    asset_channel.register_subscriber(asset_messages.ImportFBX, import_fbx)

    asset_channel.register_subscriber(asset_messages.ExportMayaAscii, export_ma)
    asset_channel.register_subscriber(asset_messages.ImportMayaAscii, import_ma)
    asset_channel.register_subscriber(asset_messages.ReferenceMayaAscii, reference_ma)
    asset_channel.register_subscriber(asset_messages.SwapReferenceMayaAscii, swap_reference)

    asset_channel.register_subscriber(asset_messages.ExportMayaBinary, export_mb)
    asset_channel.register_subscriber(asset_messages.ImportMayaBinary, import_mb)

    asset_channel.register_subscriber(asset_messages.ExportABC, export_abc)

"""
Lucid Maya IO Library

* Description

    A library for handling io operations in maya for the Lucid pipeline.

* Update History

    `2023-09-22` - Init
"""


from pathlib import Path
from typing import Optional

import maya.cmds
import pymel.core as pm


class MayaAsciiImportOptions(object):
    """
    Base maya.cmds.file() flags for importing an ascii file to maya.

    Information on args can be found here:
        https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    def __init__(self):
        self.i: bool = True
        self.filepath: Path = Path()
        self.defaultNamespace: bool = False
        self.groupReference: bool = False
        self.groupName: str = ''
        self.mergeNamespacesOnClash: bool = False
        self.preserveReferences: bool = False
        self.removeDuplicateNetworks: bool = False
        self.returnNewNodes: bool = False
        self.renamingPrefix: str = ''
        self.type: str = 'mayaAscii'


class MayaAsciiExportOptions(object):
    """
    Base maya.cmds.file() flags for exporting an object to an maya ascii file.

    Information on args can be found here:
        https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    def __init__(self):
        self.filepath: Path = Path()
        self.save: bool = True
        self.constructionHistory: bool = False
        self.channels: bool = False
        self.constraints: bool = False
        self.expressions: bool = False
        self.shader: bool = False
        self.type: str = 'mayaAscii'


class MayaAsciiReferenceOptions(object):
    """
    Base maya.cmds.file() flags for referencing a maya ascii file.

    Information on args can be found here:
        https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    def __init__(self):
        self.filepath: Path = Path()
        self.reference: bool = True
        self.defaultNamespace: bool = False
        self.deferReference: bool = False
        self.groupReference: bool = False
        self.groupLocator: bool = False
        self.groupName: str = ''
        self.mergeNamespacesOnClash: bool = False
        self.namespace: str = ''
        self.referenceNode: str = ''
        self.sharedReferenceFile: bool = False
        self.returnNewNodes: bool = False


class MayaBinaryImportOptions(object):
    """
    Base maya.cmds.file() flags for importing an binary file to maya.

    Information on args can be found here:
        https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    def __init__(self):
        self.i: bool = True
        self.filepath: Path = Path()
        self.defaultNamespace: bool = False
        self.groupReference: bool = False
        self.groupName: str = ''
        self.mergeNamespacesOnClash: bool = False
        self.preserveReferences: bool = False
        self.removeDuplicateNetworks: bool = False
        self.returnNewNodes: bool = False
        self.renamingPrefix: str = ''
        self.type: str = 'mayaBinary'


class MayaBinaryExportOptions(object):
    """
    Base maya.cmds.file() flags for exporting an object to an maya binary file.

    Information on args can be found here:
        https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    def __init__(self):
        self.filepath: Path = Path()
        self.save: bool = True
        self.constructionHistory: bool = False
        self.channels: bool = False
        self.constraints: bool = True
        self.expressions: bool = False
        self.shader: bool = True
        self.type: str = 'mayaBinary'


class FBXExportOptions(object):
    """
    Object class for the pymel.mel.FBXExport() options. This is intended to be used to define
    objects for mel.FBXExport() flags so developers do not need to call the function itself as
    multiple end points within a tool.

    Information on args can be found here:
        https://help.autodesk.com/view/MAYACRE/ENU/?guid=GUID-6CCE943A-2ED4-4CEE-96D4-9CB19C28F4E0
    """
    def __init__(self):
        self.filepath: Path = Path()
        self.FBXExportCameras: bool = False
        self.FBXExportConstraints: bool = True
        self.FBXExportInputConnections: bool = True
        self.FBXExportUpAxis: str = 'y'
        self.FBXExportTriangulate: bool = False
        self.FBXExportIncludeChildren: bool = True
        self.FBXExportShapes: bool = True
        self.FBXExportScaleFactor: float = 1.0
        self.FBXExportInstances: bool = False
        self.FBXExportLights: bool = True
        self.FBXExportSkins: bool = True

        self.export_selected: bool = False

        self.FBXExportEmbeddedTextures: bool = False
        self.FBXExportFileVersion: str = 'FBX202000'
        self.FBXExportGenerateLog: bool = False
        self.FBXExportInAscii: bool = True
        self.FBXExportReferencedAssetsContent: bool = False
        self.FBXExportSmoothMesh: bool = True
        self.FBXExportSkeletonDefinitions: bool = True
        self.FBXExportUseSceneName: bool = False
        self.FBXExportAnimationOnly: bool = False

        self.filepath: Path


class FBXImportOptions(object):
    """
    Object class for the pymel.mel.FBXImport() options. This is intended to be used to define
    objects for mel.FBXImport() flags so developers do not need to call the function itself as
    multiple end points within a tool.

    Information on args can be found here:
        https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=GUID-699CDF74-3D64-44B0-967E-7427DF800290
    """
    def __init__(self):
        self.filepath: Path = Path()
        self.FBXImportCameras: bool = True
        self.FBXImportConstraints: bool = True
        self.FBXImportLights: bool = True
        self.FBXImportUpAxis: str = 'y'
        self.FBXImportMode: str = 'add'  # modes: add, exmerge, merge
        self.FBXImportMergeAnimationLayers: bool = True
        self.FBXImportShapes: bool = True
        self.FBXImportSkins: bool = True
        self.FBXImportScaleFactor: float = 1.0

        self.FBXImportCacheFile = False
        self.FBXImportFillTimeline = False


class ABCExportOptions(object):
    """
    Object class for the maya.cmds.ABCExport() options. This is intended to be used to define
    objects for cmds.ABCExport() flags so developers do not need to call the function itself as
    multiple end points within a tool.

    Information on args can be found with:
        cmds.AbcExport(h=True) in maya script editor
    """
    def __init__(self):
        self.filepath: Path = Path()
        self.preRollStartFrame: int = 1001
        self.dontSkipUnwrittenFrames: bool = False
        self.verbose: bool = False
        self.jobArg: str = ''
        self.attr: str = ''  # not 100% sure what to do about this, as it can show up multiple times
        self.autoSubd: bool = False
        self.attrPrefix: str = 'ABC_'
        self.dataFormat: str = ''
        self.eulerFilter: bool = False
        self.file: str = ''
        self.frameRange: list[int] = [1001, 1100]
        self.frameRelativeSample: float = 0
        self.noNormals: bool = False
        self.preRoll: bool = False
        self.renderableOnly: bool = False
        self.step: float = 1.0
        self.selection: bool = False
        self.stripNamespaces: Optional[int]


class ABCImportOptions(object):
    """
    Object class for the maya.cmds.ABCImport() options. This is intended to be used to define
    objects for cmds.ABCImport() flags so developers do not need to call the function itself as
    multiple end points within a tool.

    Information on args can be found with:
        cmds.AbcImport(h=True) in maya script editor
    """
    pass


def open_file_dialog(starting_path: Optional[Path] = None) -> Optional[Path]:
    """
    Show Maya (.ma, .mb) file open dialog, and return path, or None if cancelled.

    Args:
        starting_path(Optional[Path]): The starting path for the file dialog if folder
        is not within maya project files.

    Returns:
        Optional[Path]: The path selected from the dialog window.
    """
    path = maya.cmds.fileDialog2(
        startingDirectory=starting_path,
        fileFilter='Maya Files (*.ma *.mb)',
        fileMode=1,  # A single existing file
        dialogStyle=2,  # Maya style dialog (1 is OS style)
        setProjectBtnEnabled=False
    )

    if path is not None:
        path = Path(path[0])  # If not cancelled, fileDialog returns list[str]

    return path


def open_file(file_path: Path) -> Path:
    """
    Force open a Maya (.ma, .mb) file. Does *not* prompt user if unsaved changes in scene.

    Args:
        file_path(Path): The path to the file to open.

    Returns
        Path: The name of the opened file.
    """
    return maya.cmds.file(
        file_path,
        open=True,
        force=True,  # Force an action to take place. Open file even if there are unsaved changes in current scene.
        ignoreVersion=True  # "Used to open files with versions other than those officially supported. Success is not guaranteed. Data loss, data corruption or failure to open are all possible outcomes."
    )


def export_fbx(export_options: FBXExportOptions) -> Path:
    """
    Exports a fbx file with the given parameters defined in the export_options object.

    args:
        export_options(FBXExportOptions): The class containing the fbx export options. Attributes
        are called as pymel.mel.FBXExport...() args.

    return:
        Path: The Path to the exported file.
    """
    pm.mel.FBXResetExport()

    pm.mel.FBXExportConstraints(v=export_options.FBXExportConstraints)
    pm.mel.FBXExportCameras(v=export_options.FBXExportCameras)
    pm.mel.FBXExportInputConnections(v=export_options.FBXExportInputConnections)
    pm.mel.FBXExportUpAxis(export_options.FBXExportUpAxis)
    pm.mel.FBXExportTriangulate(v=export_options.FBXExportTriangulate)
    pm.mel.FBXExportIncludeChildren(v=export_options.FBXExportIncludeChildren)
    pm.mel.FBXExportScaleFactor(export_options.FBXExportScaleFactor)
    pm.mel.FBXExportShapes(v=export_options.FBXExportShapes)
    pm.mel.FBXExportSkins(v=export_options.FBXExportSkins)
    pm.mel.FBXExportInstances(v=export_options.FBXExportInstances)
    pm.mel.FBXExportLights(v=export_options.FBXExportLights)

    pm.mel.FBXExportEmbeddedTextures(v=export_options.FBXExportEmbeddedTextures)
    pm.mel.FBXExportFileVersion(v=export_options.FBXExportFileVersion)
    pm.mel.FBXExportGenerateLog(v=export_options.FBXExportGenerateLog)
    pm.mel.FBXExportInAscii(v=export_options.FBXExportInAscii)
    pm.mel.FBXExportReferencedAssetsContent(v=export_options.FBXExportReferencedAssetsContent)
    pm.mel.FBXExportSmoothMesh(v=export_options.FBXExportSmoothMesh)
    pm.mel.FBXExportSkeletonDefinitions(v=export_options.FBXExportSkeletonDefinitions)
    pm.mel.FBXExportUseSceneName(v=export_options.FBXExportUseSceneName)
    pm.mel.FBXExportAnimationOnly(v=export_options.FBXExportAnimationOnly)

    if export_options.export_selected:
        pm.mel.FBXExport(f=export_options.filepath.as_posix(), s=True)
    else:
        pm.mel.FBXExport(f=export_options.filepath.as_posix())

    return export_options.filepath


def import_fbx(import_options: FBXImportOptions) -> None:
    """
    Imports a fbx file with the given parameters defined in the export_options object.

    args:
        import_options(FBXImportOptions): The class containing the fbx export options. Attributes
        are called as pymel.mel.FBXImport...() args.
    """
    pm.mel.FBXResetImport()

    pm.mel.FBXImportCameras(v=import_options.FBXImportCameras)
    pm.mel.FBXImportConstraints(v=import_options.FBXImportConstraints)
    pm.mel.FBXImportLights(v=import_options.FBXImportLights)
    pm.mel.FBXImportMode(v=import_options.FBXImportMode)
    pm.mel.FBXImportMergeAnimationLayers(v=import_options.FBXImportMergeAnimationLayers)
    pm.mel.FBXImportScaleFactor(import_options.FBXImportScaleFactor)
    pm.mel.FBXImportShapes(v=import_options.FBXImportShapes)
    pm.mel.FBXImportSkins(v=import_options.FBXImportSkins)
    pm.mel.FBXImportUpAxis(import_options.FBXImportUpAxis)

    pm.mel.FBXImportCacheFile(v=import_options.FBXImportCacheFile)
    pm.mel.FBXImportFillTimeline(v=import_options.FBXImportFillTimeline)

    pm.mel.FBXImport(f=import_options.filepath.as_posix())


def export_ma(options: MayaAsciiExportOptions) -> Path:
    """
    Runs a maya.cmds.file export operation from the attributes of the given MayaAsciiExportOptions object.

    Args:
        options (MayaAsciiExportOptions): The object of cmds.file() options.

    return:
        Path: The Path to the exported file.
    """
    file_args = {key: value for key, value in options.__dict__.items() if key != 'filepath'}

    maya.cmds.file(rename=options.filepath)
    maya.cmds.file(options.filepath.parent, **file_args)

    return options.filepath


def import_ma(options: MayaAsciiImportOptions) -> str:
    """
    Runs a maya.cmds.file import operation from the attributes of the given MayaAsciiImportOptions object.

    Args:
        options (MayaAsciiImportOptions): The object of cmds.file() options.

    Returns:
        str: The maya.cmds.file() return value.
    """
    file_args = {key: value for key, value in options.__dict__.items() if key != 'filepath'}

    maya.cmds.file(rename=options.filepath)
    val = maya.cmds.file(options.filepath.parent, **file_args)
    return val


def export_mb(options: MayaBinaryExportOptions) -> Path:
    """
    Runs a maya.cmds.file export operation from the attributes of the given MayaBinaryExportOptions object.

    Args:
        options (MayaBinaryExportOptions): The object of cmds.file() options.

    return:
        list[Path]: a list of paths to all exported files. [0] should be __pub__ and [1] should be
        __work__.
    """
    file_args = {key: value for key, value in options.__dict__.items() if key != 'filepath'}

    maya.cmds.file(rename=options.filepath)
    maya.cmds.file(options.filepath.parent, **file_args)

    return options.filepath


def import_mb(options: MayaBinaryImportOptions) -> str:
    """
    Runes a maya.cmds.file import operation from the attributes of the given MayaBinaryImportOptions object.

    Args:
        options (MayaBinaryImportOptions): The object of cmds.file() options.

    Returns:
        str: The maya.cmds.file() return value.
    """
    file_args = {key: value for key, value in options.__dict__.items() if key != 'filepath'}

    maya.cmds.file(rename=options.filepath)
    val = maya.cmds.file(options.filepath.parent, **file_args)
    return val


def reference_ma(options: MayaAsciiReferenceOptions) -> str:
    """
    Runs a maya.cmds.file reference operation from the attributes of the given MayaAsciiReferenceOptions object.

    Args:
        options (MayaAsciiReferenceOptions): The object of cmds.file() options.

    Returns:
        str: The maya.cmds.file() return value.
    """
    file_args = {key: value for key, value in options.__dict__.items() if key != 'filepath'}

    maya.cmds.file(rename=options.filepath)
    val = maya.cmds.file(options.filepath.parent, **file_args)
    return val


def swap_reference(options: MayaAsciiReferenceOptions) -> str:
    """
    Runs a maya.cmds.file swap reference operation from the attributes of the given MayaAsciiReferenceOptions object.

    Args:
        options (MayaAsciiReferenceOptions): The object of cmds.file() options.

    Returns:
        the maya.cmds.file() return value.
    """
    file_args = {key: value for key, value in options.__dict__.items() if key != 'filepath'}
    val = maya.cmds.file(**file_args)
    return val


def export_abc(options: ABCExportOptions) -> Path:
    """
    Runs a maya.cmds.AbcExport operation from the attributes of the given ABCExportOptions object.

    Args:
        options (ABCExportOptions): The object of cmds.file() options.

    Returns:
        Path: The alembic file export path.
    """
    file_args = {key: value for key, value in options.__dict__.items() if key != 'filepath'}
    maya.cmds.file(**file_args)

    return ABCExportOptions.filepath


def import_abc() -> None:
    raise NotImplementedError

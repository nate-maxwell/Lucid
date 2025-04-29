"""
# Lucid Asset Message Objects

* Description:

    The message objects used for asset IO domain in Maya.
"""


from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Optional

from lucid import const
from lucid.system.messaging import message


@dataclass
class OpenFileBody(message.MessageBody):
    filepath: Path


class OpenFile(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = OpenFileBody(filepath)


@dataclass
class OpenFileDialogBody(message.MessageBody):
    filepath: Optional[Path]


class OpenFileDialog(message.Command):
    def __init__(self, filepath: Optional[Path] = None) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = OpenFileDialogBody(filepath)


@dataclass
class OpenFileDialogResponseBody(message.MessageBody):
    filepath: Optional[Path]


class OpenFileDialogResponse(message.Document):
    def __init__(self, filepath: Optional[Path] = None) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = OpenFileDialogResponseBody(filepath)


@dataclass
class ImportMayaAsciiBody(message.MessageBody):
    """
    Base maya.cmds.file() flags for importing an ascii file to maya.
    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found here:
    https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    filepath: Path
    i: bool = True
    defaultNamespace: bool = False
    groupReference: bool = False
    groupName: str = ''
    mergeNamespacesOnClash: bool = False
    preserveReferences: bool = False
    removeDuplicateNetworks: bool = False
    returnNewNodes: bool = False
    renamingPrefix: str = ''
    type: str = 'mayaAscii'


class ImportMayaAscii(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ImportMayaAsciiBody(filepath)


@dataclass
class ExportMayaAsciiBody(message.MessageBody):
    """
    Base maya.cmds.file() flags for exporting an object to an maya ascii file.
    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found here:
    https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    filepath: Path
    save: bool = True
    constructionHistory: bool = False
    channels: bool = False
    constraints: bool = False
    expressions: bool = False
    shader: bool = False
    type: str = 'mayaAscii'


class ExportMayaAscii(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ExportMayaAsciiBody(filepath)


@dataclass
class ReferenceMayaAsciiBody(message.MessageBody):
    """
    Base maya.cmds.file() flags for referencing a maya ascii file.
    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found here:
    https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    filepath: Path
    reference: bool = True
    defaultNamespace: bool = False
    deferReference: bool = False
    groupReference: bool = False
    groupLocator: bool = False
    groupName: str = ''
    mergeNamespacesOnClash: bool = False
    namespace: str = ''
    referenceNode: str = ''
    sharedReferenceFile: bool = False
    returnNewNodes: bool = False


class ReferenceMayaAscii(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ReferenceMayaAsciiBody(filepath)


class SwapReferenceMayaAscii(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ReferenceMayaAsciiBody(filepath)


@dataclass
class ImportMayaBinaryBody(message.MessageBody):
    """
    Base maya.cmds.file() flags for importing a binary file to maya.
    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found here:
    https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    filepath: Path
    i: bool = True
    defaultNamespace: bool = False
    groupReference: bool = False
    groupName: str = ''
    mergeNamespacesOnClash: bool = False
    preserveReferences: bool = False
    removeDuplicateNetworks: bool = False
    returnNewNodes: bool = False
    renamingPrefix: str = ''
    type: str = 'mayaBinary'


class ImportMayaBinary(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ImportMayaBinaryBody(filepath)


@dataclass
class ExportMayaBinaryBody(message.MessageBody):
    """
    Base maya.cmds.file() flags for exporting an object to a maya binary file.
    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found here:
    https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/
    """
    filepath: Path
    save: bool = True
    constructionHistory: bool = False
    channels: bool = False
    constraints: bool = True
    expressions: bool = False
    shader: bool = True
    type: str = 'mayaBinary'


class ExportMayaBinary(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ExportMayaBinaryBody(filepath)


@dataclass
class ExportFBXBody(message.MessageBody):
    """
    Object class for the pymel.mel.FBXExport() options.
    This is intended to be used to define objects for mel.FBXExport() flags so
    developers do not need to call the function itself as multiple end points
    within a tool.

    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found here:
    https://help.autodesk.com/view/MAYACRE/ENU/?guid=GUID-6CCE943A-2ED4-4CEE-96D4-9CB19C28F4E0
    """
    filepath: Path
    FBXExportCameras: bool = False
    FBXExportConstraints: bool = True
    FBXExportInputConnections: bool = True
    FBXExportUpAxis: str = 'y'
    FBXExportTriangulate: bool = False
    FBXExportIncludeChildren: bool = True
    FBXExportShapes: bool = True
    FBXExportScaleFactor: float = 1.0
    FBXExportInstances: bool = False
    FBXExportLights: bool = True
    FBXExportSkins: bool = True

    export_selected: bool = False

    FBXExportEmbeddedTextures: bool = False
    FBXExportFileVersion: str = 'FBX202000'
    FBXExportGenerateLog: bool = False
    FBXExportInAscii: bool = True
    FBXExportReferencedAssetsContent: bool = False
    FBXExportSmoothMesh: bool = True
    FBXExportSkeletonDefinitions: bool = True
    FBXExportUseSceneName: bool = False
    FBXExportAnimationOnly: bool = False


class ExportFBX(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ExportFBXBody(filepath)


@dataclass
class ImportFBXBody(message.MessageBody):
    """
    Object class for the pymel.mel.FBXImport() options. This is intended to be
    used to define objects for mel.FBXImport() flags so developers do not need
    to call the function itself as multiple end points within a tool.

    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found here:
    https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=GUID-699CDF74-3D64-44B0-967E-7427DF800290
    """
    filepath: Path
    FBXImportCameras: bool = True
    FBXImportConstraints: bool = True
    FBXImportLights: bool = True
    FBXImportUpAxis: str = 'y'
    FBXImportMode: str = 'add'  # modes: add, exmerge, merge
    FBXImportMergeAnimationLayers: bool = True
    FBXImportShapes: bool = True
    FBXImportSkins: bool = True
    FBXImportScaleFactor: float = 1.0

    FBXImportCacheFile = False
    FBXImportFillTimeline = False


class ImportFBX(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ImportFBXBody(filepath)


@dataclass
class ExportABCBody(message.MessageBody):
    """
    Object class for the maya.cmds.ABCExport() options. This is intended to be used to define
    objects for cmds.ABCExport() flags so developers do not need to call the function itself as
    multiple end points within a tool.

    Attrs match names of cmds.file() args so that the class __dict__ can be
    passed through.

    Information on args can be found with:
    cmds.AbcExport(h=True) in maya script editor
    """
    filepath: Path = Path()
    preRollStartFrame: int = 1001
    dontSkipUnwrittenFrames: bool = False
    verbose: bool = False
    jobArg: str = ''
    attr: str = ''  # not 100% sure what to do about this, as it can show up multiple times
    autoSubd: bool = False
    attrPrefix: str = 'ABC_'
    dataFormat: str = ''
    eulerFilter: bool = False
    file: str = ''
    frameRange: list[int] = field(default_factory=lambda: [1001, 1100])
    frameRelativeSample: float = 0
    noNormals: bool = False
    preRoll: bool = False
    renderableOnly: bool = False
    step: float = 1.0
    selection: bool = False
    stripNamespaces: int = 0


class ExportABC(message.Command):
    def __init__(self, filepath: Path) -> None:
        super().__init__(const.MODEL_CHAN)
        self.body = ExportABCBody(filepath)

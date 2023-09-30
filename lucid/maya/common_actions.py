"""
# Maya Common User Actions

* Update History

    `1.0.0` - Init

* Description

    Common user actions to conveniently put on a shelf.
"""


import maya.cmds as cmds


def delete_history():
    for obj in cmds.ls(sl=True):
        cmds.delete(obj, ch=True)


def delete_all_non_deformer_history():
    geometry = cmds.ls(geometry=True)
    transforms = cmds.listRelatives(geometry, p=True, path=True)
    cmds.select(transforms, r=True)
    cmds.bakePartialHistory(cmds.ls(sl=True), prePostDeformers=True)


def center_pivot():
    for obj in cmds.ls(sl=True):
        center = cmds.objectCenter(obj, gl=True)
        cmds.xform(obj, centerPivots=True)


def freeze_transforms():
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

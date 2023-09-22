"""
# Maya User Setup

* Description

    Lucid's maya initialization

* Update History

    `2023-09-21` - Init
"""


import maya.cmds as cmds

import lucid.maya.shelves


def declare_pipeline():
    print('[LUCID PIPELINE INITIALIZATION] - Hello Dreamworld.')

cmds.evalDeferred(declare_pipeline, lowestPriority=True)
cmds.evalDeferred(lucid.maya.shelves.main, lowestPriority=True)

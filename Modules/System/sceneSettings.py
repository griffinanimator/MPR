import maya.cmds as cmds
import os
import sys
import __main__


def sceneSetup():
    cmds.currentUnit(linear="m")
    cmds.setAttr("perspShape.nearClipPlane", 0.001)
    cmds.setAttr("perspShape.farClipPlane", 10000)
    cmds.grid(size=10, spacing=5.0, d=5)
    cmds.currentUnit( time='ntscf' )
    
def startEndFrame():
    cmds.playbackOptions( minTime='0sec')
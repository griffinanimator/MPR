import maya.cmds as cmds

import System.blueprint as blueprintMod
#reload(blueprintMod)

import Blueprint.singleOrientableJoint as singleOrientableJoint
#reload(singleOrientableJoint)

import System.utils as utils
#reload(utils)

import os

CLASS_NAME = "ParentJoint"

TITLE = "Parent Joint"
DESCRIPTION = "This module will not accept animation controls.  Suggested use: Parent Joint"
ICON = os.environ["GEPPETTO"] + "/Icons/parent_button.bmp"
# 095
class ParentJoint(singleOrientableJoint.SingleOrientableJoint):
    def __init__(self, userSpecifiedName, hookObject):
        
        # The following allows for install with default functionality
        jointInfo = [ ["parent_1_joint", [0.0, 0.0, 0.0]] ]
        
        gameJntNames = ["parent_"]   
                     
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=1)
        # The previous allows for install with default functionality
          
 
        
    def lock_phase1(self):
        moduleInfo = list(singleOrientableJoint.SingleOrientableJoint.lock_phase1(self))
        moduleInfo[5]=True
        return moduleInfo
        
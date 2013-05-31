import maya.cmds as cmds

import System.blueprint as blueprintMod
#reload(blueprintMod)

import Blueprint.singleOrientableJoint as singleOrientableJoint
#reload(singleOrientableJoint)

import System.utils as utils
reload(utils)

import os

CLASS_NAME = "RootTransform"

TITLE = "Root Transform"
DESCRIPTION = "Creates a single joint with control for position and orientation. Once created (locked)  the joint can rotate, translate, and scale.  Suggested use: Global control"
ICON = os.environ["GEPPETTO"] + "/Icons/root_button.bmp"
# 095
class RootTransform(singleOrientableJoint.SingleOrientableJoint):
    def __init__(self, userSpecifiedName, hookObject):
        
        # The following allows for install with default functionality
        jointInfo = [ ["root_1_joint", [0.0, 0.0, 0.0]] ]
        
        gameJntNames = ["root_"]
                     
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=2)
        # The previous allows for install with default functionality
          
 
        
    def lock_phase1(self):
        moduleInfo = list(singleOrientableJoint.SingleOrientableJoint.lock_phase1(self))
        moduleInfo[5]=True
        return moduleInfo
        
        
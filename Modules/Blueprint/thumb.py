import maya.cmds as cmds
import os
# derive functionality from finger module
import Blueprint.finger as finger

import System.utils as utils

import System.blueprint as blueprintMod
#reload(blueprintMod)

CLASS_NAME = "Thumb"

TITLE = "Thumb"
DESCRIPTION = "Creates 5 joints, defining a Thumb. Suggested use: Thumb"
ICON = os.environ["GEPPETTO"] + "/Icons/thumbMod_button.bmp"
# 095
class Thumb(finger.Finger):
    def __init__(self, userSpecifiedName, hookObject):
        
        # The following allows for install with default functionality
        jointInfo = [ ["thumb_1_joint", [0.0, 0.0, 0.0]], ["thumb_2_joint", [4.0, 0.0, 0.0]], ["thumb_3_joint", [8.0, 0.0, 0.0]], ["thumb_4_joint", [12.0, 0.0, 0.0]] ]
        gameJntNames = ["thumb1_", "thumb2_", "thumb3_", "thumb4_"]
                     
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=0)
        # The previous allows for install with default functionality


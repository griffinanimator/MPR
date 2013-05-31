import maya.cmds as cmds
import os
# derive functionality from finger module
import Blueprint.finger as finger

import System.utils as utils

import System.blueprint as blueprintMod
#reload(blueprintMod)

CLASS_NAME = "HipJoint"

TITLE = "Hip Joint"
DESCRIPTION = "Creates a single joint with control for position and orientation. Once created (locked)  the joint can only rotate. "
ICON = os.environ["GEPPETTO"] + "/Icons/singleJoint_button.bmp"
# 095
class HipJoint(blueprintMod.Blueprint):
    def __init__(self, userSpecifiedName, hookObject):
        
        # The following allows for install with default functionality
        jointInfo = [ ["hip_1_joint", [0.0, 0.0, 0.0]] ]
        
        gameJntNames = ["hip_"]
                     
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=0)
        # The previous allows for install with default functionality
        
    # override the base class and add custom attributes    
    def install_custom(self, joints):
        self.createSingleJointOrientationControlAtJoint(joints[0])

    # 102
    def mirror_custom(self, originalModule):
        jointName = self.jointInfo[0][0]
        originalJoint = originalModule+":"+jointName
        newJoint = self.moduleNamespace+":"+jointName
        
        originalOrientationControl = self.getSingleJointOrientationControl(originalJoint)
        newOrientationControl = self.getSingleJointOrientationControl(newJoint)
        
        oldRotation = cmds.getAttr(originalOrientationControl+".rotate")[0]
        cmds.setAttr(newOrientationControl+".rotate", oldRotation[0], oldRotation[1], oldRotation[2], type="double3" )
        
    def UI_custom(self):
        joints = self.getJoints()
        self.createRotationOrderUIControl(joints[0])
        
        
    def lock_phase1(self):
        # GAther and return all required information from this modules control objects.
        # Joint Positions = list of joint positions from the root down the hierarchy
        # Joint orientations = a list of orientations, or a list of axis information  ( orient joint and secondaryAxisOrient from
        #                       # These are passed in the following tuple: ( orientstions, None) or ( NOne, axis info)
        # JointRotationOrders = a list of joint rotation orders ( integer values gathered with getAttr)
        # jointPreferred Angles = a list of joint preferred angles, optional (can pass None)
        # hookObjedct = self.findHookObjectForLock()
        # rootTransform = a bool, either True or False. True = R, T, and S on root joint.  False = R only.
        # 
        # moduleInfo = (jointPositions , jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform
        # Return moduleInfo
        

        jointPositions = []
        jointOrientationValues = []
        jointRotationOrders =[]

        joint = self.getJoints()[0]
        
        jointPositions.append(cmds.xform(joint, q=True, worldSpace=True, translation=True))
   
        jointOrientationValues.append(cmds.xform(self.getSingleJointOrientationControl(joint), q=True, worldSpace=True, rotation=True))
        jointOrientations = (jointOrientationValues, None)

        jointRotationOrders.append(cmds.getAttr(joint+".rotateOrder"))
        
        jointPreferredAngles = None
        hookObject = self.findHookObjectForLock()
        rootTransform = False
        
        moduleNamespace = self.moduleNamespace
            
        moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform, moduleNamespace)
        return moduleInfo
        
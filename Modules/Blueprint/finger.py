import maya.cmds as cmds
import os

import System.utils as utils
import System.blueprint as blueprintMod
#reload(blueprintMod)

CLASS_NAME = "Finger"

TITLE = "Finger"
DESCRIPTION = "Creates 5 joints, defining a finger. Suggested use: Finger"
ICON = os.environ["GEPPETTO"] + "/Icons/fingerMod_button.bmp"
# 095
class Finger(blueprintMod.Blueprint):
    def __init__(self, userSpecifiedName, hookObject):
        
        # The following allows for install with default functionality
        jointInfo = [ ["fing_1_joint", [0.0, 0.0, 0.0]], ["fing_2_joint", [2.0, 0.0, 0.0]], ["fing_3_joint", [4.0, 0.0, 0.0]], ["fing_4_joint", [6.0, 0.0, 0.0]] ]
        
        gameJntNames = ["fing1_", "fing2_", "fing3_", "fing4_"]
                    
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=0)
        # The previous allows for install with default functionality

    # override the base class and add custom attributes    
    def install_custom(self, joints):
        for i in range (len(joints) -1):
            cmds.setAttr(joints[i]+".rotateOrder", 3) #xzy
            
            self.createOrientationControl(joints[i], joints[i+1])
            
            paControl = self.createPreferredAngleRepresentation(joints[i], self.getTranslationControl(joints[i]), childOfOrientationControl=True)
            cmds.setAttr(paControl+".axis", 3) #-Z Axis
            
        if not self.mirrored:
            cmds.setAttr(self.moduleNamespace+":module_transform.globalScale", 1)
            
    # 097
    def mirror_custom(self, originalModule):
        for i in range(len(self.jointInfo)-1):
            jointName = self.jointInfo[i][0]
            originalJoint = originalModule+":"+jointName
            newJoint = self.moduleNamespace+":"+jointName
            
            originalOrientationControl = self.getOrientationControl(originalJoint)
            newOrientationControl = self.getOrientationControl(newJoint)
            
            cmds.setAttr(newOrientationControl+".rotateX", cmds.getAttr(originalOrientationControl+".rotateX"))
            
            # Found in blueprint getPreferredAngleControl
            originalPreferredAngleControl = self.getPreferredAngleControl(originalJoint)
            newPreferredAngleControl = self.getPreferredAngleControl(newJoint)
            
            cmds.setAttr(newPreferredAngleControl+".axis", cmds.getAttr(originalPreferredAngleControl+".axis"))
            
    # 098
    def UI_custom(self):
        joints = self.getJoints()
        joints.pop()
        
        for joint in joints:
            self.createRotationOrderUIControl(joint)
            
        for joint in joints:
            self.createPreferredAngleUIControl(self.getPreferredAngleControl(joint))
            
    def lock_phase1(self):
        # GAther and return all required information from this modules control objects.
        # Joint Positions = list of joint positions from the root down the hierarchy
        # Joint orientations = a list of orientations, or a list of axis information  ( orient joint and secondaryAxisOrient from
        #                       # These are passed in the following tuple: ( orientstions, None) or ( NOne, axis info)
        # JointRotationOrders = a list of joint rotation orders ( integer values gathered with getAttr)
        # jointPreferred Angles = a list of joint preferred angles, optional (can pass None)
        # hookObject = self.findHookObjectForLock()
        # rootTransform = a bool, either True or False. True = R, T, and S on root joint.  False = R only.
        # 
        # moduleInfo = (jointPositions , jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform
        # Return moduleInfo
        
        
        jointPositions = []
        jointOrientationValues = []
        jointRotationOrders =[]
        jointPreferredAngles = []
        #v036
        joints = self.getJoints()
        
        index = 0
        cleanParent = self.moduleNamespace+":joints_grp"
        deleteJoints = []
        for joint in joints:
            jointPositions.append(cmds.xform(joint, q=True, worldSpace=True, translation=True))
            jointRotationOrders.append(cmds.getAttr(joint+".rotateOrder"))

            if index < len(joints) -1 :
                orientationInfo = self.orientationControlledJoint_getOrientation(joint, cleanParent)
                jointOrientationValues.append(orientationInfo[0])
                cleanParent = orientationInfo[1]
                deleteJoints.append(cleanParent)
                
                jointPrefAngles = [0.0, 0.0, 0.0]
                axis = cmds.getAttr(self.getPreferredAngleControl(joint)+".axis")
                
                if axis == 0:
                    jointPrefAngles[1] = 50.0
                elif axis == 1:
                    jointPrefAngles[1] = -50.0
                elif axis == 2:
                    jointPrefAngles[2] = 50.0
                elif axis == 3:
                    jointPrefAngles[2] = -50.0
                    
                jointPreferredAngles.append(jointPrefAngles)
                
            index += 1
            
        jointOrientations = (jointOrientationValues, None)
        
        cmds.delete(deleteJoints)
        
        hookObject = self.findHookObjectForLock()
        
        rootTransform = False
        
        moduleNamespace = self.moduleNamespace
            
        moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform, moduleNamespace)
        return moduleInfo
                
import maya.cmds as cmds
import os

import System.utils as utils
import System.blueprint as blueprintMod
#reload(blueprintMod)

CLASS_NAME = "SingleJointSegment"

TITLE = "Single Joint Segment"
DESCRIPTION = "Creates 2 joints, with control for 1 joints rotation order and orientation. Suggested use: Clavicle"
ICON = os.environ["GEPPETTO"] + "/Icons/singleChain_button.bmp"

class SingleJointSegment(blueprintMod.Blueprint):
    def __init__(self, userSpecifiedName, hookObject):
        jointInfo = [["sj_1_joint", [0.0, 0.0, 0.0]], ["sj_2_joint", [4.0, 0.0, 0.0]]] 
        
        gameJntNames = ["sj1_", "sj2_"]
              
        # Call on the blueprints initialization
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=0)
        #self.canBeMirrored
    def install_custom(self, joints):
        self.createOrientationControl(joints[0], joints[1])

    def lock_phase1(self):
        """ GAther and return all required information from this modules control objects.
         Joint Positions = list of joint positions from the root down the hierarchy
         Joint orientations = a list of orientations, or a list of axis information  ( orient joint and secondaryAxisOrient from
         These are passed in the following tuple: ( orientstions, None) or ( NOne, axis info)
         JointRotationOrders = a list of joint rotation orders ( integer values gathered with getAttr)
         jointPreferred Angles = a list of joint preferred angles, optional (can pass None)
         hookObjedct = self.findHookObjectForLock()
         rootTransform = a bool, either True or False. True = R, T, and S on root joint.  False = R only.         
         moduleInfo = (jointPositions , jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform
        Return moduleInfo"""
        
        jointPositions = []
        jointOrientationValues = []
        jointRotationOrders =[]
        #v036
        joints = self.getJoints()
        
        for joint in joints:
            jointPositions.append(cmds.xform(joint, q=True, worldSpace=True, translation=True))
        #v036 
        cleanParent = self.moduleNamespace+":joints_grp"    
        orientationInfo = self.orientationControlledJoint_getOrientation(joints[0], cleanParent)
        cmds.delete(orientationInfo[1])
        jointOrientationValues.append(orientationInfo[0])
        jointOrientations = (jointOrientationValues, None)

        jointRotationOrders.append(cmds.getAttr(joints[0]+".rotateOrder"))
        
        jointPreferredAngles = None
        hookObject = self.findHookObjectForLock()
        rootTransform = False
        
        moduleNamespace = self.moduleNamespace
            
        moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform, moduleNamespace)
        return moduleInfo
    
        #v046
    #Custom UI 
    def UI_custom(self):
        joints = self.getJoints()
        self.createRotationOrderUIControl(joints[0])
    # 081    
    def mirror_custom(self, originalModule):
        jointName = self.jointInfo[0][0]
        originalJoint = originalModule+":"+jointName
        newJoint = self.moduleNamespace+":"+jointName
        
        originalOrientationControl = self.getOrientationControl(originalJoint)
        newOrientationControl = self.getOrientationControl(newJoint)
        
        cmds.setAttr(newOrientationControl+".rotateX", cmds.getAttr(originalOrientationControl+".rotateX"))
        
        
        
    

    

    

         
        
 
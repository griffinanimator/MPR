import maya.cmds as cmds

import System.blueprint as blueprintMod
#reload(blueprintMod)

import System.utils as utils
reload(utils)

import Blueprint.hingeJoint as hingeJoint

import os

CLASS_NAME = "LegFoot"

TITLE = "Leg and Foot"
DESCRIPTION = "Creates 5 joints, the first 3 acting as hip, knee and ankle.  (A hinge Joint)   The last 2 acting as ball and toe.  Ideal Use: Leg and Foot."
ICON = os.environ["GEPPETTO"] + "/Icons/legMod_button.bmp"

class LegFoot(hingeJoint.HingeJoint):
    def __init__(self, userSpecifiedName, hookObject):
        jointInfo = [ ["leg_1_joint", [0.0, 0.0, 0.0]], ["leg_2_joint", [4.0, 0.0, -1.0]], ["leg_3_joint", [8.0, 0.0, 0.0]], ["leg_4_joint", [0.0, -9.0, 3.0]], ["leg_5_joint", [0.0, -9.0, 6.0]] ]
        
        gameJntNames = ["leg_1_", "leg_2_", "leg_3_", "leg_4_", "leg_5_"]       

        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=0)
        
    def install_custom(self, joints):
        hingeJoint.HingeJoint.install_custom(self, joints)
        
        ankleOrientationControl = self.createOrientationControl(joints[2], joints[3])
        ballOrientationControl = self.createOrientationControl(joints[3], joints[4])
        
        cmds.setAttr(ankleOrientationControl+".rotateX", 180)
        cmds.setAttr(ballOrientationControl+".rotateX", -90)
        
        cmds.xform(self.getTranslationControl(joints[1]), ws=True, a=True, translation=[0.0, -4.0, 1.0])
        cmds.xform(self.getTranslationControl(joints[2]), ws=True, a=True, translation=[0.0, -8.0, 0.0])
        
        for i in range(len(joints)-1):
            joint = joints[i]
            
            rotateOrder = 3 # xzy
            
            if i >= 2:
                rotateOrder = 0 # xyz
                
            cmds.setAttr(joint+".rotateOrder", rotateOrder)
            
    def mirror_custom(self, originalModule):
        for i in range(2, 4):
            jointName = self.jointInfo[i][0]
            originalJoint = originalModule+":"+jointName
            newJoint = self.moduleNamespace+":"+jointName
            
            originalOrientationControl = self.getOrientationControl(originalJoint)
            newOrientationControl = self.getOrientationControl(newJoint)
            
            cmds.setAttr(newOrientationControl+".rotateX", cmds.getAttr(originalOrientationControl+".rotateX"))
            
            
    def UI_custom(self):
        hingeJoint.HingeJoint.UI_custom(self)
        
        joints = self.getJoints()
        self.createRotationOrderUIControl(joints[2])
        self.createRotationOrderUIControl(joints[3])
        
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
        
        moduleInfo = hingeJoint.HingeJoint.lock_phase1(self)
        jointPositions = moduleInfo[0]
        jointOrientationValues = moduleInfo[1][0]
        jointRotationOrders = moduleInfo[2]
        
        joints = self.getJoints()
        for i in range(3, 5):
            joint = joints[i]
            print joint
            jointPositions.append(cmds.xform(joint, q=True, ws=True, t=True))
            jointRotationOrders.append(cmds.getAttr(joint+".rotateOrder"))
 
        cmds.lockNode(self.containerName, lock=False, lockUnpublished=False)
        
        jointNameInfo = utils.stripAllNamespaces(joints[1])

        cleanParent = jointNameInfo[0] + ":IK_" + jointNameInfo[1] # ikKnee
        deleteJoints = []
        for i in range(2, 4):
            orientationInfo = self.orientationControlledJoint_getOrientation(joints[i], cleanParent)
            jointOrientationValues.append(orientationInfo[0])
            cleanParent = orientationInfo[1]
            deleteJoints.append(cleanParent)
            
        cmds.delete(deleteJoints)
            
        cmds.lockNode(self.containerName, lock=True, lockUnpublished=True)
        
        return moduleInfo
        
        
        
            
            
        

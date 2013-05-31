import maya.cmds as cmds
import os

import System.utils as utils
import System.blueprint as blueprintMod
#reload(blueprintMod)

CLASS_NAME = "HingeJoint"

TITLE = "Hinge Joint"
DESCRIPTION = "Creates 3 joints (the middle joint acting as a hinge joint). Suggested use: Arm/leg"
ICON = os.environ["GEPPETTO"] + "/Icons/hinge_button.bmp"

class HingeJoint(blueprintMod.Blueprint):
    def __init__(self, userSpecifiedName, hookObject):
        jointInfo = [ ["hinge_1_joint", [0.0, 0.0, 0.0]], ["hinge_2_joint", [4, 0.0, -0.2]], ["hinge_3_joint", [8, 0.0, 0.0]] ]       
        
        gameJntNames = ["hinge1_", "hinge2_", "hinge3_"]
                
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=0)

    # 107
    def install_custom(self, joints):
        cmds.select(clear=True)
        ikJoints=[]
        
        if not self.mirrored:
            index = 0
            for joint in self.jointInfo:
                ikJoints.append(cmds.joint(n=self.moduleNamespace+":IK_"+joint[0], p=joint[1], absolute=True, rotationOrder="xyz"))
                
                cmds.setAttr(ikJoints[index]+".visibility", 0)
                
                if index != 0:
                	cmds.joint(ikJoints[index -1], edit=True, oj="xyz", sao="yup")
                	
                index += 1
        else:
            rootJointName = self.jointInfo[0][0]
            tempDuplicateNodes = cmds.duplicate(self.originalModule+":IK_"+rootJointName, renameChildren=True)
            
            cmds.delete(tempDuplicateNodes.pop())
            
            mirrorXY = False
            mirrorYZ = False
            mirrorXZ = False
            if self.mirrorPlane == "XY":
                mirrorXY = True
            elif self.mirrorPlane == "YZ":
                mirrorYZ = True
            elif self.mirrorPlane == "XZ":
                mirrorXZ = True
                
                
            mirrorBehavior = False
            if self.rotationFunction == "behavior":
                mirrorBehavior = True
                
            mirrorJoints = cmds.mirrorJoint(tempDuplicateNodes[0], mirrorXY=mirrorXY, mirrorXZ=mirrorXZ, mirrorYZ=mirrorYZ, mirrorBehavior=mirrorBehavior)
                
            cmds.delete(tempDuplicateNodes)
            
            cmds.xform(mirrorJoints[0], ws=True, a=True, translation=cmds.xform(self.moduleNamespace+":"+rootJointName, q=True, ws=True, t=True))
            
            for i in range(3):
                jointName = self.jointInfo[i][0]
                newName = cmds.rename(mirrorJoints[i], self.moduleNamespace+":IK_"+jointName)
                ikJoints.append(newName)
                              	
        utils.addNodeToContainer(self.containerName, ikJoints)
        
        for joint in ikJoints:
            jointName = utils.stripAllNamespaces(joint)[1]
            cmds.container(self.containerName, edit=True, publishAndBind=[joint+".rotate", jointName+"_R"])
            
        cmds.setAttr(ikJoints[0]+".preferredAngleY", -50.0)
        cmds.setAttr(ikJoints[1]+".preferredAngleY", 50.0)

        # Call on the stretchy ik function from utils
        ikNodes = utils.RP_2segment_stretchy_IK(ikJoints[0], ikJoints[1], ikJoints[2], self.containerName)
        locators = (ikNodes[0], ikNodes[1], ikNodes[2])
        distanceNodes = ikNodes[3]
        
        # Point constraint stretch locators to transform control objects
        constraints = []
        for i in range(3):
            constraints.append(cmds.pointConstraint(self.getTranslationControl(joints[i]), locators[i], maintainOffset=False)[0])
            cmds.parent(locators[i], self.moduleNamespace+":module_grp", absolute=True)
            cmds.setAttr(locators[i]+".visibility", 0)
            
        utils.addNodeToContainer(self.containerName, constraints)
        
        scaleTarget = self.getTranslationControl(joints[1])
        paRepresentation = self.createPreferredAngleRepresentation(ikJoints[1], scaleTarget)
        
        cmds.setAttr(paRepresentation+".axis", lock=True)
        
        
    def UI_custom(self):
        joints = self.getJoints()
        print joints
        self.createRotationOrderUIControl(joints[0])
        self.createRotationOrderUIControl(joints[1])
        
        
    def lock_phase1(self):
        # GAther and return all required information from this modules control objects.
        # Joint Positions = list of joint positions from the root down the hierarchy
        # Joint orientations = a list of orientations, or a list of axis information  ( orient joint and secondaryAxisOrient from
        #                       # These are passed in the following tuple: ( orientations, None) or ( NOne, axis info)
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
        jointPreferredAngles = []

        # Unlock container and delete ik handle.
        cmds.lockNode(self.containerName, lock=False, lockUnpublished=False)
        ikHandle = self.moduleNamespace+":IK_"+self.jointInfo[0][0]+"_ikHandle"
        cmds.delete(ikHandle)
        
        # Freeze transforms on the joints before lock
        for i in range(3):
            jointName = self.jointInfo[i][0]
            ikJointName = self.moduleNamespace+":IK_"+jointName
            cmds.makeIdentity(ikJointName, rotate=True, translate=False, scale=False, apply=True)

            jointPositions.append(cmds.xform(ikJointName, q=True, ws=True, t=True))
            
            jointRotationOrders.append(cmds.getAttr(self.moduleNamespace+":"+jointName+".rotateOrder"))
            
            if i < 2:
                jointOrientX = cmds.getAttr(ikJointName+".jointOrientX")
                jointOrientY = cmds.getAttr(ikJointName+".jointOrientY")
                jointOrientZ = cmds.getAttr(ikJointName+".jointOrientZ")
                
                jointOrientationValues.append( (jointOrientX, jointOrientY, jointOrientZ) )
                
                joint_paX = cmds.getAttr(ikJointName+".preferredAngleX")
                joint_paY = cmds.getAttr(ikJointName+".preferredAngleY")
                joint_paZ = cmds.getAttr(ikJointName+".preferredAngleZ")
                
                jointPreferredAngles.append( (joint_paX, joint_paY, joint_paZ) )
                
        jointOrientations= (jointOrientationValues, None)
            
        hookObject = self.findHookObjectForLock()
        rootTransform = False
            
        moduleNamespace = self.moduleNamespace
            
        moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform, moduleNamespace)
        return moduleInfo
                
                
            

        
        
        
        


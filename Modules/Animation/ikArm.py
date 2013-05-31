import maya.cmds as cmds
import os
import System.utils as utils
from functools import partial
from math import atan2, degrees

import System.controlModule as controlModule
#reload(controlModule)

import System.controlObject as controlObject
#reload(controlObject)

# ADD
import System.utils as utils
#reload(utils)

import Animation.circleControlStretchyIK as circleIK
#reload(circleIK)

CLASS_NAME = "ArmIK"

TITLE = "Ik Arm"

DESCRIPTION = "This module provides an IK Arm"

class ArmIK(circleIK.CircleControlStretchyIK):
    def __init__(self, moduleNamespace):
        circleIK.CircleControlStretchyIK.__init__(self, moduleNamespace)
        
    def compatibleBlueprintModules(self):
        return ("Hinge_XtraJoint",)
    
    def install_custom(self, joints, moduleGrp, moduleContainer):
        wristJoint = joints[3]
        handJoint = joints[4]
        
        """ The temp locator is used to find the position of each joint """
        tempLocator = cmds.spaceLocator()[0]
        cmds.parent(tempLocator, handJoint, relative=True)
        cmds.parent(tempLocator, moduleGrp, absolute=True)
        
        handJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
        
        cmds.parent(tempLocator, wristJoint)
        for attr in [".translateX", ".translateY", ".translateZ"]:
            cmds.setAttr(tempLocator+attr, 0)
        cmds.parent(tempLocator, moduleGrp, absolute=True)
        
        wristJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
        
        cmds.delete(tempLocator)  
        
        containedNodes = []
        
        """ Pass in functionality from basic IK  """      
        ikNodes = circleIK.CircleControlStretchyIK.install_custom(self, joints, moduleGrp, moduleContainer, createHandleControl=False, poleVectorAtRoot=False)
        ikEndPosLocator = ikNodes["endLocator"]
        ikPoleVectorLocator = ikNodes["poleVectorObject"]
        
        stretchinessAttribute = ikNodes["stretchinessAttribute"]
        
        name = "armControl"
        controlObjectInstance = controlObject.ControlObject()
        handControlInfo = controlObjectInstance.create(name, "handControl.ma", self, lod=1, translation=True, rotation=True, globalScale=False, spaceSwitching=True)
        handControl = handControlInfo[0]
        handControlRootParent = handControlInfo[1]
        
        """ Parent foot control to root parent """
        cmds.parent(handControlRootParent, moduleGrp, relative=True)
        
        """ Position and orient foot control """
        handControlPos = [wristJoint_modulePos[0], handJoint_modulePos[1], wristJoint_modulePos[2]]
        cmds.xform(handControl, objectSpace=True, absolute=True, translation=handControlPos)
        
        cmds.setAttr(handControl+".rotateOrder", 3) #3 = xyz
        
        orientationVector = [handJoint_modulePos[0] - wristJoint_modulePos[0], handJoint_modulePos[2] - wristJoint_modulePos[2] ]
        
        handControlRotation = atan2(orientationVector[1], orientationVector[0])
        cmds.setAttr(handControl+".rotateY", -degrees(handControlRotation))
        
        pointConstraint = cmds.pointConstraint(handControl, ikEndPosLocator, maintainOffset=False, n=ikEndPosLocator+"_pointConstraint")[0]
        containedNodes.append(pointConstraint)
        
        """ Hookup stretchiness attribute """
        cmds.select(handControl)
        cmds.addAttr(at="float", minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True, longName="stretchiness")
        self.publishNameToModuleContainer(handControl+".stretchiness", "stretchiness", publishToOuterContainers=True)
        
        cmds.connectAttr(handControl+".stretchiness", stretchinessAttribute, force=True)
        
        """ Hand IK """
        handIKNodes = cmds.ikHandle(sj=wristJoint, ee=handJoint, solver="ikRPsolver", n=handJoint+"_ikHandle")
        handIKNodes[1] = cmds.rename(handIKNodes[1], handIKNodes[1]+"_ikEffector")
        containedNodes.extend(handIKNodes)
        
        cmds.parent(handIKNodes[0], handControl)
        cmds.setAttr(handIKNodes[0]+".visibility", 0)
        
        utils.addNodeToContainer(moduleContainer, containedNodes, ihb=True)
        
    def UI(self, parentLayout):
        armControl = self.blueprintNamespace+":"+self.moduleNamespace+":armControl"
        
        controlObjectInstance = controlObject.ControlObject(armControl)
        controlObjectInstance.UI(parentLayout)
        
        cmds.attrControlGrp(attribute=armControl+".stretchiness", label="Stretchiness")
        
        circleIK.CircleControlStretchyIK.UI(self, parentLayout)
        
        jointsGrp = self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp"
        joints = utils.findJointChain(jointsGrp)
          
    def match(self, *args):
        """ Identify and unlock the containers """
        characterContainer = self.characterNamespaceOnly + ":character_container"
        blueprintContainer = self.blueprintNamespace + ":module_container"
        moduleContainer = self.blueprintNamespace + ":" + self.moduleNamespace + ":module_container"
        
        containers = [characterContainer, blueprintContainer, moduleContainer]
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
        
        """ Find the IK joint chain """
        ikJoints = utils.findJointChain(self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp")
        blueprintJoints = utils.findJointChain(self.blueprintNamespace+":blueprint_joints_grp")
        
        armControl = self.blueprintNamespace+":"+self.moduleNamespace+":armControl" 
        
        tempChildTransform = cmds.group(empty=True)
        cmds.parent(tempChildTransform, armControl, relative=True)
        cmds.setAttr(tempChildTransform + ".translateZ", 5)
        
        ikHandPos = cmds.xform(ikJoints[4], q=True, worldSpace=True, translation=True)
        armControlPos = cmds.xform(armControl, q=True, worldSpace=True, translation=True)
        
        worldSpacePositionOffset = [ikHandPos[0] - armControlPos[0], ikHandPos[1] - armControlPos[1], ikHandPos[2] - armControlPos[2]]
                                                                      
        cmds.xform(tempChildTransform, worldSpace=True, relative=True, translation=worldSpacePositionOffset)
        
        cmds.parent(tempChildTransform, ikJoints[4], absolute=True) 
        cmds.setAttr(tempChildTransform+".translateX", 0) 
        cmds.setAttr(tempChildTransform+".translateZ", 0) 
        
        cmds.parent(tempChildTransform, blueprintJoints[4], relative=True) 
        cmds.xform(armControl, ws=True, absolute=True, translation=cmds.xform(blueprintJoints[3], q=True, ws=True, translation=True))
        
        aimConstraint = cmds.aimConstraint(blueprintJoints[4], armControl, maintainOffset=False, aimVector=[1.0, 0.0, 0.0], upVector=[0.0, 0.0, 1.0], worldUpType="object", worldUpObject=tempChildTransform) 
        
        cmds.delete(aimConstraint)
        cmds.delete(tempChildTransform) 
        
        blueprint_handJointPos = cmds.xform(blueprintJoints[4], q=True, worldSpace=True, translation=True)
        ikHandPos = cmds.xform(ikJoints[4], q=True, worldSpace=True, translation=True)
        
        worldSpacePositionOffset = [blueprint_handJointPos[0] - ikHandPos[0], blueprint_handJointPos[1] - ikHandPos[1], blueprint_handJointPos[2] - ikHandPos[2]]
        cmds.xform(armControl, worldSpace=True, relative=True, translation=worldSpacePositionOffset)
        
        #self.matchRotationControl(ikJoints[5]+"_ryControl", ikJoints[4], blueprintJoints[4])
        #self.matchRotationControl(ikJoints[5]+"_ryControl", ikJoints[3], blueprintJoints[3])
        
        circleIK.CircleControlStretchyIK.match(self, args)
           
        for c in containers:
            cmds.lockNode(c, lock=True, lockUnpublished=True)

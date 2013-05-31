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

CLASS_NAME = "LegIK_ReverseFoot"

TITLE = "Leg IK with Reverse Foot"

DESCRIPTION = "This module provides an IK Leg with reverse foot controls"

class LegIK_ReverseFoot(circleIK.CircleControlStretchyIK):
    def __init__(self, moduleNamespace):
        circleIK.CircleControlStretchyIK.__init__(self, moduleNamespace)
        
    def compatibleBlueprintModules(self):
        return ("LegFoot",)
    
    def install_custom(self, joints, moduleGrp, moduleContainer):
        ankleJoint = joints[3]
        ballJoint = joints[4]
        toeJoint = joints[5]
        
        tempLocator = cmds.spaceLocator()[0]
        cmds.parent(tempLocator, ballJoint, relative=True)
        cmds.parent(tempLocator, moduleGrp, absolute=True)
        
        ballJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
       
        cmds.parent(tempLocator, ankleJoint)
        for attr in [".translateX", ".translateY", ".translateZ"]:
            cmds.setAttr(tempLocator+attr, 0)
        cmds.parent(tempLocator, moduleGrp, absolute=True)
        
        ankleJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
        
        cmds.parent(tempLocator, toeJoint)
        for attr in [".translateX", ".translateY", ".translateZ"]:
            cmds.setAttr(tempLocator+attr, 0)
        cmds.parent(tempLocator, moduleGrp, absolute=True)
        
        toeJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
        
        cmds.delete(tempLocator)  
        
        containedNodes = []

        # Pass in functionality from basic IK        
        ikNodes = circleIK.CircleControlStretchyIK.install_custom(self, joints, moduleGrp, moduleContainer, createHandleControl=False, poleVectorAtRoot=False)
        ikEndPosLocator = ikNodes["endLocator"]
        ikPoleVectorLocator = ikNodes["poleVectorObject"]
        
        stretchinessAttribute = ikNodes["stretchinessAttribute"]
        
        name = "footControl"
        controlObjectInstance = controlObject.ControlObject()
        footControlInfo = controlObjectInstance.create(name, "footControl.ma", self, lod=1, translation=True, rotation=True, globalScale=False, spaceSwitching=True)
        footControl = footControlInfo[0]
        footControlRootParent = footControlInfo[1]
        
        # Parent foot control to root parent
        cmds.parent(footControlRootParent, moduleGrp, relative=True)
        
        # Position and orient foot control
        footControlPos = [ankleJoint_modulePos[0], ballJoint_modulePos[1], ankleJoint_modulePos[2]]
        cmds.xform(footControl, objectSpace=True, absolute=True, translation=footControlPos)
        
        cmds.setAttr(footControl+".rotateOrder", 3) #3 = xyz
        
        orientationVector = [toeJoint_modulePos[0] - ankleJoint_modulePos[0], toeJoint_modulePos[2] - ankleJoint_modulePos[2] ]
        
        footControlRotation = atan2(orientationVector[1], orientationVector[0])
        cmds.setAttr(footControl+".rotateY", -degrees(footControlRotation))
        
        # Hookup stretchiness attribute
        cmds.select(footControl)
        cmds.addAttr(at="float", minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True, longName="stretchiness")
        self.publishNameToModuleContainer(footControl+".stretchiness", "stretchiness", publishToOuterContainers=True)
        
        cmds.connectAttr(footControl+".stretchiness", stretchinessAttribute, force=True)
        
        # Setup for ball and Toe controls
        ballToeControls = []
        ballToeControl_orientGrps = []
        for joint in [ballJoint, toeJoint]:
            controlObjectInstance = controlObject.ControlObject()
            jointName = utils.stripAllNamespaces(joint)[1]
            name = jointName + "_ryControl"
            
            ryControlInfo = controlObjectInstance.create(name, "yAxisCircle.ma", self, lod=2, translation=False, rotation=[True, True, True], globalScale=False, spaceSwitching=False)
            ryControl = ryControlInfo[0]
            
            ballToeControls.append(ryControl)
            
            orientGrp = cmds.group(empty=True, n=ryControl+"_orientGrp")
            containedNodes.append(orientGrp)
            ballToeControl_orientGrps.append(orientGrp)
            
            # Constrain to inherit orientations
            orientGrp_parentConstraint = cmds.parentConstraint(joint, orientGrp, maintainOffset=False)
            cmds.delete(orientGrp_parentConstraint)
            
            cmds.parent(ryControl, orientGrp, relative=True)
            
        for grp in ballToeControl_orientGrps:
            cmds.parent(grp, moduleGrp, absolute=True)
        # Constrain ball control    
        containedNodes.append(cmds.parentConstraint(footControl, ballToeControl_orientGrps[1], maintainOffset=True, n=ballToeControl_orientGrps[1] + "_parentConstraint")[0])
        # Constrain toe control 
        containedNodes.append(cmds.parentConstraint(ballToeControls[1], ballToeControl_orientGrps[0], maintainOffset=True, n=ballToeControl_orientGrps[0] + "_parentConstraint")[0])
        # Connect IK handles
        cmds.parent(ikEndPosLocator, ballToeControls[0], absolute=True)
        cmds.parent(ikPoleVectorLocator, ballToeControls[0], absolute=True)
       
        # Ankle IK
        ankleIKNodes = cmds.ikHandle(sj=ankleJoint, ee=ballJoint, solver="ikSCsolver", n=ankleJoint+"_ikHandle")
        ankleIKNodes[1] = cmds.rename(ankleIKNodes[1], ankleIKNodes[1]+"_ikEffector")
        containedNodes.extend(ankleIKNodes)
        
        cmds.parent(ankleIKNodes[0], ballToeControls[0])
        cmds.setAttr(ankleIKNodes[0]+".visibility", 0)
        
        #Ball IK 
        ballIKNodes = cmds.ikHandle(sj=ballJoint, ee=toeJoint, solver="ikSCsolver", n=ballJoint+"_ikHandle")
        ballIKNodes[1] = cmds.rename(ballIKNodes[1], ballIKNodes[1]+"_ikEffector")
        containedNodes.extend(ballIKNodes)
        
        cmds.parent(ballIKNodes[0], ballToeControls[1])
        cmds.setAttr(ballIKNodes[0]+".visibility", 0)
        
        utils.addNodeToContainer(moduleContainer, containedNodes, ihb=True)
        
        
    def UI(self, parentLayout):
        footControl = self.blueprintNamespace+":"+self.moduleNamespace+":footControl"
        
        controlObjectInstance = controlObject.ControlObject(footControl)
        controlObjectInstance.UI(parentLayout)
        
        cmds.attrControlGrp(attribute=footControl+".stretchiness", label="Stretchiness")
        
        circleIK.CircleControlStretchyIK.UI(self, parentLayout)
        
        jointsGrp = self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp"
        joints = utils.findJointChain(jointsGrp)
        
        ballJoint = joints[4]
        toeJoint = joints[5]
        
        for joint in [ballJoint, toeJoint]:
            jointControl = joint+"_ryControl"
            controlObjectInstance = controlObject.ControlObject(jointControl)
            controlObjectInstance.UI(parentLayout)
            
            
    def match(self, *args):
        characterContainer = self.characterNamespaceOnly + ":character_container"
        blueprintContainer = self.blueprintNamespace + ":module_container"
        moduleContainer = self.blueprintNamespace + ":" + self.moduleNamespace + ":module_container"
        
        containers = [characterContainer, blueprintContainer, moduleContainer]
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
        
        ikJoints = utils.findJointChain(self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp")
        blueprintJoints = utils.findJointChain(self.blueprintNamespace+":blueprint_joints_grp")
        
        footControl = self.blueprintNamespace+":"+self.moduleNamespace+":footControl" 
        
        tempChildTransform = cmds.group(empty=True)
        cmds.parent(tempChildTransform, footControl, relative=True)
        cmds.setAttr(tempChildTransform + ".translateZ", 5)
        
        ikToePos = cmds.xform(ikJoints[5], q=True, worldSpace=True, translation=True)
        footControlPos = cmds.xform(footControl, q=True, worldSpace=True, translation=True)
        
        worldSpacePositionOffset = [ikToePos[0] - footControlPos[0], ikToePos[1] - footControlPos[1], ikToePos[2] - footControlPos[2]]
                                                                      
        cmds.xform(tempChildTransform, worldSpace=True, relative=True, translation=worldSpacePositionOffset)
        
        cmds.parent(tempChildTransform, ikJoints[5], absolute=True) 
        cmds.setAttr(tempChildTransform+".translateX", 0) 
        cmds.setAttr(tempChildTransform+".translateZ", 0) 
        
        cmds.parent(tempChildTransform, blueprintJoints[5], relative=True) 
        cmds.xform(footControl, ws=True, absolute=True, translation=cmds.xform(blueprintJoints[4], q=True, ws=True, translation=True))
        
        aimConstraint = cmds.aimConstraint(blueprintJoints[5], footControl, maintainOffset=False, aimVector=[1.0, 0.0, 0.0], upVector=[0.0, 0.0, 1.0], worldUpType="object", worldUpObject=tempChildTransform) 
        
        cmds.delete(aimConstraint)
        cmds.delete(tempChildTransform) 
        
        blueprint_toeJointPos = cmds.xform(blueprintJoints[5], q=True, worldSpace=True, translation=True)
        ikToePos = cmds.xform(ikJoints[5], q=True, worldSpace=True, translation=True)
        
        worldSpacePositionOffset = [blueprint_toeJointPos[0] - ikToePos[0], blueprint_toeJointPos[1] - ikToePos[1], blueprint_toeJointPos[2] - ikToePos[2]]
        cmds.xform(footControl, worldSpace=True, relative=True, translation=worldSpacePositionOffset)
        
        self.matchRotationControl(ikJoints[5]+"_ryControl", ikJoints[4], blueprintJoints[4])
        self.matchRotationControl(ikJoints[5]+"_ryControl", ikJoints[3], blueprintJoints[3])
        
        circleIK.CircleControlStretchyIK.match(self, args)
           
        for c in containers:
            cmds.lockNode(c, lock=True, lockUnpublished=True)
            
    def matchRotationControl(self, rotationControl, drivenJoint, targetJoint):
        controlPos = cmds.xform(rotationControl, q=True, worldSpace=True, translation=True)
        drivenJointPos = cmds.xform(drivenJoint, q=True, worldSpace=True, translation=True)
        targetJointPos = cmds.xform(targetJoint, q=True, worldSpace=True, translation=True)
        
        currentVector = [drivenJointPos[0] - controlPos[0], drivenJointPos[1] - controlPos[1], drivenJointPos[2] - controlPos[2]]
        targetVector = [targetJointPos[0] - controlPos[0], targetJointPos[1] - controlPos[1], targetJointPos[2] - controlPos[2]] 
        
        targetVector = utils.normaliseVector(targetVector)
        currentVector = utils.normaliseVector(currentVector)  
        
        offsetAngle = utils.calculateAngleBetweenNormalisedVectors  (targetVector, currentVector)
        
        cmds.setAttr(rotationControl+".rotateY", cmds.getAttr(rotationControl+".rotateY") + offsetAngle)
        
        drivenJointPos = cmds.xform(drivenJoint, q=True, worldSpace=True, translation=True)
        currentVector = [drivenJointPos[0] - controlPos[0], drivenJointPos[1] - controlPos[1], drivenJointPos[2] - controlPos[2]]
        currentVector = utils.normaliseVector(currentVector)
        
        newAngle = utils.calculateAngleBetweenNormalisedVectors  (targetVector, currentVector)
        
        if newAngle > 0.1:
            offsetAngle *= -2
            cmds.setAttr(rotationControl+".rotateY", cmds.getAttr(rotationControl+".rotateY") + offsetAngle)
  
import maya.cmds as cmds
import os
import System.utils as utils
from functools import partial

import System.controlModule as controlModule
#reload(controlModule)

import System.controlObject as controlObject
#reload(controlObject)

CLASS_NAME = "BasicStretchyIK"

TITLE = "Basic Stretchy IK"

DESCRIPTION = "This module provides stretchy IK on the joint chain, with the ability to lock stretchiness with a 0-1 slider value.  Note: the Ik handle is not space-switchable, and for that reason, has frozen transformations at it's creation position."
class BasicStretchyIK(controlModule.ControlModule):
    def __init__(self, moduleNamespace):
        controlModule.ControlModule.__init__(self, moduleNamespace)
        
           
    def compatibleBlueprintModules(self):
        return ("Finger", "HingeJoint", "SingleJointSegment", "Arm", "Wing", "Head", "ClavicleJoint",)
    
       
    def install_custom(self, joints, moduleGrp, moduleContainer):
        containedNodes = []
        rootJoint = joints[1]
        endJoint = joints[len(joints)-1]
        
        ikNodes = utils.basic_stretchy_IK(rootJoint, endJoint, container=moduleContainer, scaleCorrectionAttribute=self.blueprintNamespace+":module_grp.hierarchicalScale")
        ikHandle = ikNodes["ikHandle"]
        rootLocator = ikNodes["rootLocator"]
        endLocator = ikNodes["endLocator"]
        poleVectorLocator = ikNodes["poleVectorObject"]
        stretchinessAttribute = ikNodes["stretchinessAttribute"]
        
        # Create controls and parent ikHandles
        for node in [rootLocator, ikHandle, poleVectorLocator]:
            cmds.parent(node, moduleGrp, absolute=True)
            
        name = "ikHandleControl"
        # controlObject class
        controlObjectInstance = controlObject.ControlObject()
        handleControlInfo = controlObjectInstance.create(name, "cubeLocator.ma", self, lod=1, translation=True, rotation=False, globalScale=False, spaceSwitching=True)
        handleControl = handleControlInfo[0]
        handleRootParent = handleControlInfo[1]
        
        cmds.parent(handleRootParent, moduleGrp, relative=True)
        
        cmds.xform(handleControl, worldSpace=True, absolute=True, translation=cmds.xform(endLocator, q=True, worldSpace=True, translation=True))
        
        cmds.parent(endLocator, handleControl, absolute=True)
        
        # Create a pre-transform node that sits above the control object.
        handleControlParent = cmds.listRelatives(handleControl, parent=True)[0]
        preTransform = cmds.group(empty=True, n=handleControl+"_preTransform")
        containedNodes.append(preTransform)
        
        cmds.parent(preTransform, handleControl, relative=True)
        cmds.parent(preTransform, handleControlParent, absolute=True)
        cmds.parent(handleControl, preTransform, absolute=True)
        
        #Add attributes to control
        cmds.select(handleControl)
        cmds.addAttr(at="float", minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True, longName="stretchiness")
        cmds.addAttr(at="float", softMinValue=-360.0, softMaxValue=360.0, defaultValue=0.0, keyable=True, longName="twist")
        
        #connect attrs
        cmds.connectAttr(handleControl+".twist", ikHandle+".twist")
        cmds.connectAttr(handleControl+".stretchiness", stretchinessAttribute)
        
        # Add attrs to container
        self.publishNameToModuleContainer(handleControl+".twist", "twist", publishToOuterContainers=True)
        self.publishNameToModuleContainer(handleControl+".stretchiness", "stretchiness", publishToOuterContainers=True)
        
        # 171 >
        jointName = utils.stripAllNamespaces(rootJoint)[1]
        ikJoints = utils.findJointChain(rootJoint)
        targetJoints = utils.findJointChain(self.blueprintNamespace+":creationPose_"+jointName)
        
        utils.matchTwistAngle(handleControl+".twist", ikJoints, targetJoints)
        
        offsetNode = cmds.shadingNode("plusMinusAverage", asUtility=True, n=handleControl+"_twistOffset")
        containedNodes.append(offsetNode)
        
        cmds.setAttr(offsetNode+".input1D[0]", cmds.getAttr(handleControl+".twist"))
        cmds.connectAttr(handleControl+".twist", offsetNode+".input1D[1]")
        cmds.connectAttr(offsetNode+".output1D", ikHandle+".twist", force=True)
        
        cmds.setAttr(handleControl+".twist", 0.0)
        # < 171
        utils.addNodeToContainer(moduleContainer, containedNodes)
        
    def UI(self, parentLayout):
        ikHandleControl = self.blueprintNamespace+":"+self.moduleNamespace+":ikHandleControl"
        controlObjectInstance = controlObject.ControlObject(ikHandleControl)
        controlObjectInstance.UI(parentLayout)
        
        cmds.attrControlGrp(attribute=ikHandleControl+".twist", label="Twist")
        cmds.attrControlGrp(attribute=ikHandleControl+".stretchiness", label="Stretchiness")
        
    def match(self, *args):
        # Unlock all the containers
        characterContainer = self.characterNamespaceOnly + ":character_container"
        blueprintContainer = self.blueprintNamespace + ":module_container"
        moduleContainer = self.blueprintNamespace + ":" + self.moduleNamespace +":module_container"
        
        containers = [characterContainer, blueprintContainer, moduleContainer]
        
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
            
        joints = utils.findJointChain(self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp")
        blueprintJoints = utils.findJointChain(self.blueprintNamespace+":blueprint_joints_grp")
        
        ikHandleControl = self.blueprintNamespace + ":" + self.moduleNamespace + ":ikHandleControl"
        
        cmds.setAttr(ikHandleControl+".stretchiness", 1)
        
        endPos = cmds.xform(blueprintJoints[ len(blueprintJoints)-1], q=True, ws=True, t=True)
        cmds.xform(ikHandleControl, ws=True, a=True, t=endPos)
        
        joints.pop(0)
        blueprintJoints.pop(0)
        
        utils.matchTwistAngle(ikHandleControl+".twist", joints, blueprintJoints)
            
            
        for c in containers:
            cmds.lockNode(c, lock=True, lockUnpublished=True)
        
        
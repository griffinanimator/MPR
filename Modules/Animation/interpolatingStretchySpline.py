import maya.cmds as cmds
import os
import System.utils as utils
from functools import partial

import System.controlModule as controlModule
#reload(controlModule)

import System.controlObject as controlObject
#reload(controlObject)

CLASS_NAME = "InterpolatingStretchySpline"

TITLE = "Interpolation-based Stretchy Spline"

DESCRIPTION = "This module provides root and end controls for translation and rotation (root control is optional), with fine tuning interpolation controls for specific spline shapes."

class InterpolatingStretchySpline(controlModule.ControlModule):
    def __init__(self, moduleNamespace):
        controlModule.ControlModule.__init__(self, moduleNamespace)
    
                
    def compatibleBlueprintModules(self):
        return ("Spline", "Spine",)
    
    def install_requirements(self):
        blueprintJointsGrp = self.blueprintNamespace + ":blueprint_joints_grp"
        blueprintJoints = utils.findJointChain(blueprintJointsGrp)
        
        if len(blueprintJoints) >= 6:
            return True
        else:
            cmds.confirmDialog(title="Interpolation-based Stretchy Spline", message="This control module can only be installed on spline blueprints with 5 joints or more", button=["Accept"], defaultButton="Accept")
            return False
    
       
    def install_custom(self, joints, moduleGrp, moduleContainer):
        result = cmds.confirmDialog(title="Interpolation-based Stretchy Spline", message="please specify the root control type:", button=["Translation and Rotation", "Rotation Only", "None"], defaultButton="Translation and Rotation", cancelButton="None", dismissString="None")
        
        rootControlTranslation = (result == "Translation and Rotation")
        createRootControl = not (result == "None")
        
        containedNodes = []
        
        creationPoseJoints = []
        for joint in joints:
            jointName = utils.stripAllNamespaces(joint)[1]
            creationPoseJoint = self.blueprintNamespace+":creationPose_"+jointName
            creationPoseJoints.append(creationPoseJoint)

        # Create root and end controls   
        rootControlObject = moduleGrp
        if createRootControl:
            rootControlObjectInfo = self.createRootEndControl("rootControl", creationPoseJoints[1], creationPoseJoints[1], rootControlTranslation, containedNodes, moduleGrp)
            
            #"Return Tuple.  [0] is object, [1] parent"
            rootControlObject = rootControlObjectInfo[0]
            rootControlParent = rootControlObjectInfo[1]
            
            if not rootControlTranslation:
                containedNodes.append(cmds.pointConstraint(moduleGrp, rootControlParent, maintainOffset=True)[0])
        # Orient end joint based off second to last joint
        endControlObjectInfo = self.createRootEndControl("endControl", creationPoseJoints[len(creationPoseJoints)-2], creationPoseJoints[len(creationPoseJoints)-1], True, containedNodes, moduleGrp)
        endControlObject = endControlObjectInfo[0]
        
        # Setup splineIK
        # Duplicate stretchyIKJoints and rename
        stretchyIKJoints = cmds.duplicate(joints, renameChildren=True)
        index = 0
        for joint in stretchyIKJoints:
            stretchyIKJoints[index] = cmds.rename(joint, joints[index]+"_stretchyIKJoint")
            index +=1
            
        containedNodes.extend(stretchyIKJoints)
        
        # Get the ws position of the root and end joints
        rootJoint = stretchyIKJoints[1]
        endJoint = stretchyIKJoints[len(stretchyIKJoints)-1]
        secondJoint = stretchyIKJoints[2]
        secondToLastJoint = stretchyIKJoints[len(stretchyIKJoints)-2]
        
        
        rootPos = cmds.xform(rootJoint, q=True, ws=True, translation=True)
        endPos = cmds.xform(endJoint, q=True, ws=True, translation=True)
        
        rootLocator = cmds.spaceLocator(n=stretchyIKJoints[0]+"_systemStretch_rootLocator")[0]
        cmds.xform(rootLocator, ws=True, absolute=True, translation=rootPos)
        #containedNodes.append(rootLocator)
        
        endLocator = cmds.spaceLocator(n=stretchyIKJoints[0]+"_systemStretch_endLocator")[0]
        cmds.xform(endLocator, ws=True, absolute=True, translation=endPos)
        #containedNodes.append(endLocator)
        
        # Hide locators
        for loc in [rootLocator, endLocator]:
            cmds.setAttr(loc+".visibility", 0)
        
        #parent locators to controls    
        cmds.parent(rootLocator, rootControlObject, absolute=True)
        cmds.parent(endLocator, endControlObject, absolute=True)
        
        index = 0
        for joint in stretchyIKJoints:
            if index > 2 and index < len(stretchyIKJoints)-1:
                cmds.select(stretchyIKJoints[index], replace=True)
                cmds.addAttr(at="float", longName="originalLength")
                originalLength = cmds.getAttr(stretchyIKJoints[index]+".translateX")
                cmds.setAttr(stretchyIKJoints[index]+".originalLength", originalLength)
                
            index += 1
        
        # Setup the scale factor   
        scaleFactorAttr = self.createDistanceCalculations(rootLocator, endLocator, containedNodes)
        
        rootScaler = self.createScalar(rootLocator, scaleFactorAttr, containedNodes)
        endScaler = self.createScalar(endLocator, scaleFactorAttr, containedNodes)
        
        rootIKLocators = self.setupBasicStretchyIK(rootJoint, secondJoint, creationPoseJoints[1], rootControlObject, moduleContainer, moduleGrp)
        rootIK_rootLocator = rootIKLocators[0]
        rootIK_endLocator = rootIKLocators[1]
        
        cmds.parent(rootIK_endLocator, rootScaler, absolute=True)
        
        endIKLocators = self.setupBasicStretchyIK(secondToLastJoint, endJoint, creationPoseJoints[len(creationPoseJoints)-2], endControlObject, moduleContainer, moduleGrp)
        endIK_rootLocator = endIKLocators[0]
        endIK_endLocator = endIKLocators[1]
        
        cmds.parent(endIK_endLocator, endControlObject, absolute=True)
                       
        ikNodes = cmds.ikHandle(sj=secondJoint, ee=secondToLastJoint, n=secondJoint+"_splineIKHandle", sol="ikSplineSolver", rootOnCurve=False, createCurve=True )
        
        ikNodes[1] = cmds.rename(ikNodes[1], secondJoint+"_splineIKEffector")
        ikNodes[2] = cmds.rename(ikNodes[2], secondJoint+"_splineIKCurve")
        
        splineIKhandle = ikNodes[0]       
        splineIKCurve = ikNodes[2] 
               
        containedNodes.extend(ikNodes)
        
        cmds.parent(splineIKhandle, moduleGrp, absolute=True)
        cmds.setAttr(splineIKhandle+".visibility", 0)
        cmds.setAttr(splineIKCurve+".visibility", 0)
        
        cmds.parent(splineIKCurve, world=True, absolute=True)
        cmds.setAttr(splineIKCurve+".inheritsTransform", 0)
        cmds.parent(splineIKCurve, moduleGrp, relative=True)
        
        # Create a cluster for the CV's on the curve.
        cmds.select(splineIKCurve+".cv[0:1]", replace=True)
        clusterNodes = cmds.cluster(n=splineIKCurve+"_rootCluster")
        cmds.container(moduleContainer, edit=True, addNode=clusterNodes, ihb=True, includeNetwork=True)
        rootClusterHandle = clusterNodes[1]
        
        cmds.select(splineIKCurve+".cv[2:3]", replace=True)
        clusterNodes = cmds.cluster(n=splineIKCurve+"_endCluster")
        cmds.container(moduleContainer, edit=True, addNode=clusterNodes, ihb=True, includeNetwork=True)
        endClusterHandle = clusterNodes[1]
        
        for handle in [rootClusterHandle, endClusterHandle]:
            cmds.setAttr(handle+".visibility", 0)
        
        cmds.parent(rootClusterHandle, rootScaler, absolute=True)
        cmds.parent(endClusterHandle, endScaler, absolute=True)
        
        containedNodes.append(cmds.parentConstraint(rootControlObject, rootJoint, maintainOffset=True)[0])
        
        targetLocatorNodes = cmds.duplicate(endIK_rootLocator, name=endIK_rootLocator+"_duplicateTarget")
        targetLocator = targetLocatorNodes[0]
        cmds.delete(targetLocatorNodes[1])
        cmds.parent(targetLocator, endScaler, absolute=True)
        
        splineScaleFactorAttr = self.createDistanceCalculations(rootIK_endLocator, targetLocator, containedNodes)
        
        # Use scaleFactor on each of the joints
        index = 0
        for joint in stretchyIKJoints:
            if index > 2 and index < len(stretchyIKJoints)-1:
                multNode = cmds.shadingNode("multiplyDivide", asUtility=True, n=joint+"_jointScale")
                containedNodes.append(multNode)
                cmds.connectAttr(scaleFactorAttr, multNode+".input1X")
                cmds.setAttr(multNode+".input2X", cmds.getAttr(joint+".originalLength"))
                
                cmds.connectAttr(multNode+".outputX", joint+".translateX")           
            index += 1
            
        cmds.setAttr(splineIKhandle+".dTwistControlEnable", 1)
        cmds.setAttr(splineIKhandle + ".dWorldUpType", 4)
        cmds.setAttr(splineIKhandle + ".dWorldUpAxis", 5)
        
        cmds.setAttr(splineIKhandle + ".dWorldUpVector", 0.0, 0.0, 1.0, type="double3")
        cmds.setAttr(splineIKhandle + ".dWorldUpVectorEnd", 0.0, 0.0, 1.0, type="double3")
        
        if createRootControl:
            cmds.connectAttr(rootControlObject+".worldMatrix[0]", splineIKhandle+".dWorldUpMatrix")
        else:
            dummyNode = cmds.duplicate(rootJoint, parentOnly=True, n=rootJoint+"_dummyDuplicate")[0]
            containedNodes.append(dummyNode)
            cmds.parent(dummyNode, moduleGrp, absolute=True)
            cmds.connectAttr(dummyNode+".worldMatrix[0]", splineIKhandle+".dWorldUpMatrix")
            
        cmds.connectAttr(endControlObject+".worldMatrix[0]", splineIKhandle+".dWorldUpMatrixEnd")
        # Create 2 attributes for "offsetY and offsetZ".
        cmds.select(moduleGrp)
        cmds.addAttr(at="float", defaultValue=0.0, softMinValue=-10.0, softMaxValue=10.0, keyable=True, longName="offsetY")
        cmds.addAttr(at="float", defaultValue=0.0, softMinValue=-10.0, softMaxValue=10.0, keyable=True, longName="offsetZ")
        # Publish new attrs to container
        self.publishNameToModuleContainer(moduleGrp+".offsetY", "interpolator_offsetY", publishToOuterContainers=True)
        self.publishNameToModuleContainer(moduleGrp+".offsetZ", "interpolator_offsetZ", publishToOuterContainers=True)
        # Create a node to inverse offset
        inverseNode = cmds.shadingNode("multiplyDivide", asUtility=True, n=moduleGrp+"_offsetInverse")
        containedNodes.append(inverseNode)
        
        cmds.connectAttr(moduleGrp+".offsetY", inverseNode+".input1Y")
        cmds.connectAttr(moduleGrp+".offsetZ", inverseNode+".input1Z")
        cmds.setAttr(inverseNode+".input2Y", -1)
        cmds.setAttr(inverseNode+".input2Z", -1)
        # Setup interpolators
        numStretchyIKJoints = len(stretchyIKJoints)-1
        
        interpolators_ikParents = []
        aimChildren = []
        
        for i in range(1, numStretchyIKJoints):
            if i > 1:
                # Create a group to follow each joint
                jointFollower = cmds.group(empty=True, n=stretchyIKJoints[i]+"_follower")
                containedNodes.append(jointFollower)
                # Parent the group to the joint we are following
                cmds.parent(jointFollower, moduleGrp, relative=True)
                containedNodes.append(cmds.parentConstraint(stretchyIKJoints[i], jointFollower, maintainOffset=False, n=jointFollower+"_parentConstraint")[0])
                
                offset = cmds.group(empty=True, n=stretchyIKJoints[i]+"_interpolatorOffset")
                containedNodes.append(offset)
                # parent the offset group to the follower group
                cmds.parent(offset, jointFollower, relative=True)
                
                cmds.connectAttr(moduleGrp+".offsetY", offset+".translateY")
                cmds.connectAttr(moduleGrp+".offsetZ", offset+".translateZ")
                
                name = utils.stripAllNamespaces(joints[i])[1] + "_offsetControl"
                controlObjectInstance = controlObject.ControlObject()
                offsetControlObject = controlObjectInstance.create(name, "cubeLocator.ma", self, lod=2, translation=True, rotation=False, globalScale=False, spaceSwitching=False)[0]
                # parent control object under offset group
                cmds.parent(offsetControlObject, offset, relative=True)
                
                offsetCancelation = cmds.group(empty=True, n=stretchyIKJoints[i]+"interpolatorOffsetCancelation")
                containedNodes.append(offsetCancelation)
                cmds.parent(offsetCancelation, offsetControlObject, relative=True)
                
                cmds.connectAttr(inverseNode+".outputY", offsetCancelation+".translateY")
                cmds.connectAttr(inverseNode+".outputZ", offsetCancelation+".translateZ")
                
                interpolators_ikParents.append(offsetCancelation)
                
            aimChild = cmds.group(empty=True, n=stretchyIKJoints[i]+"_aimChild")
            containedNodes.append(aimChild)
            aimChildren.append(aimChild)
            
            if i > 1:
                cmds.parent(aimChild, offsetCancelation, relative=True)
                print "parent offset cancel"
            else:
                cmds.parent(aimChild, stretchyIKJoints[i], relative=True)
                
            cmds.setAttr(aimChild+".translateY", -1)
        # Make use of interpolation nodes    
        for i in range(1, numStretchyIKJoints):
            ikNodes = utils.basic_stretchy_IK(joints[i], joints[i+1], container=moduleContainer, scaleCorrectionAttribute=self.blueprintNamespace+":module_grp.hierarchicalScale", lockMinimumLength=False, poleVectorObject=aimChildren[i-1])
            ikHandle = ikNodes["ikHandle"]
            rootLocator = ikNodes["rootLocator"]
            endLocator = ikNodes["endLocator"]
            
            for loc in (ikHandle, rootLocator):
                cmds.parent(loc, moduleGrp, absolute=True)
                
            utils.matchTwistAngle(ikHandle+".twist", [joints[i],], [stretchyIKJoints[i],])
            
            if i == 1:
                if createRootControl:
                    containedNodes.append(cmds.pointConstraint(rootControlObject, joints[i], maintainOffset=False, n=joints[i]+"_pointConstraint")[0])
                    
            cmds.setAttr(endLocator+".translate", 0.0, 0.0, 0.0, type="double3")
            if i < numStretchyIKJoints-1:
                cmds.parent(endLocator, interpolators_ikParents[i-1], relative=True)
            else:
                cmds.parent(endLocator, endControlObject, relative=True)
                
        cmds.setAttr(moduleGrp+".lod", 2)
                                      
        utils.addNodeToContainer(moduleContainer, containedNodes, ihb=True)
        # Publish joints to module container.
        for joint in stretchyIKJoints:
            jointName = utils.stripAllNamespaces(joint)[1]
            self.publishNameToModuleContainer(joint+".rotate", jointName+"_R", publishToOuterContainers=False)
            self.publishNameToModuleContainer(joint+".translate", jointName+"_T", publishToOuterContainers=False)
    
    def setupBasicStretchyIK(self, sJoint, eJoint, creationPose_sJoint, controlObject, moduleContainer, moduleGrp):
        ikNodes = utils.basic_stretchy_IK(sJoint, eJoint, container=moduleContainer, scaleCorrectionAttribute=self.blueprintNamespace+":module_grp.hierarchicalScale", lockMinimumLength=False)
        ikHandle = ikNodes["ikHandle"]
        rootLocator = ikNodes["rootLocator"]
        endLocator = ikNodes["endLocator"]
        poleVectorLocator = ikNodes["poleVectorObject"]
        
        for loc in [rootLocator, ikHandle]:
            cmds.parent(loc, moduleGrp, absolute=True)
            
        cmds.parent(poleVectorLocator, creationPose_sJoint)
        cmds.setAttr(poleVectorLocator+".translateX", 0)
        cmds.setAttr(poleVectorLocator+".translateY", 10)
        cmds.setAttr(poleVectorLocator+".translateZ", 0)
        
        utils.matchTwistAngle(ikHandle+".twist", [sJoint,], [creationPose_sJoint,])
        
        cmds.parent(poleVectorLocator, controlObject, absolute=True)
        
        return (rootLocator, endLocator)
        
            
    def createScalar(self, parentLocator, scaleFactorAttr, containedNodes):
        scaler = cmds.group(empty=True, n=parentLocator+"_scaler")
        containedNodes.append(scaler)
        cmds.parent(scaler, parentLocator, relative=True)
        
        for attr in [".scaleX", ".scaleY", ".scaleZ"]:
            cmds.connectAttr(scaleFactorAttr, scaler+attr)
            
        return scaler
        
     
    def createDistanceCalculations(self, rootLocator, endLocator, containedNodes):
        rootLocatorName = utils.stripAllNamespaces(rootLocator)[1]
        endLocatorName = utils.stripAllNamespaces(endLocator)[1]
        distNode = cmds.shadingNode("distanceBetween", asUtility=True, n=self.blueprintNamespace+":"+self.moduleNamespace+":distanceBetween_" + rootLocatorName + "__" + endLocatorName)
        containedNodes.append(distNode)
        
        rootLocShape = rootLocator+"Shape"
        endLocShape = endLocator+"Shape"
        
        cmds.connectAttr(rootLocShape+".worldPosition[0]", distNode+".point1")
        cmds.connectAttr(endLocShape+".worldPosition[0]", distNode+".point2")
        
        totalOriginalLength = cmds.getAttr(distNode+".distance")
        totalOriginalLength /= cmds.getAttr(self.blueprintNamespace+":module_grp.hierarchicalScale")
        
        scaleFactor = cmds.shadingNode("multiplyDivide", asUtility=True, n=distNode+"_scaleFactor")
        containedNodes.append(scaleFactor)
        
        cmds.setAttr(scaleFactor+".operation", 2) # Divide
        cmds.connectAttr(distNode+".distance", scaleFactor+".input1X")
        cmds.setAttr(scaleFactor+".input2X", totalOriginalLength)
        
        scaleCorrection = cmds.shadingNode("multiplyDivide", asUtility=True, n=scaleFactor+"_correction")
        containedNodes.append(scaleCorrection)
        
        cmds.setAttr(scaleCorrection+".operation", 2) #Divide
        cmds.connectAttr(scaleFactor+".outputX", scaleCorrection+".input1X")
        cmds.connectAttr(self.blueprintNamespace+":module_grp.hierarchicalScale", scaleCorrection+".input2X")
        
        return scaleCorrection+".outputX"
    
        
        
           
    def createRootEndControl(self, name, orientJoint, posJoint, translation, containedNodes, moduleGrp):
        # Create control object
        controlObjectInstance = controlObject.ControlObject()
        controlObjectInfo = controlObjectInstance.create(name, "flattenedCube.ma", self, lod=1, translation=translation, rotation=True, globalScale=False, spaceSwitching=True)

        controlObj = controlObjectInfo[0]
        controlParent = controlObjectInfo[1]
        # Create a pre-transform to orient the control
        preTransform = cmds.group(empty=True, n=controlObj+"_preTransform")
        containedNodes.append(preTransform)
        
        cmds.parent(controlObj, preTransform, relative=True)
        cmds.parent(preTransform, controlParent, relative=True)
        
        # Get the true worldSpace orientation of the joint
        tempOrientationLocator = cmds.spaceLocator()[0]
        tempOrientConstraint = cmds.orientConstraint(orientJoint, tempOrientationLocator, maintainOffset=False)[0]
        
        targetOrientation = cmds.xform(tempOrientationLocator, q=True, worldSpace=True, rotation=True)
        
        cmds.delete(tempOrientConstraint)
        cmds.delete(tempOrientationLocator)
        
        cmds.xform(preTransform, worldSpace=True, absolute=True, rotation=targetOrientation)
        
        cmds.parent(controlParent, moduleGrp, relative=True)
        cmds.setAttr(controlObj+".rotateOrder", cmds.getAttr(orientJoint+".rotateOrder"))
        
        cmds.xform(controlObj, worldSpace=True, absolute=True, translation=cmds.xform(posJoint, q=True, worldSpace=True, translation=True))
        
        return (controlObj, controlParent)
    
    def UI(self, parentLayout):
        rootControl = self.blueprintNamespace + ":" + self.moduleNamespace + ":rootControl"
        if cmds.objExists(rootControl):
            controlObjectInstance = controlObject.ControlObject(rootControl)
            controlObjectInstance.UI(parentLayout)
            
        jointsGrp = self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp"
        joints = utils.findJointChain(jointsGrp)
        
        joints.pop(0)
        joints.pop(0)
        joints.pop()
        
        for joint in joints:
            offsetControl = joint+"_offsetControl"
            controlObjectInstance = controlObject.ControlObject(offsetControl)
            controlObjectInstance.UI(parentLayout)
            
        endControl = self.blueprintNamespace + ":" + self.moduleNamespace + ":endControl"
        controlObjectInstance = controlObject.ControlObject(endControl)
        controlObjectInstance.UI(parentLayout)
        
        
    def UI_preferences(self, parentLayout):
        moduleGrp = self.blueprintNamespace + ":" + self.moduleNamespace + ":module_grp"
        cmds.attrControlGrp(attribute=moduleGrp+".offsetY", label="Offset Y")
        cmds.attrControlGrp(attribute=moduleGrp+".offsetZ", label="Offset Z")
            
        
        
    
    
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

CLASS_NAME = "LegIK_AttrFoot"

TITLE = "Leg IK with Attribute Foot"

DESCRIPTION = "This module provides an IK Leg with attribute foot controls"

class LegIK_AttrFoot(circleIK.CircleControlStretchyIK):
    def __init__(self, moduleNamespace):
        circleIK.CircleControlStretchyIK.__init__(self, moduleNamespace)
        
    def compatibleBlueprintModules(self):
        return ("LegFoot",)
    
    def install_custom(self, joints, moduleGrp, moduleContainer):
        moduleNamespace = self.blueprintNamespace + ":" + self.moduleNamespace
        
        """ Assign the joint indices to a variable """
        ankleJoint = joints[3]
        ballJoint = joints[4]
        toeJoint = joints[5]
        """ Create a list of objects that need to be added to a namespace """
        namespaceObjects = []
        
        """ Get the module positions by creating a temp locator which is parented to each module in turn.
        Use xform on the locator and save it's position to a new variable.
        """
        
        """ Temp locator used to get the module positions """
        tempLocator = cmds.spaceLocator()[0]
        
        """ Ball Joint """   
        cmds.parent(tempLocator, ballJoint, relative=True)
        cmds.parent(tempLocator, moduleGrp, absolute=True)  
        ballJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
       
        """ Ankle Joint """
        cmds.parent(tempLocator, ankleJoint)
        for attr in [".translateX", ".translateY", ".translateZ"]:
            cmds.setAttr(tempLocator+attr, 0)
        cmds.parent(tempLocator, moduleGrp, absolute=True)
        ankleJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
 
        """ Toe Joint """
        cmds.parent(tempLocator, toeJoint)
        for attr in [".translateX", ".translateY", ".translateZ"]:
            cmds.setAttr(tempLocator+attr, 0)
        cmds.parent(tempLocator, moduleGrp, absolute=True) 
        toeJoint_modulePos = [cmds.getAttr(tempLocator+".translateX"), cmds.getAttr(tempLocator+".translateY"), cmds.getAttr(tempLocator+".translateZ")]
        
        """ Delete the temp locator """
        cmds.delete(tempLocator)  
        
        """ containedNodes is an empty list that will store all the nodes that should be added to the animation module container """
        containedNodes = []

        """ Pass in functionality from basic IK """    
        ikNodes = circleIK.CircleControlStretchyIK.install_custom(self, joints, moduleGrp, moduleContainer, createHandleControl=False, poleVectorAtRoot=False)
        ikEndPosLocator = ikNodes["endLocator"]
        ikPoleVectorLocator = ikNodes["poleVectorObject"]
        #namespaceObjects.append(ikEndPosLocator)
        #namespaceObjects.append(ikPoleVectorLocator)
        
        stretchinessAttribute = ikNodes["stretchinessAttribute"]
        
        """ Import the foot control """
        name = "footControl"
        controlObjectInstance = controlObject.ControlObject()
        footControlInfo = controlObjectInstance.create(name, "footControl.ma", self, lod=1, translation=True, rotation=True, globalScale=False, spaceSwitching=True)
        footControl = footControlInfo[0]
        footControlRootParent = footControlInfo[1]

        """ Create control attributes on the foot control """
        footControlAttributes = ('roll', 'roll_break', 'toe_twist', 'ball_twist', 'heel_twist', 'bank', 'toe_flap')
        cmds.select(footControl)
        for attr in footControlAttributes:
            cmds.addAttr(shortName=attr, defaultValue=0.0, k=True)
            self.publishNameToModuleContainer(footControl + '.' + attr, attr, publishToOuterContainers=True)

        #footControlAttributes = ('pv_follow')
        #cmds.select(footControl) 

        #cmds.addAttr(shortName=footControlAttributes[0], at='enum', en='off:on', k=True)
        """ Publish attributes to the top level character container """
        #self.publishNameToModuleContainer(footControl + '.' + attr, attr, publishToOuterContainers=True)
            
   

        """ Parent foot control to root parent"""
        cmds.parent(footControlRootParent, moduleGrp, relative=True)
        
        """ Position and orient foot control"""
        footControlPos = [ankleJoint_modulePos[0], ballJoint_modulePos[1], ankleJoint_modulePos[2]]
        cmds.xform(footControl, objectSpace=True, absolute=True, translation=footControlPos)
        
        """ Position the foot control pivot at the ankle """
        cmds.xform(footControl, ws=True, p=True, piv=[ankleJoint_modulePos[0], ankleJoint_modulePos[1], ankleJoint_modulePos[2]])  
 
        cmds.setAttr(footControl+".rotateOrder", 3) #3 = xyz
        
        orientationVector = [toeJoint_modulePos[0] - ankleJoint_modulePos[0], toeJoint_modulePos[2] - ankleJoint_modulePos[2] ]
        
        footControlRotation = atan2(orientationVector[1], orientationVector[0])
        cmds.setAttr(footControl+".rotateY", -degrees(footControlRotation))
        
        # Hookup stretchiness attribute
        cmds.select(footControl)
        cmds.addAttr(at="float", minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True, longName="stretchiness")
        self.publishNameToModuleContainer(footControl+".stretchiness", "stretchiness", publishToOuterContainers=True)
        
        cmds.connectAttr(footControl+".stretchiness", stretchinessAttribute, force=True)
  
        """ Setup for ball and Toe controls"""
        ballToeControls = []
        ballToeControl_orientGrps = []
        rootParents =  []
        for joint in [ankleJoint, ballJoint]:
            controlObjectInstance = controlObject.ControlObject()
            jointName = utils.stripAllNamespaces(joint)[1]
            name = jointName + "_pivotControl"
            
            ryControlInfo = controlObjectInstance.create(name, "needleControl.ma", self, lod=2, translation=True, rotation=False, globalScale=False, spaceSwitching=False)
            ryControl = ryControlInfo[0]
            ryControlRootParent = ryControlInfo[0]
            
            ballToeControls.append(ryControl)
            rootParents.append(ryControlInfo[0])
            
            orientGrp = cmds.group(empty=True, n=ryControl+"_orientGrp")
            containedNodes.append(orientGrp)
            ballToeControl_orientGrps.append(orientGrp)
 
            cmds.parent(ryControl, orientGrp, relative=True)
    
            
        cmds.xform(ballToeControl_orientGrps[0], objectSpace=True, absolute=True, translation=ankleJoint_modulePos)
        cmds.xform(ballToeControl_orientGrps[1], objectSpace=True, absolute=True, translation=ballJoint_modulePos)

        heelControlRootParent = rootParents[0]
        bankControlRootParent = rootParents[1]
     
        for grp in ballToeControl_orientGrps:
            cmds.parent(grp, moduleGrp, absolute=True)
            
        """ This aligns the leg """
        #cmds.parent(ikEndPosLocator, ballToeControls[0], absolute=True)
        
        """ Ankle IK """
        ankleIKNodes = cmds.ikHandle(sj=ankleJoint, ee=ballJoint, solver="ikSCsolver", n=ankleJoint+"_ikHandle")
        ankleIKNodes[1] = cmds.rename(ankleIKNodes[1], ankleIKNodes[1]+"_ikEffector")
        containedNodes.extend(ankleIKNodes)
        namespaceObjects.append(ankleIKNodes[0])
        namespaceObjects.append(ankleIKNodes[1])
        
        
        cmds.setAttr(ankleIKNodes[0]+".visibility", 0)
        
        """ Ball IK  """
        ballIKNodes = cmds.ikHandle(sj=ballJoint, ee=toeJoint, solver="ikSCsolver", n=ballJoint+"_ikHandle")
        ballIKNodes[1] = cmds.rename(ballIKNodes[1], ballIKNodes[1]+"_ikEffector")
        containedNodes.extend(ballIKNodes)
        namespaceObjects.append(ballIKNodes[0])
        namespaceObjects.append(ballIKNodes[1])
        
        cmds.setAttr(ballIKNodes[0]+".visibility", 0)
                 
        utils.addNodeToContainer(moduleContainer, containedNodes, ihb=True)
        
        
        """ Empty the contained nodes list """
        containedNodes = []

   
        """ Create the IK_Groups """
        ikGroups = []
        
        """ These groups go at the ankle """
        ikGrp = cmds.group(em=True, name='footIK_grp')
        cmds.xform(ikGrp, a=True, t=ankleJoint_modulePos)
        ikGroups.append(ikGrp)
        containedNodes.append(ikGrp)
        
        """ These go at the ball """
        groupNames = ('bank_grp', 'ballTwist_grp', 'ballRoll_grp', 'toeFlap_grp')
        for group in groupNames:
            cmds.group(em=True, name=group)
            cmds.xform(group, a=True, t=ballJoint_modulePos)
            ikGroups.append(group)
            containedNodes.append(group)
  
        """ These go at the toe """
        ikGrp = cmds.group(em=True, name='toeRoll_grp')
        cmds.xform(ikGrp, a=True, t=toeJoint_modulePos)
        ikGroups.append(ikGrp)
        containedNodes.append(ikGrp)
        
        """ Create a heel roll group """
        """ TODO:  How do I get this to sit at the heel without adding a joint for it? """
        ikGrp = cmds.group(em=True, name='heelRoll_grp')
        cmds.xform(ikGrp, a=True, t=(ankleJoint_modulePos[0], 0, ankleJoint_modulePos[2]) )
        ikGroups.append(ikGrp)
        containedNodes.append(ikGrp)
     
        """ Create 3 locators to be used for roll attribute """
        rollLctrs = []
        dynRollLctr = cmds.spaceLocator(name='dynRoll_lctr')[0]
        cmds.xform(dynRollLctr, a=True, t=ballJoint_modulePos)
        rollLctrs.append(dynRollLctr)
        containedNodes.append(dynRollLctr)
        
        statRollLctr = cmds.spaceLocator(name='statRoll_lctr')[0]
        cmds.xform(statRollLctr, a=True, t=ballJoint_modulePos)
        rollLctrs.append(statRollLctr)
        containedNodes.append(statRollLctr)
        
        """ heelRoll_lctr """
        heelRollLctr = cmds.spaceLocator(name='heelRoll_lctr')[0]
        cmds.xform(heelRollLctr, a=True, t=ballJoint_modulePos)
        rollLctrs.append(heelRollLctr)
        containedNodes.append(heelRollLctr)
        
        for locator in rollLctrs:
            cmds.setAttr(locator + '.visibility', 0) 
            
        """ Parent the adjustment controls to the foot control """
        cmds.parent(heelControlRootParent , ikGroups[3], absolute=True)
        cmds.makeIdentity(heelControlRootParent, apply=True, translate=True )        
        cmds.parent(bankControlRootParent , ikGroups[3], absolute=True)
        
        """ Parent the ikHandles under the appropriate group """
        cmds.parent(ankleIKNodes[0], ikGroups[3])
        cmds.parent(ikEndPosLocator, ikGroups[3])
        
        cmds.parent(ballIKNodes[0], ikGroups[4])
        
        cmds.parent(ikGroups[3], ikGroups[5]) #ballRoll  toeRoll  
        cmds.parent(ikGroups[4], ikGroups[5]) #toeFlap toeRoll   
        cmds.parent(ikGroups[5], ikGroups[2]) #toeRoll  ballTwist  
        cmds.parent(ikGroups[2], ikGroups[1]) #ballTwist  bank  
        cmds.parent(ikGroups[1], ikGroups[6]) #bank  heelRoll
        cmds.parent(ikGroups[6], ikGroups[0]) #heelRoll  footIK
        
        cmds.parent(dynRollLctr, ikGroups[0])
        cmds.parent(heelRollLctr, ikGroups[0])
        cmds.parent(statRollLctr, ikGroups[6])
        
        """ Parent constrain ball and toe groups to roll_lctrs """
        parentConstraints = []
        rollParentConstraint = cmds.parentConstraint(dynRollLctr, ikGroups[3], mo=True, st=('x', 'y', 'z'), sr=('y', 'z'))
        parentConstraints.append(rollParentConstraint[0])
        rollParentConstraint = cmds.parentConstraint(statRollLctr, ikGroups[3], mo=True, st=('x', 'y', 'z'), sr=('y', 'z'))
        parentConstraints.append(rollParentConstraint[0])
        rollParentConstraint = cmds.parentConstraint(statRollLctr, ikGroups[5], mo=True, st=('x', 'y', 'z'), sr=('y', 'z'))
        parentConstraints.append(rollParentConstraint[0])
        rollParentConstraint = cmds.parentConstraint(dynRollLctr, ikGroups[5], mo=True, st=('x', 'y', 'z'), sr=('y', 'z'))
        parentConstraints.append(rollParentConstraint[0])
        
        for constraint in parentConstraints:
            print constraint
            newName = moduleNamespace+':'+constraint
            cmds.rename(constraint, newName)
        
        
        """ Create a remap value node to control foot roll """
        cmds.createNode('remapValue', name ='roll_rv')
        cmds.setAttr('roll_rv.inputMax', 180.0)
        """ Connect to the remap value node """
        """" Connect the output of dynRollLctr to roll_rv input value """
        cmds.connectAttr(dynRollLctr + '.rx', 'roll_rv.inputValue' )
        """ roll_break to input min """
        cmds.setAttr(footControl + '.roll_break', 45.0)
        cmds.connectAttr(footControl + '.roll_break', 'roll_rv.inputMin')
        """ roll_break to parent constraint switches """
        cmds.connectAttr('roll_rv.outColorG', ikGroups[3] + '.blendParent2')
        cmds.connectAttr('roll_rv.outColorR', ikGroups[5] + '.blendParent2')
        namespaceObjects.append('roll_rv')
    
        """ constrain the heelRoll_grp to heelRoll_lctr.  Switch off the constraint when greater than 0 """
        cmds.createNode('condition', name='roll_cond')
        heelOrientConstraint = cmds.orientConstraint(heelRollLctr, ikGroups[6], skip=('y', 'z'), mo=True)
        heelOrientAttr = (heelOrientConstraint[0] + '.' + heelRollLctr +'W0')
        cmds.connectAttr('roll_cond.outColorR', heelOrientAttr)
        cmds.connectAttr(heelRollLctr + '.rx', 'roll_cond.firstTerm')
        cmds.setAttr('roll_cond.operation', 3)
        newName = moduleNamespace+':'+heelOrientConstraint[0]
        cmds.rename(heelOrientConstraint[0], newName)
        namespaceObjects.append('roll_cond')
        
        """ Connect the foot attributes to respective groups and locators """
        cmds.connectAttr(footControl + ".roll", heelRollLctr + '.rx')
        cmds.connectAttr(footControl + ".roll", 'dynRoll_lctr.rx')
        cmds.connectAttr(footControl + ".toe_twist", 'toeRoll_grp.ry')
        cmds.connectAttr(footControl + ".ball_twist", 'ballTwist_grp.ry')
        cmds.connectAttr(footControl + ".heel_twist", 'heelRoll_grp.ry')
        cmds.connectAttr(footControl + ".bank", 'bank_grp.rz')
        cmds.connectAttr(footControl + ".toe_flap", 'toeFlap_grp.rx')
        
        """ Connect pivot controls to the rotatePivot of appropriate group """
        cmds.connectAttr(rootParents[1]+'.translate', 'bank_grp.rotatePivot')
        cmds.connectAttr(rootParents[0]+'.translate', 'heelRoll_grp.rotatePivot')
        
        """ Parent the footIK_grp to the foot control """
        cmds.parent('footIK_grp', footControl, absolute=True)

        utils.addNodeToContainer(moduleContainer, containedNodes, ihb=True)
        
        for node in containedNodes:
            newName = moduleNamespace+':'+node
            cmds.rename(node, newName)
            
            
        """ Add the namespaceObjects to the moduleNamespace """
        
        for node in namespaceObjects:
            print node
            newName = moduleNamespace+':'+node
            cmds.rename(node, newName)

        
        
  
     
        
    def UI(self, parentLayout):
        footControl = self.blueprintNamespace+":"+self.moduleNamespace+":footControl"
        
        controlObjectInstance = controlObject.ControlObject(footControl)
        controlObjectInstance.UI(parentLayout)
        
        cmds.attrControlGrp(attribute=footControl+".stretchiness", label="Stretchiness")
        
        circleIK.CircleControlStretchyIK.UI(self, parentLayout)
        
        jointsGrp = self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp"
        joints = utils.findJointChain(jointsGrp)
        
        """ Remove ? """
        """
        ballJoint = joints[4]
        toeJoint = joints[5]
        
        for joint in [ballJoint, toeJoint]:
            jointControl = joint+"_ryControl"
            controlObjectInstance = controlObject.ControlObject(jointControl)
            controlObjectInstance.UI(parentLayout)
        """
            
            
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
  
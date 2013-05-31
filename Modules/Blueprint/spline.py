import maya.cmds as cmds

import System.blueprint as blueprintMod
#reload(blueprintMod)

import System.utils as utils

import os

from functools import partial

CLASS_NAME = "Spline"

TITLE = "Spline"
DESCRIPTION = "Creates an optionaly interpolating joint count adjustable spline.  Ideal use:  Spine, neck/head, tail, tentacles, etc."
ICON = os.environ["GEPPETTO"] + "/Icons/spline_button.bmp"

class Spline(blueprintMod.Blueprint):
    def __init__(self, userSpecifiedName, hookObject, numberOfJoints=None, startJointPos=None, endJointPos=None):
        if numberOfJoints == None:
            jointsGrp = CLASS_NAME + "__" + userSpecifiedName +":joints_grp"
            if not cmds.objExists(jointsGrp):
                numberOfJoints = 5 # default
            else:
                joints = utils.findJointChain(jointsGrp)
                joints.pop()
                numberOfJoints = len(joints)
                
        jointInfo = []
        gameJntNames = []
        
        if startJointPos == None:
            startJointPos = [0.0, 0.0, 0.0]
        if endJointPos == None:
            endJointPos = [0.0, 5.0, 0.0]
            
        jointIncrement = list(endJointPos)
        
        jointIncrement[0] -= startJointPos[0]
        jointIncrement[1] -= startJointPos[1]
        jointIncrement[2] -= startJointPos[2]
        
        jointIncrement[0] /= (numberOfJoints - 1)
        jointIncrement[1] /= (numberOfJoints - 1)
        jointIncrement[2] /= (numberOfJoints - 1)
        
        jointPos = startJointPos
        
        for i in range(numberOfJoints):
            jointName = "spline_"+str(i)+"_joint"
            gameJntName = "spline_"+str(i)+"_"
            
            jointInfo.append([jointName, list(jointPos)])
            gameJntNames.append(gameJntName)
            
            jointPos[0] += jointIncrement[0]
            jointPos[1] += jointIncrement[1]
            jointPos[2] += jointIncrement[2]
            
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=0)
        
        self.canBeMirrored = False
        
    #112    
    def install_custom(self, joints):
     
        self.setup_interpolation()
        
        moduleGrp = self.moduleNamespace+":module_grp"
        cmds.select(moduleGrp)
        
        cmds.addAttr(at="enum", enumName="y:z", longName="sao_local")
        cmds.addAttr(at="enum", enumName="+x:-x:+y:-y:+z:-z", longName="sao_world")
        
        for attr in ["sao_local", "sao_world"]:
            cmds.container(self.containerName, edit=True, publishAndBind=[moduleGrp+"."+attr, attr])
            
            
        
        
    def setup_interpolation(self, unlockContainer=False, *args):

        previousSelection = cmds.ls(sl=True)
        
        if unlockContainer:
            cmds.lockNode(self.containerName, lock=False, lockUnpublished=False)
            
        joints = self.getJoints()
        numberOfJoints = len(joints)
        
        startControl = self.getTranslationControl(joints[0])
        endControl = self.getTranslationControl(joints[numberOfJoints-1])
        
        pointConstraints = []
        
        for i in range(1, numberOfJoints-1):
            material = joints[i] + "_m_translation_control"
            cmds.setAttr(material+".colorR", 0.815)
            cmds.setAttr(material+".colorG", 0.629)
            cmds.setAttr(material+".colorB", 0.498)
            
            translationControl = self.getTranslationControl(joints[i])
            # Index / number of joints -1
            endWeight = 0.0 + (float(i) / (numberOfJoints-1))
            startWeight = 1.0 - endWeight
            
            pointConstraints.append(cmds.pointConstraint(startControl, translationControl, maintainOffset=False, weight=startWeight)[0])
            pointConstraints.append(cmds.pointConstraint(endControl, translationControl, maintainOffset=False, weight=endWeight)[0])
            
            for attr in [".translateX", ".translateY", ".translateZ"]:
                cmds.setAttr(translationControl+attr, lock=True)
        # Create a container to hold all the constraints       
        interpolationContainer = cmds.container(n=self.moduleNamespace+":interpolation_container")
        utils.addNodeToContainer(interpolationContainer, pointConstraints)
        utils.addNodeToContainer(self.containerName, interpolationContainer)
                      
        if unlockContainer:
            cmds.lockNode(self.containerName, lock=True, lockUnpublished=True)
            
        if len(previousSelection) > 0: 
           cmds.select(previousSelection, replace=True)
        else:
            cmds.select(clear=True)
            
    def UI_custom(self): 

           
        cmds.rowLayout(nc=2, columnWidth=[1, 100], adj=2)
        cmds.text(label="Number Of Joints:")
        numJoints = len(self.jointInfo)
        self.numberOfJointsField = cmds.intField(value=numJoints, min=2, changeCommand=self.changeNumberOfJoints)
        
        cmds.setParent("..")
        
        joints = self.getJoints()
        
        self.createRotationOrderUIControl(joints[0])
        
        cmds.separator()
        
        cmds.text(label="Orientation:", align="left")
        cmds.rowLayout(nc=3)
        cmds.attrEnumOptionMenu(attribute=self.moduleNamespace+":module_grp.sao_local", label="Local:")
        cmds.text(label="will be oriented to")
        cmds.attrEnumOptionMenu(attribute=self.moduleNamespace+":module_grp.sao_world", label="World:")
        
        cmds.setParent("..")
        
        cmds.separator()
        
        interpolating = False
        if cmds.objExists(self.moduleNamespace+":interpolation_container"):
            interpolating = True
            
        cmds.rowLayout(nc=2, columnWidth=[1, 80], adj=2)
        cmds.text(label="Interpolate:")
        cmds.checkBox(label="", value=interpolating, onc=partial(self.setup_interpolation, True), ofc=self.delete_interpolation)
        
    def delete_interpolation(self, *args):

        cmds.lockNode(self.containerName, lock=False, lockUnpublished=False)
        joints = self.getJoints()
        
        for i in range(1, len(joints)-1):
            translationControl = self.getTranslationControl(joints[i])
            for attr in [".translateX", ".translateY", ".translateZ"]:
                cmds.setAttr(translationControl+attr, l=False)
                
            material = joints[i] + "_m_translation_control"
            cmds.setAttr(material+".colorR", 0.758)
            cmds.setAttr(material+".colorG", 0.051)
            cmds.setAttr(material+".colorB", 0.102)
            
        cmds.delete(self.moduleNamespace+":interpolation_container")
        
        cmds.lockNode(self.containerName, lock=True, lockUnpublished=True)
        
    def changeNumberOfJoints(self, *args):

        self.blueprint_UI_instance.deleteScriptJob()
        
        joints = self.getJoints()
        numJoints = len(joints)
        newNumJoints = cmds.intField(self.numberOfJointsField, q=True, value=True)
        
        startPos = cmds.xform(self.getTranslationControl(joints[0]), q=True, ws=True, t=True)
        endPos = cmds.xform(self.getTranslationControl(joints[numJoints-1]), q=True, ws=True, t=True)
        
        hookObject = self.findHookObjectForLock()
        
        rotationOrder = cmds.getAttr(joints[0] + ".rotateOrder")
        sao_local = cmds.getAttr(self.moduleNamespace+":module_grp.sao_local")
        sao_world = cmds.getAttr(self.moduleNamespace+":module_grp.sao_world")
        
        self.delete()
        
        newInstance = Spline(self.userSpecifiedName, hookObject, newNumJoints, startPos, endPos)
        newInstance.install()
        # We have to refer to the new instance stored in memory
        newJoints = newInstance.getJoints()
        
        cmds.setAttr(newJoints[0]+".rotateOrder", rotationOrder)
        
        cmds.setAttr(newInstance.moduleNamespace+":module_grp.sao_local", sao_local)
        cmds.setAttr(newInstance.moduleNamespace+":module_grp.sao_world", sao_world)
        
        self.blueprint_UI_instance.createScriptJob()
        
        cmds.select(newInstance.moduleNamespace+":module_transform", replace=True)
    #115   
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
        jointRotationOrders = []
        jointPreferredAngles = []

        joints = self.getJoints()
        
        jointOrientationSettings = []
        moduleGrp = self.moduleNamespace+":module_grp"
        
        localAxis = cmds.getAttr(moduleGrp+".sao_local")
        
        if localAxis == 0:
            jointOrientationSettings.append("xyz")
        else:
            jointOrientationSettings.append("xzy")
            
        worldAxis = cmds.getAttr(moduleGrp+".sao_world")
        if worldAxis == 0:
            jointOrientationSettings.append("xup")
        elif worldAxis == 1:
            jointOrientationSettings.append("xdown")
        elif worldAxis == 2:
            jointOrientationSettings.append("yup")
        elif worldAxis == 3:
            jointOrientationSettings.append("ydown")
        elif worldAxis == 4:
            jointOrientationSettings.append("zup")
        elif worldAxis == 5:
            jointOrientationSettings.append("zdown")
            
        for joint in joints:
            jointPositions.append(cmds.xform(joint, q=True, ws=True, t=True))
            jointRotationOrders.append(cmds.getAttr(joints[0]+".rotateOrder"))
            jointOrientationValues.append(jointOrientationSettings)
            
        jointOrientations = (None, jointOrientationValues)
        
        hookObject = self.findHookObjectForLock()
        # Using rootTransform=True breaks the spline.  Turning it false for now.
        rootTransform=False
        
        moduleNamespace = self.moduleNamespace
            
        moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform, moduleNamespace)
        return moduleInfo
        

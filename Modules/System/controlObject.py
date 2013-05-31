import maya.cmds as cmds

import System.utils as utils

import os

from functools import partial

class ControlObject:
    def __init__(self, controlObject = None):
        if controlObject != None:
            self.controlObject = controlObject
            
            # Define what axis the module can move on.
            # If attr is locked in animation control object blueprint, then value will be set to false.
            self.translation = []
            self.translation.append(not cmds.getAttr(self.controlObject+".translateX", l=True))
            self.translation.append(not cmds.getAttr(self.controlObject+".translateY", l=True))
            self.translation.append(not cmds.getAttr(self.controlObject+".translateZ", l=True))
            
            self.rotation = []
            self.rotation.append(not cmds.getAttr(self.controlObject+".rotateX", l=True))
            self.rotation.append(not cmds.getAttr(self.controlObject+".rotateY", l=True))
            self.rotation.append(not cmds.getAttr(self.controlObject+".rotateZ", l=True))
            
            self.globalScale = not cmds.getAttr(self.controlObject+".scaleY", l=True)
            
    def create(self, name, controlFile, animationModuleInstance, lod=1, translation=True, rotation=True, globalScale=True, spaceSwitching=False):
        if translation == True or translation == False:
            translation = [translation, translation, translation]
            
        if rotation == True or rotation == False:
            rotation = [rotation, rotation, rotation]
            
        self.translation = translation
        self.rotation = rotation
        self.globalScale = globalScale
            
        animationModuleName = animationModuleInstance.moduleNamespace
        blueprintModuleNamespace = animationModuleInstance.blueprintNamespace
        blueprintModuleUserSpecifiedName = utils.stripAllNamespaces(blueprintModuleNamespace)[1].partition("__")[2]
        
        animationModuleNamespace = blueprintModuleNamespace + ":" + animationModuleName
        # This system currently pulls in control objects from a maya file.  I would like to change this so control objects are built on the fly.  
        # I may also want to use the lo rez geo as a control.
        controlObjectFile = os.environ["GEPPETTO"] + "/ControlObjects/Animation/" + controlFile
        cmds.file(controlObjectFile, i=True)
        
        self.controlObject = cmds.rename("control", animationModuleNamespace+":"+name)
        self.rootParent = self.controlObject
        
        self.setupIconScale(animationModuleNamespace)
        
        # Set control object drawing overrides.
        cmds.setAttr(self.controlObject+".overrideEnabled", 1)
        cmds.setAttr(self.controlObject+".overrideShading", 0)
        cmds.connectAttr(animationModuleNamespace+":module_grp.overrideColor", self.controlObject+".overrideColor")
        
        # Add objects to container and setup attrs for global scale.
        cmds.container(animationModuleNamespace+":module_container", edit=True, addNode=self.controlObject, ihb=True, includeNetwork=True)
        
        if globalScale:
            cmds.connectAttr(self.controlObject+".scaleY", self.controlObject+".scaleX")
            cmds.connectAttr(self.controlObject+".scaleY", self.controlObject+".scaleZ")
            cmds.aliasAttr("globalScale", self.controlObject+".scaleY")
            
        # Promote attrs to top level container.
        attributes=[]
        
        if self.translation == [True, True, True]:
            attributes.append([True, ".translate", "T"])
        else:
            attributes.extend([ [translation[0], ".translateX", "TX"], [translation[1], ".translateY", "TY"], [translation[2], ".translateZ", "TZ"]])
        
        if self.rotation == [True, True, True]:
            attributes.append([True, ".rotate", "R"])
        else:
            attributes.extend([ [rotation[0], ".rotateX", "RX"], [rotation[1], ".rotateY", "RY"], [rotation[2], ".rotateZ", "RZ"]])
        
        attributes.append([globalScale, ".globalScale", "scale"])
        
        for attrInfo in attributes:
            if attrInfo[0]:
                attributeNiceName = name + "_" + attrInfo[2]
                animationModuleInstance.publishNameToModuleContainer(self.controlObject+attrInfo[1], attributeNiceName, publishToOuterContainers=True)
            
        cmds.select(self.controlObject, replace=True)
        cmds.addAttr(at="bool", defaultValue=1, k=True, ln="display")
        animationModuleInstance.publishNameToModuleContainer(self.controlObject+".display", "display", publishToOuterContainers=False)
        
        # Create an expression to tie together module grp vis and lod.
        moduleGrp = animationModuleNamespace+":module_grp"
        visibilityExpression = self.controlObject+".visibility = " + self.controlObject+".display * (" + moduleGrp+".lod >= " +str(lod) + ");"       
        expression = cmds.expression(n=self.controlObject+"_visibility_expression", string=visibilityExpression)
        utils.addNodeToContainer(animationModuleNamespace+":module_container", expression)
        
        # 173 >
        axisInverse = cmds.spaceLocator(name=self.controlObject+"_axisInverse")[0]
        cmds.parent(axisInverse, self.controlObject, relative=True)
        cmds.setAttr(axisInverse+".visibility", 0)
        utils.addNodeToContainer(animationModuleNamespace+":module_container", axisInverse, ihb=True)
        
        spaceSwitchTarget = cmds.spaceLocator(name=self.controlObject+"_spaceSwitchTarget")[0]
        cmds.setAttr(spaceSwitchTarget + ".visibility", 0)
        cmds.parent(spaceSwitchTarget, self.controlObject, relative=True)
        cmds.setAttr(axisInverse+".visibility", 0)
        utils.addNodeToContainer(animationModuleNamespace+":module_container", axisInverse, ihb=True)
        
        if self.rotation ==[False, False, False]:
            self.setupMirroring(blueprintModuleNamespace, animationModuleNamespace, axisInverse)
            
        if spaceSwitching:
            self.setupSpaceSwitching(blueprintModuleNamespace, animationModuleNamespace, animationModuleInstance)
 
        # < 173 
        return(self.controlObject, self.rootParent) 
    
    # Create a cluster on the control object to scale the shape without effecting the4 transform.
    def setupIconScale(self, animationModuleNamespace):
        clusterNodes = cmds.cluster(self.controlObject, n=self.controlObject+"_icon_scale_cluster", relative=True) 
        cmds.container(animationModuleNamespace+":module_container", edit=True, addNode=clusterNodes, ihb=True, includeNetwork=True)
        
        clusterHandle = clusterNodes[1]
        
        cmds.setAttr(clusterHandle+".scalePivotX", 0)
        cmds.setAttr(clusterHandle+".scalePivotY", 0)
        cmds.setAttr(clusterHandle+".scalePivotZ", 0)
        
        cmds.connectAttr(animationModuleNamespace+":module_grp.iconScale", clusterHandle+".scaleX")
        cmds.connectAttr(animationModuleNamespace+":module_grp.iconScale", clusterHandle+".scaleY")
        cmds.connectAttr(animationModuleNamespace+":module_grp.iconScale", clusterHandle+".scaleZ")
        
        cmds.parent(clusterHandle, self.controlObject, absolute=True)
        cmds.setAttr(clusterHandle+".visibility", 0)
    
    # 173
    def setupMirroring(self, blueprintModuleNamespace, animationModuleNamespace, axisInverse):  
        moduleGrp = blueprintModuleNamespace+":module_grp"
        
        if cmds.attributeQuery("mirrorInfo", n=moduleGrp, exists=True):
            enumValue = cmds.getAttr(moduleGrp+".mirrorInfo")
            
            if enumValue == 0: # "None"
                return
            
            mirrorAxis = ""
            
            if enumValue == 1:
                mirrorAxis = "X"
            elif enumValue == 2:
                mirrorAxis = "Y"
            elif enumValue == 3:
                mirrorAxis = "Z"
                
            mirrorGrp = cmds.group(empty=True, name=self.controlObject+"_mirror_grp")
            self.rootParent = mirrorGrp
            
            cmds.parent(self.controlObject, mirrorGrp, absolute=True)
            
            cmds.setAttr(mirrorGrp+".scale"+mirrorAxis, -1)
            cmds.setAttr(axisInverse+".scale"+mirrorAxis, -1)
            
            utils.addNodeToContainer(animationModuleNamespace+":module_container", mirrorGrp)
                
    # 174            
    def setupSpaceSwitching(self, blueprintModuleNamespace, animationModuleNamespace, animationModuleInstance):
        cmds.select(self.controlObject, replace=True)
        # Do we have spaceswitching and is it orientation only
        cmds.addAttr(at="bool", defaultValue=True, keyable=False, longName="spaceSwitching")
        cmds.addAttr(at="bool", defaultValue=False, keyable=False, longName="switchOrientationOnly")
        
        spaceSwitcher = cmds.group(empty=True, name=self.controlObject+"_spaceSwitcher")
        
        if self.translation != [True, True, True]:
            cmds.setAttr(self.controlObject+".switchOrientationOnly", True)
            
        cmds.parent(self.rootParent, spaceSwitcher, absolute=True)
        self.rootParent = spaceSwitcher
        
        utils.addNodeToContainer(animationModuleNamespace+":module_container", spaceSwitcher)
        
        self.switchSpace(blueprintModuleNamespace+":HOOK_IN", "Module Hook")
        
        controlObjectName = utils.stripAllNamespaces(self.controlObject)[1]
        animationModuleInstance.publishNameToModuleContainer(spaceSwitcher+".currentSpace", controlObjectName+"_currentSpace", publishToOuterContainers=True)
        
        
    # 173    
    def switchSpace(self, targetObject, spaceName, index=-1, maintainOffset=False, setKeyframes=False):
        if cmds.objExists(targetObject+"_spaceSwitchTarget"):
            targetObject = targetObject+"_spaceSwitchTarget"
            
        setKeyframes = setKeyframes and maintainOffset
        
        currentPosition = cmds.xform(self.controlObject, q=True, worldSpace=True, translation=True)
        currentOrientation = cmds.xform(self.controlObject, q=True, worldSpace=True, rotation=True)
        currentScale = self.getCurrentScale()
        
        spaceSwitcher = self.controlObject+"_spaceSwitcher"
        animModuleNamespace = utils.stripAllNamespaces(self.controlObject)[0]
        
        if index == -1:
            cmds.select(spaceSwitcher)
            enumIndex = 0
            
            if cmds.attributeQuery("currentSpace", n=spaceSwitcher, exists=True):
                currentEntries = cmds.attributeQuery("currentSpace", n=spaceSwitcher, listEnum=True)[0]
                newEntry = currentEntries + ":" + spaceName
                cmds.addAttr(spaceSwitcher+".currentSpace", edit=True, enumName=newEntry)
                
                enumIndex = len(currentEntries.split(":"))
                
            else:
                cmds.addAttr(at="enum", enumName=spaceName, keyable=True, longName="currentSpace")
                
            if self.globalScale:
                scaleConstraint = cmds.scaleConstraint(targetObject, spaceSwitcher, n=spaceSwitcher+"_scaleConstraint", maintainOffset=False)[0]
                
            skipTranslate = "none"
            if cmds.getAttr(self.controlObject+".switchOrientationOnly"):
                skipTranslate = ["x", "y", "z"]
             
            parentConstraint = cmds.parentConstraint(targetObject, spaceSwitcher, n=spaceSwitcher+"_parentConstraint", maintainOffset=False, skipTranslate=skipTranslate)[0]
            
            parentWeightList = cmds.parentConstraint(parentConstraint, q=True, weightAliasList=True)
            parentWeight = parentConstraint + "." + parentWeightList[len(parentWeightList)-1]
            
            attrs = [(parentWeight, "parent")]
            containedNodes = [parentConstraint]
            
            if self.globalScale:
                scaleWeightList = cmds.scaleConstraint(scaleConstraint, q=True, weightAliasList=True)
                scaleWeight = scaleConstraint + "." + scaleWeightList[len(scaleWeightList)-1]
                
                attrs.append( (scaleWeight, "scale") )
                containedNodes.append(scaleConstraint)
                
            for attr in attrs:
                expressionString = attr[0] + " = (" + spaceSwitcher + ".currentSpace == " + str(enumIndex) + ");\n"
                expressionName = spaceSwitcher+"_"+attr[1]+"WeightExpression_"+str(enumIndex)
                containedNodes.append(cmds.expression(name=expressionName, string=expressionString))
                
            utils.addNodeToContainer(animModuleNamespace+":module_container", containedNodes)
            
            index = enumIndex
            
        transformAttributes = ( [self.translation[0], "translateX"], [self.translation[1], "translateY"], [self.translation[2], "translateZ"], [self.rotation[0], "rotateX"], [self.rotation[1], "rotateY"], [self.rotation[2], "rotateZ"], [self.globalScale, "globalScale"] )
        currentTime = cmds.currentTime(q=True)
        if setKeyframes:
            for attribute in transformAttributes:
                if attribute[0]:
                    if not cmds.selectKey(self.controlObject, attribute=attribute[1], time=(currentTime-1,)) > 0:
                        value = cmds.getAttr(self.controlObject+"."+attribute[1], time=currentTime-1 )
                        cmds.setKeyframe(self.controlObject, attribute=attribute[1], time=currentTime-1, value=value, outTangentType="step")
                        
        cmds.setAttr(spaceSwitcher+".currentSpace", index)
        cmds.setKeyframe(spaceSwitcher, at="currentSpace", ott="step")
        utils.addNodeToContainer(animModuleNamespace+":module_container", spaceSwitcher+"_currentSpace")
        
        if maintainOffset:
            if self.globalScale == True:
                newScale = self.getCurrentScale()
                scaleRatio = newScale/currentScale
                newScaleAttributeValue = cmds.getAttr(self.controlObject+".scaleY") / scaleRatio
                cmds.setAttr(self.controlObject+".scaleY", newScaleAttributeValue)
                
            if self.rotation == [True, True, True]:
                cmds.xform(self.controlObject, ws=True, a=True, rotation=currentOrientation)
                
            if self.translation == [True, True, True]:
                cmds.xform(self.controlObject, ws=True, a=True, translation=currentPosition)
                
        if setKeyframes:
            for attribute in transformAttributes:
                if attribute[0]:
                    cmds.setKeyframe(self.controlObject, attribute=attribute[1])
                    
                      
    # 173    
    def getCurrentScale(self):
        locator = cmds.spaceLocator()[0]        
        cmds.scaleConstraint(self.controlObject, locator)        
        scale = cmds.getAttr(locator+".scaleY")        
        cmds.delete(locator)        
        return scale
          
    #161
    def UI(self, parentLayout):
        cmds.setParent(parentLayout)
        cmds.separator()
        
        niceName = utils.stripLeadingNamespace(self.controlObject)[1]
        cmds.text(label=niceName)
        
        cmds.attrControlGrp(attribute=self.controlObject+".display", label="Visibility: ")
        
        if self.translation == [True, True, True]:
            cmds.attrControlGrp(attribute=self.controlObject+".translate", label="Translate")
        else:
            if self.translation[0] == True:
                cmds.attrControlGrp(attribute=self.controlObject+".translateX", label="Translate X")
            
            if self.translation[1] == True:
                cmds.attrControlGrp(attribute=self.controlObject+".translateY", label="Translate Y")
                
            if self.translation[2] == True:
                cmds.attrControlGrp(attribute=self.controlObject+".translateZ", label="Translate Z")
                

        if self.rotation == [True, True, True]:
            cmds.attrControlGrp(attribute=self.controlObject+".rotate", label="Rotate")
        else:
            if self.translation[0] == True:
                cmds.attrControlGrp(attribute=self.controlObject+".rotateX", label="Rotate X")
            
            if self.translation[1] == True:
                cmds.attrControlGrp(attribute=self.controlObject+".rotateY", label="Rotate Y")
                
            if self.translation[2] == True:
                cmds.attrControlGrp(attribute=self.controlObject+".rotateZ", label="Rotate Z")
        # WARNING Commented out the global scale here.        
        if self.globalScale == True:
            try:
                cmds.attrControlGrp(attribute=self.controlObject+".globalScale", label="Scale")
            except: pass
            
    #176
    def switchSpace_UI(self, targetObject):
        constraint = self.controlObject+"_spaceSwitcher_scaleConstraint"
        if not cmds.objExists(constraint):
            constraint = self.controlObject+"_spaceSwitcher_parentConstraint"
            if not cmds.objExists(constraint):
                print "ERROR: Control object appears to have no space switching capabilities"
                return
            
        spaceNameText = "[a-z][A-Z][0-9] or _ only"
        spaceNameEnable = True
        
        enumIndex = -1
        index = 0
        done = False
        
        while not done:
            attribute = constraint+".target["+str(index)+"].targetScale"
            if cmds.connectionInfo(attribute, isDestination=True):
                connection = cmds.listConnections(attribute)[0]
                
                if connection == targetObject + "_spaceSwitchTarget" or connection == targetObject:
                    enumIndex = index
                    
                    enumEntries = cmds.attributeQuery("currentSpace", n=self.controlObject+"_spaceSwitcher", listEnum=True)[0]
                    enumEntriesList = enumEntries.split(":")
                    
                    spaceNameText = enumEntriesList[index]
                    spaceNameEnable = False
                    
                    done = True
            
            else:
                done = True
                
            index += 1
            
        self.windowName = "switchSpace_UI_window"
        
        self.UIElements = {}
        
        if cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName)
            
        self.windowWidth = 300
        self.windowHeight = 200
        self.UIElements["window"] = cmds.window(self.windowName, width=self.windowWidth, height=self.windowHeight, title="Switch_Space", sizeable=False)
        
        self.UIElements["topColumnLayout"] = cmds.columnLayout(adj=True, rs=3)
        
        self.UIElements["spaceName_rowColumn"] = cmds.rowColumnLayout(nc=2, columnAttach=(1, "right", 0), columnWidth = [(1, 80), (2, self.windowWidth-90)])       
        cmds.text(label="Space Name :")
        self.UIElements["spaceName"] = cmds.textField(enable=spaceNameEnable, text=spaceNameText)
        
        cmds.setParent(self.UIElements["topColumnLayout"])
        
        cmds.separator()
        self.UIElements["maintainOffset_checkBox"] = cmds.checkBox(label="Maintain Offset?", value=True)
        self.UIElements["setKeyframes_checkBox"] = cmds.checkBox(label="Set Keyframes on Control?", value=False)
        cmds.separator()
        
        columnWidth = (self.windowWidth/2) - 5
        self.UIElements["button_row"] = cmds.rowLayout( nc=2, columnWidth=[(1, columnWidth), (2, columnWidth)], cat=[(1, "both", 10), (2, "both", 10)], columnAlign = [(1, "center"), (2, "center")])
        cmds.button(label="Accept", c=partial(self.acceptWindow, targetObject, enumIndex))
        cmds.button(label="Cancel", c=self.cancelWindow)
        cmds.showWindow(self.UIElements["window"])
        
        
    def acceptWindow(self, targetObject, enumIndex, *args):
        spaceName = cmds.textField(self.UIElements["spaceName"], q=True, text=True)
        maintainOffset = cmds.checkBox(self.UIElements["maintainOffset_checkBox"], q=True, value=True)
        setKeyframes = cmds.checkBox(self.UIElements["setKeyframes_checkBox"], q=True, value=True)
        
        cmds.deleteUI(self.UIElements["window"])
        
        animModuleNamespace = utils.stripAllNamespaces(self.controlObject)[0]
        blueprintModuleNamespace = utils.stripAllNamespaces(animModuleNamespace)[0]
        characterNamespace = utils.stripAllNamespaces(blueprintModuleNamespace)[0]
        
        containers = (characterNamespace+":character_container", blueprintModuleNamespace+":module_container", animModuleNamespace+":module_container")
        
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
            
        self.switchSpace(targetObject, spaceName, index=enumIndex, maintainOffset=maintainOffset, setKeyframes=setKeyframes )
               
        for c in containers:    
            cmds.lockNode(c, lock=True, lockUnpublished=True)
            
        cmds.select(self.controlObject, replace=True)
        
    def cancelWindow(self, *args):
        cmds.deleteUI(self.UIElements["window"])
        
        
            
    
        
    
            
                
        
        
            
 
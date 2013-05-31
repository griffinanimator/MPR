import maya.cmds as cmds
import os
import System.utils as utils
from functools import partial



class ControlModule():
    def __init__(self, moduleNamespace):
        print " Control Module Init"
        self.moduleContianer = None
        
        if moduleNamespace == None:
            return
        
        moduleNamespaceInfo = utils.stripAllNamespaces(moduleNamespace)
        
        self.blueprintNamespace = moduleNamespaceInfo[0]
        self.moduleNamespace = moduleNamespaceInfo[1]
        self.characterNamespaceOnly = utils.stripLeadingNamespace(self.blueprintNamespace)[0]
        
        self.moduleContainer = self.blueprintNamespace + ":" + self.moduleNamespace + ":module_container"
        
        self.publishedNames = []
        
    def install_custom(self, joints, moduleGrp, moduleContainer):
        print " install_custom() method not implemented by derived module."
        
    def install_requirements(self):
        return True
        
    def compatibleBlueprintModules(self):
        return ("-1",)
    
    # 160
    # Module specific controls
    def UI(self, parentLayout):
        print "No custom user interface provided"
        
    def UI_preferences(self, parentLayout):
        print " No custom preferences user interface provided"
    # <160
    
    # 164>
    def match(self, *args):
        print "No matching functionality provided"
        
    
    def install(self):
        # <191
        if self.install_requirements()== False:
            return
        # <191
        # initialization.  Needs to happen for every animation control module.
        nodes = self.install_init()
        joints = nodes[0]
        moduleGrp = nodes[1]
        moduleContainer = nodes[2]
        
        self.install_custom(joints, moduleGrp, moduleContainer)
        self.install_finalize()
        
        
    def install_init(self):
        cmds.namespace(setNamespace=self.blueprintNamespace)
        cmds.namespace(add=self.moduleNamespace)
        cmds.namespace(setNamespace=":")
        
        characterContainer = self.characterNamespaceOnly+":character_container"
        blueprintContainer = self.blueprintNamespace+":module_container"
        containers = [characterContainer, blueprintContainer]
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
            
        # Duplicate creation pose joints to create new instance. Stored in external method.   
        self.joints = self.duplicateAndRenameCreationPose()
        moduleJointsGrp = self.joints[0]
        
        # Group everything for animation module and parent to "Hook_IN_Grp"
        moduleGrp = cmds.group(empty=True, name=self.blueprintNamespace+":"+self.moduleNamespace+":module_grp")
        hookIn = self.blueprintNamespace+":HOOK_IN"
        cmds.parent(moduleGrp, hookIn, relative=True)
        cmds.parent(moduleJointsGrp, moduleGrp, absolute=True)
        
        # Attr to define icon size.
        cmds.select(moduleGrp)
        cmds.addAttr(at="float", ln="iconScale", min=0.001, softMaxValue=10.0, defaultValue=1, k=True)
        cmds.setAttr(moduleGrp+".overrideEnabled", 1)
        cmds.setAttr(moduleGrp+".overrideColor", 6)
        
        utilityNodes = self.setupBlueprintWeightBasedBlending()
        
        self.setupModuleVisibility(moduleGrp)
        
        containedNodes = list(self.joints)
        containedNodes.append(moduleGrp)
        containedNodes.extend(utilityNodes)
        
        self.moduleContainer = cmds.container(n=self.moduleContainer)
        utils.addNodeToContainer(self.moduleContainer, containedNodes, ihb=True)
        utils.addNodeToContainer(blueprintContainer, self.moduleContainer)
        #151
        index = 0
        publishToOuterContainers=False
        for joint in self.joints:
            if index > 0:
                niceJointName = utils.stripAllNamespaces(joint)[1]
                self.publishNameToModuleContainer(joint+".rotate", niceJointName+"_R", publishToOuterContainers=False)
                publishToOuterContainers=False
                
            index += 1
            
        self.publishNameToModuleContainer(moduleGrp+".lod", "Control_LOD")
        self.publishNameToModuleContainer(moduleGrp+".iconScale", "Icon_Scale")
        self.publishNameToModuleContainer(moduleGrp+".overrideColor", "Icon_Color")
        self.publishNameToModuleContainer(moduleGrp+".visibility", "Vis")
        self.publishNameToModuleContainer(moduleGrp+".visibility", "Vis", publishToOuterContainers=False)
        
        return (self.joints, moduleGrp, self.moduleContainer)
             
    #Hook all joints into a weight attr that gets wired into blueprint joints.
        
    def duplicateAndRenameCreationPose(self):
        joints = cmds.duplicate(self.blueprintNamespace+":creationPose_joints_grp", renameChildren=True)
        
        for i in range(len(joints)):
            nameSuffix = joints[i].rpartition("creationPose_")[2]
            joints[i] = cmds.rename(joints[i], self.blueprintNamespace+":"+self.moduleNamespace+":"+nameSuffix)
            
        return joints
    
    def setupBlueprintWeightBasedBlending(self):
        settingsLocator = self.blueprintNamespace+":SETTINGS"
        
        attributes = cmds.listAttr(settingsLocator, keyable=False)
        weightAttributes = []
        for attr in attributes:
            if attr.find("_weight") != -1:
                weightAttributes.append(attr)
                
        value = 0
        if len(weightAttributes) == 0:
            value = 1
            cmds.setAttr(settingsLocator+".creationPoseWeight", 0)
            
        cmds.select(settingsLocator)
        weightAttributeName = self.moduleNamespace + "_weight"
        cmds.addAttr(ln=weightAttributeName, at="double", min=0, max=1, defaultValue=value, keyable=False)
        
        cmds.container(self.blueprintNamespace+":module_container", edit=True, publishAndBind=[settingsLocator+"."+weightAttributeName, weightAttributeName])
        
        currentEntries = cmds.attributeQuery("activeModule", n=settingsLocator, listEnum=True)
        
        newEntry = self.moduleNamespace
        
        if currentEntries[0] == "None":
            cmds.addAttr(settingsLocator+".activeModule", edit=True, enumName=newEntry)
            cmds.setAttr(settingsLocator+".activeModule", 0)
        else:
            cmds.addAttr(settingsLocator+".activeModule", edit=True, enumName=currentEntries[0]+":"+newEntry)
            
        utilityNodes = []
        for i in range(1, len(self.joints)):
            joint = self.joints[i]
            
            nameSuffix = utils.stripAllNamespaces(joint)[1]
            blueprintJoint = self.blueprintNamespace+":blueprint_"+nameSuffix
            weightNodeAttr = settingsLocator+"."+weightAttributeName
            
            if i < len(self.joints) -1 or len(self.joints) == 2:
                multiplyRotations = cmds.shadingNode("multiplyDivide", n=joint+"_multiplyRotationsWeight", asUtility=True)
                utilityNodes.append(multiplyRotations)
                cmds.connectAttr(joint+".rotate", multiplyRotations+".input1", force=True)
                
                
                for attr in ["input2X", "input2Y", "input2Z"]:
                    cmds.connectAttr(weightNodeAttr, multiplyRotations+"."+attr, force=True)
                    
                index = utils.findFirstFreeConnection(blueprintJoint+"_addRotations.input3D")
                cmds.connectAttr(multiplyRotations+".output", blueprintJoint+"_addRotations.input3D[" + str(index) + "]")
                
            if i == 1:
                addNode = blueprintJoint+"_addTranslate"
                if cmds.objExists(addNode):
                    multiplyTranslation = cmds.shadingNode("multiplyDivide", n=joint+"_multiplyTranslationWeight", asUtility=True)
                    utilityNodes.append(multiplyTranslation)
                    
                    cmds.connectAttr(joint+".translate", multiplyTranslation+".input1", force=True)
                    for attr in ["input2X", "input2Y", "input2Z"]:
                        cmds.connectAttr(weightNodeAttr, multiplyTranslation+"."+attr, force=True)
                        
                    index = utils.findFirstFreeConnection(addNode+".input3D")
                    cmds.connectAttr(multiplyTranslation+".output", addNode+".input3D["+str(index)+"]", force=True)
                    
                addNode = blueprintJoint+"_addScale"
                #I am removing the following lines to eliminate scale for now.
                if cmds.objExists(addNode):
                    multiplyScale = cmds.shadingNode("multiplyDivide", n=joint+"_multiplyScaleWeight", asUtility=True)
                    utilityNodes.append(multiplyScale)
                    
                    cmds.connectAttr(joint+".scale", multiplyScale+".input1", force=True)
                    for attr in ["input2X", "input2Y", "input2Z"]:
                        cmds.connectAttr(weightNodeAttr, multiplyScale+"."+attr, force=True)
                        
                    index = utils.findFirstFreeConnection(addNode+".input3D")
                    cmds.connectAttr(multiplyScale+".output", addNode+".input3D["+str(index)+"]", force=True)
                    
                       
            else:
                multiplyTranslation = cmds.shadingNode("multiplyDivide", n=joint+"_multiplyTranslationWeight", asUtility=True)
                utilityNodes.append  (multiplyTranslation)
                
                cmds.connectAttr(joint+".translateX", multiplyTranslation+".input1X", force=True)
                cmds.connectAttr(weightNodeAttr, multiplyTranslation+".input2X", force=True)
                
                addNode = blueprintJoint+"_addTx"
                index = utils.findFirstFreeConnection(addNode+".input1D")
                cmds.connectAttr(multiplyTranslation+".outputX", addNode+".input1D[" + str(index) + "]", force=True)
                
        return utilityNodes
    
    
    def setupModuleVisibility(self, moduleGrp):
        cmds.select(moduleGrp, replace=True)
        cmds.addAttr(at="byte", defaultValue=1, minValue=0, softMaxValue=3, longName="lod", k=True )
        
        moduleVisibilityMultiply = self.characterNamespaceOnly+":moduleVisibilityMultiply"
        cmds.connectAttr(moduleVisibilityMultiply+".outputX", moduleGrp+".visibility", force=True)
                
                 
    # Wrapper function to publish names to container
    def publishNameToModuleContainer(self, attribute, attributeNiceName, publishToOuterContainers=True):
        if self.moduleContainer == None:
            return
        
        blueprintName = utils.stripLeadingNamespace(self.blueprintNamespace)[1].partition("__")[2]
        
        attributePrefix = blueprintName + "_" + self.moduleNamespace + "_"
        publishedName = attributePrefix + attributeNiceName
        if publishToOuterContainers:
            self.publishedNames.append(publishedName)
            
        cmds.container(self.moduleContainer, edit=True, publishAndBind=[attribute, publishedName])
        
   
    def install_finalize(self):
        self.publishModuleContainerNamesToOuterContainers()
        
        cmds.setAttr(self.blueprintNamespace+":blueprint_joints_grp.controlModulesInstalled", True)
        
        characterContainer = self.characterNamespaceOnly+":character_container"
        blueprintContainer = self.blueprintNamespace+":module_container"
        containers=[characterContainer, blueprintContainer, self.moduleContainer ]
        for c in containers:
            cmds.lockNode(c, lock=True, lockUnpublished=True)
        
    def publishModuleContainerNamesToOuterContainers(self):
        if self.moduleContainer == None:
            return
        
        characterContainer = self.characterNamespaceOnly+":character_container"
        blueprintContainer = self.blueprintNamespace+":module_container"
        
        for publishedName in self.publishedNames:
            outerPublishedNames = cmds.container(blueprintContainer, q=True, publishName=True)
            if publishedName in outerPublishedNames:
                continue
            
            cmds.container(blueprintContainer, edit=True, publishAndBind=[self.moduleContainer+"."+publishedName, publishedName])
            cmds.container(characterContainer, edit=True, publishAndBind=[blueprintContainer+"."+publishedName, publishedName])
    # 161       
    def uninstall(self):
        characterContainer = self.characterNamespaceOnly + ":character_container"
        blueprintContainer = self.blueprintNamespace + ":module_container"
        moduleContainer = self.moduleContainer
        
        # Unlock containers
        containers = [ characterContainer, blueprintContainer, moduleContainer]
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
            
        containers.pop()
        
        blueprintJointsGrp = self.blueprintNamespace + ":blueprint_joints_grp"
        blueprintJoints = utils.findJointChain(blueprintJointsGrp)
        blueprintJoints.pop(0)
        
        settingsLocator = self.blueprintNamespace+":SETTINGS"
        
        connections = cmds.listConnections(blueprintJoints[0]+"_addRotations", source=True, destination=False)
        if len(connections) == 2:
            cmds.setAttr(blueprintJointsGrp+".controlModulesInstalled", False)
            
        publishedNames = cmds.container(moduleContainer, q=True, publishName=True)
        publishedNames.sort()
        
        for name in publishedNames:
            outerPublishedNames = cmds.container(characterContainer, q=True, publishName=True)
            if name in outerPublishedNames:
                cmds.container(characterContainer, edit=True, unbindAndUnpublish=blueprintContainer+"."+name) 
                cmds.container(blueprintContainer, edit=True, unbindAndUnpublish=moduleContainer+"."+name)    
                
        cmds.delete(moduleContainer)
        
        weightAttributeName = self.moduleNamespace +"_weight"
        cmds.deleteAttr(settingsLocator+"."+weightAttributeName)
        
        attributes = cmds.listAttr(settingsLocator, keyable=False)
        weightAttributes = []
        for attr in attributes:
            if attr.find("_weight") != -1:
                weightAttributes.append(attr)
        
        totalWeight = 0
        for attr in weightAttributes:        
            totalWeight += cmds.getAttr(settingsLocator+"."+attr)
            
        cmds.setAttr(settingsLocator+".creationPoseWeight", 1-totalWeight)
        
        currentEntries = cmds.attributeQuery("activeModule", n=settingsLocator, listEnum=True)
        currentEntriesList = currentEntries[0].split(":")
        
        ourEntry = self.moduleNamespace
        
        currentEntriesString = ""
        for entry in currentEntriesList:
            if entry != ourEntry:
                currentEntriesString += entry + ":"
                
        if currentEntriesString == "":
            currentEntriesString = "None"
            
        cmds.addAttr(settingsLocator+".activeModule", edit=True, enumName=currentEntriesString)
        
        cmds.setAttr(settingsLocator+".activeModule", 0)
        
        cmds.namespace(setNamespace=self.blueprintNamespace)
        cmds.namespace(removeNamespace=self.moduleNamespace)
        cmds.namespace(setNamespace=":")
        
        for c in containers:
            cmds.lockNode(c, lock=True, lockUnpublished=True)
            
    # 163
    def duplicateControlModule(self, withAnimation=True):
        # Unlock containers
        characterContainer = self.characterNamespaceOnly + ":character_container"
        blueprintContainer = self.blueprintNamespace + ":module_container"
        moduleContainer = self.moduleContainer
        
        containers = [ characterContainer, blueprintContainer, moduleContainer]
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
            
        # Find all the animation nodes and determine which are user created, space switch, etc.
        cmds.namespace(setNamespace=self.blueprintNamespace + ":" + self.moduleNamespace)
        allAnimationNodes = cmds.namespaceInfo(listOnlyDependencyNodes=True)
        # Get all the animation curves
        allAnimationNodes = cmds.ls(allAnimationNodes, type="animCurve")
        
        # Find all contained animation  nodes
        containedAnimationNodes = cmds.container(moduleContainer, q=True, nodeList=True)
        containedAnimationNodes = cmds.ls(containedAnimationNodes, type="animCurve")
        
        animationNodes = []
        spaceSwitchAnimationNodes = []
        
        for node in allAnimationNodes:
            if not node in containedAnimationNodes:
                animationNodes.append(node)
            else:
                if node.rpartition("_")[2] == "currentSpace":
                    spaceSwitchAnimationNodes.append(node)
        # Set namespace back to Root           
        cmds.namespace(setNamespace=":")
        
        utils.addNodeToContainer(moduleContainer, animationNodes)
        
        # Create temp namespace to duplicate nodes into.
        cmds.namespace(addNamespace="TEMP")
        cmds.namespace(setNamespace="TEMP")
        # Duplicate the entire module container
        cmds.duplicate(moduleContainer, inputConnections=True)
        
        cmds.namespace(setNamespace=":"+self.blueprintNamespace)
        moduleNamespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        
        baseModuleNamespace = self.moduleNamespace.rpartition("_")[0] + "_"
        baseNamespace = self.blueprintNamespace + ":" + baseModuleNamespace
        
        highestSuffix = utils.findHighestTrailingNumber(moduleNamespaces, baseNamespace)
        highestSuffix += 1
        
        newModuleNamespace = baseModuleNamespace + str(highestSuffix)
        # Add the new module namespace and set the default namespace back to root.
        cmds.namespace(addNamespace=newModuleNamespace)
        cmds.namespace(setNamespace=":")
        
        cmds.namespace(moveNamespace=["TEMP", self.blueprintNamespace+":"+newModuleNamespace])
        cmds.namespace(removeNamespace="TEMP")
        
        oldModuleNamespace = self.moduleNamespace
        self.moduleNamespace = newModuleNamespace
        
        newModuleContainer = self.blueprintNamespace + ":" + self.moduleNamespace + ":module_container"
        utils.addNodeToContainer(blueprintContainer, newModuleContainer)
        
        # Generate a publish name list.  Name of the attribute on the container and the name of the attribute it is driving.
        publishedNameList = []
        
        publishedNames = cmds.container(newModuleContainer, q=True, publishName=True)
        
        for name in publishedNames:
            drivenAttribute = cmds.connectionInfo(newModuleContainer+"."+name, getExactSource=True)
            publishedNameList.append( (name, drivenAttribute) )
            
        # Now loop through the attribute names and rename the names on the container.
        #unbind the attributes on the new container.
        #  This seems to be failing on the first .visibility attribute.  A maya command error is returned. 
        #  I am adding a try so I can get past this for now.  No fing clue why I error out.
        
        for name in publishedNameList:
            try:          
                cmds.container(newModuleContainer, edit=True, unbindAndUnpublish=name[1])
            
                nameInfo = name[0].partition(oldModuleNamespace)
                newName = nameInfo[0] + self.moduleNamespace + nameInfo[2]
            
                # Now that we have the new attribute name, publish that name to our container.
            
                cmds.container(newModuleContainer, edit=True, publishAndBind=[name[1], newName])
            except: pass

                   
        self.moduleContainer = moduleContainer
        oldPublishedNames = self.findAllNamesPublishedToOuterContainers()
        newPublishedNames = []
        
        for name in oldPublishedNames:
            nameInfo = name.partition(oldModuleNamespace)
            newPublishedNames.append( (nameInfo[0] + self.moduleNamespace + nameInfo[2]))
        
        # Loop through and publish attributes to outer container.
        self.publishedNames = list(newPublishedNames)
        self.moduleContainer = newModuleContainer
        self.publishModuleContainerNamesToOuterContainers() 
        
        deleteNodes = []
        
        moduleJointsGrp = self.blueprintNamespace+":"+self.moduleNamespace+":joints_grp"
        self.joints = utils.findJointChain(moduleJointsGrp)
        
        for joint in self.joints:
            if cmds.objExists(joint+"_multiplyRotationsWeight"):
                deleteNodes.append(joint+"_multiplyRotationsWeight") 
            
            if cmds.objExists(joint+"_multiplyTranslationWeight"):
                deleteNodes.append(joint+"_multiplyTranslationWeight")\
                
            if cmds.objExists(joint+"_multiplyScaleWeight"):
                deleteNodes.append(joint+"_multiplyScaleWeight")
                
        cmds.delete(deleteNodes, inputConnectionsAndNodes=False)
        
        utilityNodes = self.setupBlueprintWeightBasedBlending()
        utils.addNodeToContainer(newModuleContainer, utilityNodes)
                
        
        
    def findAllNamesPublishedToOuterContainers(self):
        # Look at the top node container to find the names of all published attributes
        if self.moduleContainer == None:
            return []
        
        blueprintContainer = self.blueprintNamespace + ":module_container"
        
        modulePublishedNames = cmds.container(self.moduleContainer, q=True, publishName=True)
        blueprintPublishedNames = cmds.container(blueprintContainer, q=True, publishName=True)
        
        returnPublishedNames = []
        for name in modulePublishedNames:
            if name in blueprintPublishedNames:
                returnPublishedNames.append(name)
                
        return returnPublishedNames
        
        
                
        
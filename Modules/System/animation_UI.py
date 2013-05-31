import maya.cmds as cmds

import maya.mel as mel

import os
from functools import partial

import System.utils as utils

import System.controlObject as controlObject

import System.animationToolUtils as animUtils

class Animation_UI:
    def __init__(self):
        # Setup the scene the Turbine way
        utils.sceneSetup(self)
        
        self.previousBlueprintListEntry = None
        self.previousBlueprintModule = None
        self.previousAnimationModule = None
        
        baseIconsDir = os.environ["GEPPETTO"] + "/Icons/"
        
        self.selectedCharacter = self.findSelectedCharacter()
        
        if self.selectedCharacter == None:
            return
        
        self.characterName = self.selectedCharacter.partition("__")[2]
        
        self.windowName = self.characterName + "_window"
        
        self.UIElements = {}
        
        if cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName)
            
        self.windowWidth = 420
        self.windowHeight = 730
        
        self.UIElements["window"] = cmds.window(self.windowName, width=self.windowWidth, height=self.windowHeight, title = "Animation UI: " + self.characterName, sizeable=False)
       
        self.UIElements["topColumnLayout"] = cmds.columnLayout(adj=True, rs=3)
        
        buttonWidth = 32
        columnOffset = 5
        buttonColumnWidth = buttonWidth + (2*columnOffset)
        textScrollWidth = (self.windowWidth - buttonColumnWidth - 8) /2
        
        self.UIElements["listBoxRowLayout"] = cmds.rowLayout(nc=3, columnWidth3=[textScrollWidth, textScrollWidth, buttonColumnWidth], columnAttach=([1, "both", columnOffset], [2, "both", columnOffset], [3, "both", columnOffset]))
        
        self.UIElements["blueprintModule_textScroll"] = cmds.textScrollList(numberOfRows=12, allowMultiSelection=False, selectCommand=self.refreshAnimationModuleList)
        self.initialiseBlueprintModuleList()
        
        self.UIElements["animationModule_textScroll"] = cmds.textScrollList(numberOfRows=12, allowMultiSelection=False, selectCommand=self.setupModuleSpecificControls)
        
        self.UIElements["buttonColumnLayout"] = cmds.columnLayout()
   
        #self.UIElements["pinButton"] = cmds.symbolCheckBox(onImage=baseIconsDir+"_pinned.bmp", offImage=baseIconsDir+"_unpinned.bmp", width=buttonWidth, height=buttonWidth, onCommand=self.deleteScriptJob, offCommand=self.setupScriptJob)

        self.UIElements["zeroModulesButton"] = cmds.symbolButton(image=baseIconsDir+"_zeroPose.bmp", width=buttonWidth, height=buttonWidth, enable=False,  annotation='Set all Animation Controls %100 to the Creation Pose', c=self.zeroModWeightsA)
 
        #if cmds.objExists(self.selectedCharacter+":non_blueprint_grp"):
            #value = cmds.getAttr(self.selectedCharacter+":non_blueprint_grp.display")
            #self.UIElements["nonBlueprintVisibility"] = cmds.symbolCheckBox(image=baseIconsDir+"_geoVis.bmp", width=buttonWidth, height=buttonWidth, onCommand=self.toggleNonBlueprintVisibility, offCommand=self.toggleNonBlueprintVisibility)
            
        value = cmds.getAttr(self.selectedCharacter + ":character_grp.animationControlVisibility")
        self.UIElements["animControlVisibility"] = cmds.symbolCheckBox(image=baseIconsDir+"_ctrlVis.bmp", width=buttonWidth, height=buttonWidth, onCommand=self.toggleAnimControlVisibility, annotation='Hide all Animation Controls', offCommand=self.toggleAnimControlVisibility)
        
        self.UIElements["deleteModuleButton"] = cmds.symbolButton(image=baseIconsDir+"_shelf_delete.bmp", width=buttonWidth, height=buttonWidth, enable=False,  annotation='Delete an Animation Module', c=self.deleteSelectedModule)        
        self.UIElements["duplicateModuleButton"] = cmds.symbolButton(image=baseIconsDir+"_duplicate.bmp", width=buttonWidth, height=buttonWidth, enable=False,  annotation='Duplicate an Animation Module', c=self.duplicateSelectedModule)
        
        cmds.setParent(self.UIElements["topColumnLayout"])        
        
        cmds.separator()
        
        # 159 >
        self.UIElements["activeModuleColumn"] = cmds.columnLayout(adj=True)
        self.setupActiveModuleControls()
        
        cmds.setParent(self.UIElements["topColumnLayout"])
        cmds.separator()
        
        self.UIElements["matchingButton"] = cmds.button(label="Match Controls to Result",   annotation='This is the FK/IK Switch', enable=False)
        
        cmds.separator()
        # < 159
        # 175 >
        # Setup space switching UI
        self.UIElements["spaceSwitchingColumn"] = cmds.columnLayout(adj=True)
        self.setupSpaceSwitchingControls()
        
        cmds.setParent(self.UIElements["topColumnLayout"])
        cmds.separator()
        
        # < 175 
        
        cmds.rowColumnLayout(nr=1, rowAttach=[1, "both", 0], rowHeight=[1, self.windowHeight-395])        
        self.UIElements["moduleSpecificControlsScroll"] = cmds.scrollLayout(hst=0)        
        scrollWidth = cmds.scrollLayout(self.UIElements["moduleSpecificControlsScroll"], q=True, scrollAreaWidth=True)
        self.UIElements["moduleSpecificControlsColumn"] = cmds.columnLayout(columnWidth=scrollWidth+300, columnAttach=["both", 5])
              
        self.refreshAnimationModuleList()
        
        self.setupScriptJob()
        
        # Shows a new window for each character.  Tab these?
        #cmds.showWindow (self.UIElements["window"])
        
        #pane1 = cmds.paneLayout( configuration='single', parent=self.UIElements["window"])

        #allowedAreas = ['right', 'left']
        
        #cmds.dockControl( area='left', content=self.UIElements["window"], allowedArea=allowedAreas, l="AnimationUI")
        cmds.showWindow(self.windowName)
        self.selectionChanged()
        
        
    def initialiseBlueprintModuleList(self):
        cmds.namespace(setNamespace=self.selectedCharacter)
        blueprintNamespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        cmds.namespace(setNamespace=":")
        # Dictionary containing full names of blueprint modules
        self.blueprintModules = {}
        
        if len(blueprintNamespaces) > 0:
            for namespace in blueprintNamespaces:
                blueprintModule = utils.stripLeadingNamespace(namespace)[1]
                
                """ Add in to modify name displayed in module scroll list """
                #uSpecNameA = blueprintModule.partition("__")[0]
                #uSpecNameB = blueprintModule.partition("__")[2]
                #userSpecifiedName = (uSpecNameA + "_" + uSpecNameB)
                userSpecifiedName = blueprintModule.partition("__")[2]
                cmds.textScrollList(self.UIElements["blueprintModule_textScroll"], edit=True, append=userSpecifiedName)
                self.blueprintModules[userSpecifiedName] = namespace
                
        cmds.textScrollList(self.UIElements["blueprintModule_textScroll"], edit=True, selectIndexedItem=1)
        selectedBlprnModule = cmds.textScrollList(self.UIElements["blueprintModule_textScroll"], q=True, selectItem=True)
        self.selectedBlueprintModule = self.blueprintModules[selectedBlprnModule[0]]       
            
        
    def refreshAnimationModuleList(self, index=1):
        cmds.textScrollList(self.UIElements["animationModule_textScroll"], edit=True, removeAll=True)
        
        cmds.symbolButton(self.UIElements["deleteModuleButton"], edit=True, enable=False)
        cmds.symbolButton(self.UIElements["duplicateModuleButton"], edit=True, enable=False)
        
        selectedBlprnModule = cmds.textScrollList(self.UIElements["blueprintModule_textScroll"], q=True, selectItem=True)
        self.selectedBlueprintModule = self.blueprintModules[selectedBlprnModule[0]]
        
        self.setupActiveModuleControls()
        
        cmds.namespace(setNamespace=self.selectedBlueprintModule)
        controlModuleNamespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        cmds.namespace(setNamespace=":")
        
        if controlModuleNamespaces != None:
            for module in controlModuleNamespaces:
                moduleName = utils.stripAllNamespaces(module)[1]
                cmds.textScrollList(self.UIElements["animationModule_textScroll"], edit=True, append=moduleName)
                
            cmds.textScrollList(self.UIElements["animationModule_textScroll"], edit=True, selectIndexedItem = index)
            
            cmds.symbolButton(self.UIElements["deleteModuleButton"], edit=True, enable=True)
            cmds.symbolButton(self.UIElements["duplicateModuleButton"], edit=True, enable=True)
            cmds.symbolButton(self.UIElements["zeroModulesButton"], edit=True, enable=True)
         
        self.setupModuleSpecificControls()    
        self.previousBlueprintListEntry = selectedBlprnModule
        
        
    def findSelectedCharacter(self):
        selection = cmds.ls(selection=True, transforms=True)
        character = None
        
        if len(selection) > 0:
            selected = selection[0]
            selectedNamespaceInfo = utils.stripLeadingNamespace(selected)
            
            if selectedNamespaceInfo != None:
                selectedNamespace = selectedNamespaceInfo[0]
                
                if selectedNamespace.find("Character__") == 0:
                    character = selectedNamespace
        
        return character
    
    
    def toggleNonBlueprintVisibility(self, *args):
        visibility = not cmds.getAttr(self.selectedCharacter + ":non_blueprint_grp.display")
        cmds.setAttr(self.selectedCharacter + ":non_blueprint_grp.display", visibility)
               
    def toggleAnimControlVisibility(self, *args):
        visibility = not cmds.getAttr(self.selectedCharacter + ":character_grp.animationControlVisibility")
        cmds.setAttr(self.selectedCharacter + ":character_grp.animationControlVisibility", visibility)
        
    def setupScriptJob(self, *args):
        self.scriptJobNum = cmds.scriptJob(parent=self.UIElements["window"], event=["SelectionChanged", self.selectionChanged])
        
    def deleteScriptJob(self, *args):
        cmds.scriptJob(kill = self.scriptJobNum)
    
    # I think this may not be working.    
    def selectionChanged(self):
        """  I need to add a check in case no selection exists"""
        selection = cmds.ls(selection=True, transforms=True)
        if len(selection) > 0:
            selectedNode = selection[0]
            
            characterNamespaceInfo = utils.stripLeadingNamespace(selectedNode)    
            if characterNamespaceInfo != None and characterNamespaceInfo[0] == self.selectedCharacter:
                blueprintNamespaceInfo = utils.stripLeadingNamespace(characterNamespaceInfo[1])
                
                if blueprintNamespaceInfo != None:
                    listEntry = blueprintNamespaceInfo[0].partition("__")[2]
                    allEntries = cmds.textScrollList(self.UIElements["blueprintModule_textScroll"], q=True, allItems=True)
                    
                    if listEntry in allEntries:
                        cmds.textScrollList(self.UIElements["blueprintModule_textScroll"], edit=True, selectItem=listEntry)
                        
                        if listEntry != self.previousBlueprintListEntry:
                            self.refreshAnimationModuleList()
                            
                        moduleNamespaceInfo = utils.stripLeadingNamespace(blueprintNamespaceInfo[1])
                        if moduleNamespaceInfo != None:
                            allEntries = cmds.textScrollList(self.UIElements["animationModule_textScroll"], q=True, allItems=True)
                            if moduleNamespaceInfo[0] in allEntries:
                                cmds.textScrollList(self.UIElements["animationModule_textScroll"], edit=True, selectItem=moduleNamespaceInfo[0])
                                
        self.setupModuleSpecificControls()
        self.setupSpaceSwitchingControls()
                                
   #159
   # Grab all controls in active module control column.  Delete and re-create for the active control.
    def setupActiveModuleControls(self): 
        existingControls = cmds.columnLayout(self.UIElements["activeModuleColumn"], q=True, childArray=True)
        if existingControls != None:
           cmds.deleteUI(existingControls)
           
        cmds.setParent(self.UIElements["activeModuleColumn"])
        
        largeButtonSize = 100
        enumOptionWidth = self.windowWidth - 2*largeButtonSize
        
        self.settingsLocator = self.selectedBlueprintModule + ":SETTINGS"
        activeModuleAttribute = self.settingsLocator + ".activeModule"
        
        currentEntries = cmds.attributeQuery("activeModule", n=self.settingsLocator, listEnum=True)
        enable = True
        if currentEntries[0] == "None":
            enable=False
            
        self.UIElements["activeModule_rowLayout"] = cmds.rowLayout(nc=3, adjustableColumn=1, ct3=("both", "both", "both"), cw3= (enumOptionWidth, largeButtonSize, largeButtonSize))
        
        attributes = cmds.listAttr(self.settingsLocator, keyable=False)
        weightAttributes = []
        for attr in attributes:
            if attr.find("_weight") != -1:
                weightAttributes.append(attr)
                
        self.UIElements["activeModule"] = cmds.attrEnumOptionMenu(label="Active Module", width=enumOptionWidth, attribute=activeModuleAttribute, changeCommand=partial(self.activeModule_enumCallback, weightAttributes), enable=enable)
        self.UIElements["keyModuleWeights"] = cmds.button(label= "Key All", c=partial(self.keyModuleWeights, weightAttributes), annotation='Key Control Switching', enable=enable)
        self.UIElements["graphModuleWeights"] = cmds.button(label="Graph Weights", c=self.graphModuleWeights, enable=enable)
        
        cmds.setParent(self.UIElements["activeModuleColumn"])
        
        self.UIElements["moduleWeights_frameLayout"] = cmds.frameLayout(collapsable=True, collapse=False, label="Module Weights", height=100, collapseCommand = self.moduleWeight_UICollapse, expandCommand=self.moduleWeight_UIExpand)
        cmds.scrollLayout(hst=0)
        cmds.columnLayout(adj=True)
        
        cmds.attrFieldSliderGrp(at=self.settingsLocator+".creationPoseWeight", enable=False)
        cmds.separator
        
        for attr in weightAttributes:
            self.UIElements[attr] = cmds.floatSliderGrp(label=attr, field=True, precision=4, minValue=0.0, maxValue=1.0, value=cmds.getAttr(self.settingsLocator+"."+attr), cc=partial(self.moduleWeights_sliderCallback, attr, weightAttributes))
        
        parentUIElements = self.UIElements["moduleWeights_frameLayout"]
        self.create_moduleWeightsScriptJob(parentUIElements, weightAttributes)
        
        self.moduleWeights_updateMatchingButton()
        
    # Collapse weights down and resize window  
    def moduleWeight_UICollapse(self, *args):
        cmds.window(self.UIElements["window"], edit=True, height=self.windowHeight -80)
        
    def moduleWeight_UIExpand(self, *args):
        cmds.window(self.UIElements["window"], edit=True, height=self.windowHeight)
        
    def activeModule_enumCallback(self, weightAttributes, *args):
        enumValue = args[0]
        
        for attr in weightAttributes:
            value = 0
            if enumValue+"_weight" == attr:
                value = 1
                
            cmds.setAttr(self.settingsLocator+"."+attr, value)
            
        cmds.setAttr(self.settingsLocator+".creationPoseWeight", 0)
        self.moduleWeights_timeUpdateScriptJobCallback(weightAttributes)
        self.moduleWeights_updateMatchingButton()
        
    """ Trying to use activeModule_enumCallback to iterate through all controls in the scene."""
        
    def moduleWeights_sliderCallback(self, controlledAttribute, weightAttributes, *args):
        value = float(args[0])
        currentTotalWeight = 0.0
        
        for attribute in weightAttributes:
            if attribute != controlledAttribute:
                currentTotalWeight += cmds.getAttr(self.settingsLocator+"."+attribute)
                
            if currentTotalWeight + value > 1.0:
                value = 1.0 - currentTotalWeight
                
            cmds.setAttr(self.settingsLocator+"."+controlledAttribute, value)
            cmds.floatSliderGrp(self.UIElements[controlledAttribute], edit=True, value=value)
            
            newTotalWeight = currentTotalWeight + value
            
            creationPoseWeight = 1.0 - newTotalWeight
            cmds.setAttr(self.settingsLocator+".creationPoseWeight", creationPoseWeight)
            
            self.moduleWeights_updateMatchingButton()
                   
    # Script job that accounts for changing time in relation to slider values.
    def create_moduleWeightsScriptJob(self, parentUIElement, weightAttributes):
        cmds.scriptJob(event=["timeChanged", partial(self.moduleWeights_timeUpdateScriptJobCallback, weightAttributes)],parent=parentUIElement )
        
    def moduleWeights_timeUpdateScriptJobCallback(self, weightAttributes):    
        for attr in weightAttributes:
            value = cmds.getAttr(self.settingsLocator + "." + attr)
            cmds.floatSliderGrp(self.UIElements[attr], edit=True, value=value)
            
        self.moduleWeights_updateMatchingButton()
            
    
    # Matching button only active when currently selected module has a weight of 0.   
    def moduleWeights_updateMatchingButton(self):
        currentlySelectedModuleInfo = cmds.textScrollList(self.UIElements["animationModule_textScroll"], q=True, selectItem=True)
        if currentlySelectedModuleInfo != None:
            currentlySelectedModuleNamespace = currentlySelectedModuleInfo[0]
            
            moduleWeightValue = cmds.getAttr(self.settingsLocator+"."+currentlySelectedModuleNamespace+"_weight")
            
            matchButtonEnable = moduleWeightValue == 0
            cmds.button(self.UIElements["matchingButton"], edit=True, enable=matchButtonEnable)
        
        
    def keyModuleWeights(self, weightAttributes, *args):
        for attr in weightAttributes:
            cmds.setKeyframe(self.settingsLocator, at=attr, itt="linear", ott="linear")
            
        cmds.setKeyframe(self.settingsLocator, at="creationPoseWeight", itt="linear", ott="linear")
        
        
    def graphModuleWeights(self, *args):
        cmds.select(self.settingsLocator, replace=True)
        mel.eval("tearOffPanel \"Graph Editor\"graphEditor true")
        
    # 160
    def setupModuleSpecificControls(self):
        currentlySelectedModuleInfo = cmds.textScrollList(self.UIElements["animationModule_textScroll"], q=True, selectItem=True)
        currentlySelectedModuleNamespace = None
        if currentlySelectedModuleInfo != None:
            currentlySelectedModuleNamespace = currentlySelectedModuleInfo[0]
            
            if currentlySelectedModuleNamespace == self.previousAnimationModule and self.selectedBlueprintModule == self.previousBlueprintModule:
                return
            
        existingControls = cmds.columnLayout(self.UIElements["moduleSpecificControlsColumn"], q=True, childArray=True)
        if existingControls != None:
            cmds.deleteUI(existingControls)
            
        cmds.button(self.UIElements["matchingButton"], edit=True, enable=False)
        
        cmds.setParent(self.UIElements["moduleSpecificControlsColumn"])
        
        moduleNameInfo = utils.findAllModuleNames("/Modules/Animation")
        modules = moduleNameInfo[0]
        moduleNames = moduleNameInfo[1]
        
        if currentlySelectedModuleInfo != None:
            currentlySelectedModule = currentlySelectedModuleNamespace.rpartition("_")[0]
            
            if currentlySelectedModule in moduleNames:
                # Matching button enabled?
                # Should that actually be _weight?
                moduleWeightValue = cmds.getAttr(self.selectedBlueprintModule+":SETTINGS."+currentlySelectedModuleNamespace+"_weight")
                matchButtonEnable = moduleWeightValue == 0.0
                
                moduleIndex = moduleNames.index(currentlySelectedModule)
                module = modules[moduleIndex]
                
                cmds.attrControlGrp(attribute=self.selectedBlueprintModule+":"+currentlySelectedModuleNamespace+":module_grp.lod", label="Module_LOD")
                
                mod = __import__("Animation."+module, {}, {}, [module])                
                reload(mod)
                
                moduleClass = getattr(mod, mod.CLASS_NAME)
                
                moduleInst = moduleClass(self.selectedBlueprintModule+":"+currentlySelectedModuleNamespace)
                
                moduleInst.UI(self.UIElements["moduleSpecificControlsColumn"])
                
                # Set parent back to module specific controls layout
                self.UIElements["moduleSpecificControls_preferencesFrame"] = cmds.frameLayout(borderVisible=True, label="preferences", collapsable=True)
                self.UIElements["moduleSpecificControls_preferencesColumn"] = cmds.columnLayout(columnAttach=["both", 5], adj=True)
                
                cmds.attrControlGrp(attribute=self.selectedBlueprintModule+":"+currentlySelectedModuleNamespace+":module_grp.iconScale", label="Icon Scale")
                
                value = cmds.getAttr(self.selectedBlueprintModule+":"+currentlySelectedModuleNamespace+":module_grp.overrideColor")
                self.UIElements["iconColor"] = cmds.colorIndexSliderGrp(label="Icon Color", maxValue=32, v=value, cc=partial(self.iconColor_callback, currentlySelectedModuleNamespace))
                
                moduleInst.UI_preferences(self.UIElements["moduleSpecificControls_preferencesColumn"])
                
                cmds.button(self.UIElements["matchingButton"], edit=True, enable=matchButtonEnable, c=moduleInst.match)
                
            self.previousBlueprintModule = self.selectedBlueprintModule
            self.previousAnimationModule = currentlySelectedModuleNamespace
            
    def iconColor_callback(self, currentlySelectedModuleNamespace, *args):
        value = cmds.colorIndexSliderGrp(self.UIElements["iconColor"], q=True, value=True)
        cmds.setAttr(self.selectedBlueprintModule+":"+currentlySelectedModuleNamespace+":module_grp.overrideColor", value-1)
        
    #162 
    def deleteSelectedModule(self, *args):
        selectedModule = cmds.textScrollList(self.UIElements["animationModule_textScroll"], q=True, selectItem=True)[0]
        selectedModuleNamespace = self.selectedBlueprintModule + ":" + selectedModule
        
        moduleNameInfo = utils.findAllModuleNames("/Modules/Animation")
        modules = moduleNameInfo[0]
        moduleNames = moduleNameInfo[1]
        
        selectedModuleName = selectedModule.rpartition("_")[0]
        
        if selectedModuleName in moduleNames:
            moduleIndex = moduleNames.index(selectedModuleName)
            module = modules[moduleIndex]
            
            mod = __import__("Animation."+module, {}, {}, [module])
            reload(mod)
            
            moduleClass = getattr(mod, mod.CLASS_NAME)
            
            moduleInst = moduleClass(selectedModuleNamespace)
            
            moduleInst.uninstall()
            
            self.refreshAnimationModuleList()
            
    #163
    def duplicateSelectedModule(self, *args):
        self.deleteScriptJob()
        
        result = cmds.confirmDialog(messageAlign="center", title="Duplicate Control Module", message="Duplicate animation as well as controls?", button=["Yes", "No", "Cancel"], defaultButton="Yes", cancelButton="Cancel", dismissString="Cancel")
        
        if result == "Cancel":
            self.setupScriptJob()
            return
        
        duplicateWithAnimation = False
        if result == "Yes":
            duplicateWithAnimation = True
            
            
        selectedModule = cmds.textScrollList(self.UIElements["animationModule_textScroll"], q=True, selectItem=True)[0]
        selectedModuleNamespace = self.selectedBlueprintModule + ":" + selectedModule
        
        moduleNameInfo = utils.findAllModuleNames("/Modules/Animation")
        modules = moduleNameInfo[0]
        moduleNames = moduleNameInfo[1]
        
        selectedModuleName = selectedModule.rpartition("_")[0]
        
        if selectedModuleName in moduleNames:
            moduleIndex = moduleNames.index(selectedModuleName)
            module = modules[moduleIndex]
            
            mod = __import__("Animation."+module, {}, {}, [module])
            reload(mod)
            
            moduleClass = getattr(mod, mod.CLASS_NAME)
            
            moduleInst = moduleClass(selectedModuleNamespace)
            
            selectedIndex = cmds.textScrollList(self.UIElements["animationModule_textScroll"], q=True, selectIndexedItem=True)
            previousSelection = cmds.ls(sl=True)
            
            moduleInst.duplicateControlModule(withAnimation=duplicateWithAnimation)
            # Refresh animation module list
            utils.forceSceneUpdate()
            
            if len(previousSelection) != 0:
                cmds.select(previousSelection, replace=True)
            else:
                cmds.select(clear=True)
                       
            self.refreshAnimationModuleList(index = selectedIndex)
            
        self.setupScriptJob()
        
        
    def setupSpaceSwitchingControls(self):
        existingControls = cmds.columnLayout(self.UIElements["spaceSwitchingColumn"], q=True, childArray=True)
        if existingControls != None:
            cmds.deleteUI(existingControls)
            
        cmds.setParent(self.UIElements["spaceSwitchingColumn"])
        
        largeButtonSize = 80
        smallButtonSize = 35
        
        enumOptionWidth = self.windowWidth -2*(largeButtonSize + smallButtonSize)
        
        enable = False
        selection = cmds.ls(sl=True, transforms=True)
        spaceSwitcher = None
        controlObj = None
        targetObject = None
        
        if len(selection) > 0:
            if cmds.attributeQuery("spaceSwitching", n=selection[0], exists=True):
                enable = True
                controlObj = selection[0]
                spaceSwitcher = selection[0] + "_spaceSwitcher"
                
                if len(selection) > 1:
                    targetObject = selection[1]
                    
            if targetObject == None:
                targetObject = self.selectedBlueprintModule + ":HOOK_IN"
                
            self.UIElements["spaceSwitching_rowLayout"] = cmds.rowLayout(enable=enable, nc=5, adjustableColumn=1, ct5=("both", "both", "both", "both", "both"), cw5=(enumOptionWidth, largeButtonSize, largeButtonSize, smallButtonSize, smallButtonSize))
            
            if enable:
                attribute = spaceSwitcher + ".currentSpace"
                self.UIElements["currentSpace"] = cmds.attrEnumOptionMenu(label="Current Space", width=enumOptionWidth, enable=True, attribute=attribute)
            else:
                self.UIElements["currentSpace"] = cmds.attrEnumOptionMenu(label="Current Space", width=enumOptionWidth, enable=False)
                
            self.UIElements["spaceSwitching_spaceSwitch"] = cmds.button(enable=enable, label="Space Switch", c=partial(self.spaceSwitching_spaceSwitch, controlObj, targetObject))
            self.UIElements["spaceSwitching_deleteKey"] = cmds.button(enable=enable, label="Delete Key", c=partial(self.spaceSwitching_deleteKey, spaceSwitcher))
            self.UIElements["spaceSwitching_backKey"] = cmds.button(enable=enable, label="<", c=partial(self.spaceSwitching_backKey, spaceSwitcher))
            self.UIElements["spaceSwitching_forewardKey"] = cmds.button(enable=enable, label=">", c=partial(self.spaceSwitching_forewardKey, spaceSwitcher))
            
    def spaceSwitching_spaceSwitch(self, controlObj, targetObject, *args):
        controlObjectInstance = controlObject.ControlObject(controlObj)
        controlObjectInstance.switchSpace_UI(targetObject)
        
    def spaceSwitching_deleteKey(self, spaceSwitcher, *args):
        animationNamespace = utils.stripAllNamespaces(spaceSwitcher)[0]
        
        characterContainer = self.selectedCharacter+":character_container"
        blueprintContainer = self.selectedBlueprintModule+":module_container"
        animationContainer = animationNamespace+":module_container"
        
        containers = [characterContainer, blueprintContainer, animationContainer]
        for c in containers:
            cmds.lockNode(c, lock=False, lockUnpublished=False)
            
        cmds.cutKey(spaceSwitcher, at="currentSpace", time=(cmds.currentTime(q=True),))
                       
        for c in containers:
            cmds.lockNode(c, lock=True, lockUnpublished=True)
        
    def spaceSwitching_forewardKey(self, spaceSwitcher, *args):
        currentTime = cmds.currentTime(q=True)
        time = cmds.findKeyframe(spaceSwitcher, at="currentSpace", time=(currentTime,), which="next")
        
        if currentTime < time:
            cmds.currentTime(time)
        
    def spaceSwitching_backKey(self, spaceSwitcher, *args):
        currentTime = cmds.currentTime(q=True)
        time = cmds.findKeyframe(spaceSwitcher, at="currentSpace", time=(currentTime,), which="previous")
        
        if currentTime > time:
            cmds.currentTime(time)
            
    def zeroModWeightsA(self, *args):
        animUtils.zeroModWeights()
               
            
    
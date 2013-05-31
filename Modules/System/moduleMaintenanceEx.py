import maya.cmds as cmds

import System.utils as utils
#reload(utils)

#import System.animationModSettings as animModSettings
#reload(animModSettings)

from functools import partial

class ModuleMaintenanceEx():
    def __init__(self):

        self.UIElements = {}
        
        self.currentBlueprintModule = {}
        
        self.controlModuleCompatibility = self.initializeControlModuleCompatibility()
        
    def initializeControlModuleCompatibility(self):
        print "initializeControlModuleCompatibility 16"
        # Use util function to query all available animation modules
        animationControlModules = utils.findAllModules("/Modules/Animation")
        # Store all compatible animation modules
        moduleList = []
        
        for module in animationControlModules:
            mod = __import__("Animation."+module, {}, {}, [module])

            reload(mod)
            
            moduleClass = getattr(mod, mod.CLASS_NAME)

            moduleInstance = moduleClass(None)
            
            compatibleBlueprintModules = moduleInstance.compatibleBlueprintModules()
            
            moduleList.append( (mod, mod.CLASS_NAME, compatibleBlueprintModules))
        # I put this in as a check
        if moduleList == None:
            print "no animation modules"    
        return moduleList
    
    def setModuleMaintenanceVisibility(self, vis=True):

        characters = utils.findInstalledCharacters()
        
        for c in characters:
            characterContainer = c+":character_container"
            cmds.lockNode(characterContainer, lock=False, lockUnpublished=False)
            
            characterGroup = c+":character_grp"
            cmds.setAttr(characterGroup+".moduleMaintenanceVisibility", vis)
            
            """ tHIS WOULD BE A GOOD TIME TO LOD THE MESH """
            
            cmds.lockNode(characterContainer, lock=True, lockUnpublished=True)
 
            
    def objectSelected(self):
        print "objectSelected 58"
        objects = cmds.ls(selection = True)
        
        cmds.select(clear=True)
        
        """ Find the installed characters """
        characters = utils.findInstalledCharacters()
        
        """ Unlock the containers """
        for character in characters:
            characterContainer = character + ":character_container"
            cmds.lockNode(characterContainer, lock=False, lockUnpublished=False)
            # Find every module installed on that character.
            blueprintInstances = utils.findInstalledBlueprintInstances(character)
            
            for blueprintInstance in blueprintInstances:
                moduleContainer = character+":"+blueprintInstance+":module_container"
                cmds.lockNode(moduleContainer, lock=False, lockUnpublished=False)
                
                """ Do we have modules installed?  If so, set the joint color to blue. """
                blueprintJointsGrp = character+":"+blueprintInstance+":blueprint_joints_grp"
                
                if cmds.getAttr(blueprintJointsGrp+".controlModulesInstalled"):
                    #Blue
                    cmds.setAttr(blueprintJointsGrp+".overrideColor", 6)
                else:
                    cmds.setAttr(blueprintJointsGrp+".overrideColor", 2)
                
                cmds.lockNode(moduleContainer, lock=True, lockUnpublished=True)
                       
            cmds.lockNode(characterContainer, lock=True, lockUnpublished=True)
        
        if len(objects) > 0:
            lastSelected = objects[len(objects)-1]
            
            lastSelected_stripNamespaces = utils.stripAllNamespaces(lastSelected)
                    
            if lastSelected_stripNamespaces != None:
                lastSelected_withoutNamespaces = lastSelected_stripNamespaces[1]
                
                if lastSelected_withoutNamespaces.find("blueprint_") == 0:
                    blueprintModuleNamespace_incCharNamespace = lastSelected_stripNamespaces[0]
                    moduleContainer = blueprintModuleNamespace_incCharNamespace + ":module_container"

                    cmds.select(moduleContainer, replace=True)
                    
                    # set color of the joints
                    characterNamespace = utils.stripLeadingNamespace(lastSelected)[0]
                    
                    characterContainer = characterNamespace + ":character_container"
                    
                    containers = [characterContainer, moduleContainer]
                    for container in containers:
                        cmds.lockNode(container, lock=False, lockUnpublished=False)
                        
                    blueprintJointsGrp = blueprintModuleNamespace_incCharNamespace+":blueprint_joints_grp"
                    #  This was not in the video.  I needed to add this to allow overrides.
                    cmds.setAttr(blueprintJointsGrp+".overrideEnabled", 1)

                    cmds.setAttr(blueprintJointsGrp+".overrideColor", 13)
                                              
                    for container in containers:
                        cmds.lockNode(container, lock=True, lockUnpublished=True)

        self.currentBlueprintModule['currentMod'] = (blueprintModuleNamespace_incCharNamespace)
        print "ModMaintEX cureent bp mod name "
        print self.currentBlueprintModule['currentMod']
        
    def controlModuleSelected(self, animMod, *args):
        print "Control Mod Selected"
        print animMod
        moduleNameInfo = animMod
        if moduleNameInfo == None:
            return
        else:
            moduleName = moduleNameInfo
            
            animMod=None
            for controlModule in self.controlModuleCompatibility:
                print controlModule
                if controlModule[1] == moduleName:
                    print "Yaya"
                    animMod = controlModule[0]
                    self.installModule(animMod, moduleName)
                    
            if animMod != None:
                moduleTitle = animMod.TITLE
                moduleDescription = animMod.DESCRIPTION       
        
    def isModuleInstalled(self, moduleName):
        print "isModuleInstalled 193"
        cmds.namespace(setNamespace=self.currentBlueprintModule)
        installedModules = cmds.namespaceInfo(listOnlyNamespaces=True)
        cmds.namespace(setNamespace=":")
        
        if installedModules != None:
            for module in installedModules:
                installedModuleNameWithSuffix = utils.stripAllNamespaces(module)[1]
                installedModuleName = installedModuleNameWithSuffix.rpartition("_")[0]
                if installedModuleName == moduleName:
                    return True
                
        return False
 
 
                
    def installModule(self, mod, moduleName):
        print "MM Install"
        
        moduleNamespace = self.currentBlueprintModule['currentMod'] + ":" + mod.CLASS_NAME+"_1"

        moduleClass = getattr(mod, mod.CLASS_NAME)

        moduleInstance = moduleClass(moduleNamespace)

        moduleInstance.install()
    
        utils.forceSceneUpdate()
        
        #cmds.select(self.currentBlueprintModule['currentMod'] + ":module_container", replace=True)
                   
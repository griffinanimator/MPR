import maya.cmds as cmds

import System.utils as utils
reload(utils)

import System.moduleMaintenance as modMaint

from ctypes import *

class AnimMod_Info():
    def __init__(self):
        print "In AnimMod_Info"

    def animModInfo(self):
        """ Call on getInstalledAnimModules to get bp mod name, anim mod class
        and anim mod container name"""
        modSets = self.getInstalledAnimModules()
        
        for set in modSets: 
            print set[3]
            animContainer = set[2]
            moduleContainer = set[3]

            animModAttrs = self.getAnimModAttrs(animContainer, moduleContainer)
        
    
    def getInstalledAnimModules(self):
        modSets = []
        
        characters = utils.findInstalledCharacters()
      
        for character in characters:
            characterContainer = character + ":character_container"
            """ Find the blueprints in the scene"""
            blueprintInstances = utils.findInstalledBlueprintInstances(character)
    
            
            for blueprintInstance in blueprintInstances:
                moduleContainer = character+":"+blueprintInstance+":module_container"
               
                """ Do we have animation modules installed? """
                blueprintJointsGrp = character+":"+blueprintInstance+":blueprint_joints_grp"
                
                if cmds.getAttr(blueprintJointsGrp+".controlModulesInstalled"):
                    nodes = cmds.container(moduleContainer, q=True, nl=True)
                    for node in nodes:
                        suffix = ":module_container"  
                        result = node.endswith(suffix)  
                        if result == True:
                            """ The module container holds all the attr info we need to save"""
                            animContainer = node
                            tmpVar = node.rpartition(":module_container")
                            tmpVar = tmpVar[0].rpartition(":")
                            className = tmpVar[2]
                            
                            modSets.append([blueprintInstance, className, animContainer, moduleContainer])
         
                            
        return (modSets) # Contains the bp module name, anim mod class name, anim mod container
                           
    def getAnimModAttrs(self, animContainer, moduleContainer):
        print " IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"
        animContainerAttrs = cmds.listAttr(animContainer)
        for attr in animContainerAttrs:
            """ I want to capture the following attrs """
            targetAttrs = ("Control_LOD", "Icon_Scale", "Icon_Color", "Vis", "stretchiness", "currentSpace", "twistControlOffset")
            for tAttr in targetAttrs:
                result = attr.endswith(tAttr)  
                if result == True:
                    print attr
                    #val = cmds.getAttr(attr)
                    #print val
            
        """ Get the settings locator by replacing :module_container with :SETTINGS """
        settingsLocator = moduleContainer.replace(":module_container", ":SETTINGS")
        
        settingsLocatorAttrs = cmds.listAttr(settingsLocator)
        for attr in settingsLocatorAttrs:
            """ I want to capture the following attrs """
            targetAttrs = ("weight", "creationPoseWeight", "activeModule")
            for tAttr in targetAttrs:
                result = attr.endswith(tAttr)  
                if result == True:
                    print attr
                    #val = cmds.getAttr(attr)
                    #print val
                   
                
    def getAllAnimModules():
        # Use util function to query all available animation modules
        animationControlModules = utils.findAllModules("/Modules/Animation")
        # Store all animation modules
        moduleList = []
            
        for module in animationControlModules:
            mod = __import__("Animation."+module, {}, {}, [module])
    
            moduleClassName = mod.CLASS_NAME
            #print moduleClassName
            
            moduleList.append(moduleClass)
       
        return moduleList            
 
    
 #"Control_LOD", "Icon_Scale", "Icon_Color", "Vis", "stretchiness", "currentSpace", "twistControlOffset"   
 # module_grp   
# creationPoseWeight
# lod
# iconScale
# overrideColor

#"weight", "creationPoseWeight", "activeModule"
  # SETTINGS
# activeModule

                
                
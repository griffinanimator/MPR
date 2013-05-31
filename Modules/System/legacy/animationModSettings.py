import maya.cmds as cmds

import System.utils as utils

import System.moduleMaintenance as modMaint

from ctypes import *

def getInstalledAnimModules():
    modSets = []
    
    characters = utils.findInstalledCharacters()
  
    for character in characters:
        characterContainer = character + ":character_container"

        blueprintInstances = utils.findInstalledBlueprintInstances(character)

        
        for blueprintInstance in blueprintInstances:
            moduleContainer = character+":"+blueprintInstance+":module_container"
            #print moduleContainer
            """ Do we have animation modules installed? """
            blueprintJointsGrp = character+":"+blueprintInstance+":blueprint_joints_grp"
            
            if cmds.getAttr(blueprintJointsGrp+".controlModulesInstalled"):
                #print "This is the group holding the blueprint joints that the animation module is installed on """
                #print blueprintJointsGrp
                nodes = cmds.container(moduleContainer, q=True, nl=True)
                for node in nodes:
                    suffix = ":module_container"  
                    result = node.endswith(suffix)  
                    if result == True:
                        tmpVar = node.rpartition(":module_container")
                        tmpVar = tmpVar[0].rpartition(":")
                        className = tmpVar[2]
                        
                        modSets.append([blueprintInstance, className])
     
                        print (blueprintInstance + " has this anim mod installed " + className)
                        
    print modSets
                       
def getAnimModAttrs():
               
            
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
    
    
    

                
                
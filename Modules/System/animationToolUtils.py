import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils
import System.turbineSpecificUtils as turbineUtils

""" Find containers would be a good general util """
def findAnimContainers():
    # Get the character name frome turbineUtils
    fullCharName = turbineUtils.getCharacterInfo()[2]
    # Find the root character container
    characterContainer = (fullCharName + ":character_container")
    cmds.select(characterContainer)
    
    # Get all the module_containers
    allContainers = []
    containerNodes = cmds.container(characterContainer, q=True, nl=True)
    
    for container in containerNodes:
        selContainer = container.encode("ascii","ignore")
  
        suffix = "module_container"
        
        result = selContainer.endswith(suffix)
        
        if result == True:
            allContainers.append(selContainer)

    return allContainers


def getSettingsLocator():
    allContainers = findAnimContainers()

    allSettingsLocs = []
    for container in allContainers:
         containerNodes = cmds.container(container, q=True, nl=True)
         
         for object in containerNodes:
            selContainer = object.encode("ascii","ignore")
      
            suffix = "SETTINGS"
            
            result = selContainer.endswith(suffix)
            
            if result == True:
                allSettingsLocs.append(selContainer)
    
    return allSettingsLocs

def zeroModWeights():
    allSettingsLocs = getSettingsLocator()

    for loc in allSettingsLocs:
        settingsAttrs = cmds.listAttr(loc, ud=True)
        
        suffix = "_weight"
        
        for setting in settingsAttrs:
        
            result = setting.endswith(suffix)
        
            if result == True:
                cmds.setAttr(loc + "." + setting, 0)
                
            if setting == "creationPoseWeight":
                cmds.setAttr(loc + "." + setting, 1)
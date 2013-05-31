import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.turbineSpecificUtils as turbineUtils

class Container_Utils():
    
    def __init__(self):
        self.containers = {}
        
        try:
            self.characterName = turbineUtils.getCharacterInfo()[0]
            self.characterPrefix = turbineUtils.getCharacterInfo()[2]
            self.exportPrefix = self.characterPrefix.replace('Character__', 'Export__')
        except: pass
        
        """ Run all the functions to collect the container names """
        self.characterContainers() 
        self.blueprintContainers()
        self.animationModContainers()
        self.allContainers()
        
        print self.containers['characterContainer']
        #print self.containers['rigModuleContainer']
        #print self.containers['blueprintContainer']
        #print self.containers['animationModuleContainer'] 
        
        
      
    def characterContainers(self):
        characterContainers = []
        container = (self.characterPrefix + ':character_container')
        characterContainers.append(container)
        self.containers['characterContainer'] = characterContainers
        
    def blueprintContainers(self):
        rigModuleContainers = []
        blueprintContainers = []
        
        """ Find the blueprint modules in the scene"""  
        blueprintInstances = utils.findInstalledBlueprintInstances(self.characterPrefix)
        for blueprint in blueprintInstances:
            
            rigModContainer = (self.characterPrefix + ':' + blueprint + ':module_container')
            blueprintContainer = (self.characterPrefix + ':' + blueprint + ':blueprint_container')

            if cmds.objExists(rigModContainer):
                if rigModContainer not in (rigModuleContainers):
                    rigModuleContainers.append(rigModContainer)
            if cmds.objExists(blueprintContainer):
                if blueprintContainer not in (blueprintContainers):
                    blueprintContainers.append(blueprintContainer)

        self.containers['rigModuleContainer'] = rigModuleContainers
        self.containers['blueprintContainer'] = blueprintContainers
        
    def blueprintJointGrps(self, container):
        blueprintJointsGrp = container.replace(':module_container', ':blueprint_joints_grp')
            
        return blueprintJointsGrp

        
    def animationModContainers(self):
        animModContainers = []
        for container in self.containers['rigModuleContainer']:
            blueprintJointsGrp = self.blueprintJointGrps(container)
            if cmds.getAttr(blueprintJointsGrp+".controlModulesInstalled"):
                nodes = cmds.container(container, q=True, nl=True)                
                for node in nodes:
                    suffix = ":module_container"  
                    result = node.endswith(suffix)  
                    if result == True: 
                        if node not in (animModContainers):
                            animModContainers.append(node)        
        self.containers['animationModuleContainer'] = animModContainers
        
    def allContainers(self):
        containers = []
        container = self.containers['characterContainer']
        for each in container:
            containers.append(each)
        container = self.containers['rigModuleContainer']
        for each in container:
            containers.append(each)
        container = self.containers['blueprintContainer']
        for each in container:
            containers.append(each)
        container = self.containers['animationModuleContainer'] 
        for each in container:
            containers.append(each)
            
        self.containers['allContainers'] = containers
            
    def lockContainers(self, containers):
        for each in containers:
            cmds.lockNode(each, l=True, lu=True)
            print (each + ' container locked')
            
    def unlockContainers(self, containers):
        for each in containers:
            cmds.lockNode(each, l=False, lu=False)
            print (each + ' container unlocked')
            
    def unlockAllContainers(self):
        self.unlockContainers(self.containers['characterContainer'])
        self.unlockContainers(self.containers['rigModuleContainer'])
        self.unlockContainers(self.containers['blueprintContainer'])
        self.unlockContainers(self.containers['animationModuleContainer'])
        
        
    def lockAllContainers(self):
        self.lockContainers(self.containers['animationModuleContainer'])
        self.lockContainers(self.containers['blueprintContainer'])
        self.lockContainers(self.containers['rigModuleContainer'])
        self.lockContainers(self.containers['characterContainer'])
        
       
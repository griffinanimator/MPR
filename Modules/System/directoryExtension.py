import maya.cmds as cmds
import os

#from tap.core.maya.utility import Path

import System.turbineSpecificUtils as turbineUtils

import __main__
class DirectoryExtension():
    
    artPath = "Z:/art/"
    print "This is self.artPath"
    print artPath
    
    def __init__(self):
        """ Get the ArtPath """
        

        self.paths = {}
        
        self.characterName = 'Character__tmp'
       
        # Use the character name to determine the name of the setup node
        try:
            self.characterName = turbineUtils.getCharacterInfo()[0]
            self.characterPrefix = turbineUtils.getCharacterInfo()[2]
            self.exportPrefix = self.characterPrefix.replace('Character__', 'Export__')
        except: pass
     
        self.paths = {}
       
        """ Set the path to the animLib """
        self.paths['animLib'] = (self.artPath + "/character/GEPPETTO/Animation/animLib/")
        self.paths['userRigSetting'] = (self.artPath + "/character/GEPPETTO/Data/UserSettings/")
        self.paths['characters'] = (self.artPath + "character/")

        self.paths['charPath'] = (self.artPath + '/character/' + self.characterName)
        
        self.paths['animationPath'] = (self.paths['charPath'] + '/animation/')
        self.paths['setupPath'] = (self.paths['charPath'] + '/rig/setup/')
        self.paths['rigPath'] = (self.paths['charPath'] + '/rig/')
        self.paths['exportPath'] = (self.paths['charPath'] + '/export/')
        self.paths['ragdollPath'] = (self.paths['charPath'] + '/ragdoll/')
        #self.paths['setupPath'] = (self.charPath + '/setup/' + self.characterName)
        self.paths['wipPath'] = (self.paths['rigPath'] + '/wip/')
        
        self.paths['rigDir'] = (self.artPath + "/character/GEPPETTO/Rig/")
        self.paths['jointInfo'] = (self.artPath + "/character/GEPPETTO/Data/Character/")
                
    def createAllDirs(self, *args):
        for each in self.paths.values():
            directory = each
            self.verifyDirectory(directory)
            
    def createBakDirs(self, *args):
        for each in self.paths.values():
            directory = (each + '/Bak')
            self.verifyDirectory(directory)
           
    def verifyDirectory(self, directory, *args):
        if not os.path.exists(directory):
            os.makedirs(directory)
            print directory

import maya.cmds as cmds

import os

from System.userUtils import getUser

import System.turbineSpecificUtils as turbineUtils

import System.utils as utils

import System.directoryExtension as dirExt

import animationModuleSettings as animModSettings

import System.animationLibrary as animLibrary

import System.referenceUtils as referenceUtils

import System.setupTools as setupTools


""" import maya.cmds as cmds
import System.batchTools as batchTools
reload(batchTools)
batchTools = batchTools.ArtToolsBatch()
animationDirectory = '//corp-nas01/DC/dc_art/character/chr_superman/animation/'
batchTools.batchSaveToAnimLib(animationDirectory)
"""

"""
import maya.cmds as cmds
import System.batchTools as batchTools
reload(batchTools)
batchTools = batchTools.ArtToolsBatch()

animationDirectory = '//corp-nas01/DC/dc_art/character/GEPPETTO/Animation/animLib/'
rigFile = '//corp-nas01/DC/dc_art/character/chr_superman/rig/chr_superman.ma'
setupFile = '//corp-nas01/DC/dc_art/character/chr_superman/rig/setup/chr_superman.ma'
saveDir = '//corp-nas01/DC/dc_art/character/chr_superman/animation/batchTest/'

batchTools.batchLoadFromAnimLib(animationDirectory, rigFile, setupFile, saveDir)
"""



class ArtToolsBatch():
    
    def __init__(self):
        print 'init batch tools'
        self.characterName = turbineUtils.getCharacterInfo()[0]
        self.characterPrefix = turbineUtils.getCharacterInfo()[2]
        
        import System.directoryExtension as dirExt
        dirExt = dirExt.DirectoryExtension()
        self.animDir = dirExt.paths['animLib']
        
        
        
    def batchSaveToAnimLib(self, animationDirectory):
        animLib = animLibrary.animLibFuncs()
        animationFiles = utils.findAllAnimFiles(animationDirectory)
        
        """ Open each file so we can save the animation """
        for file in animationFiles:
            anmFile = (animationDirectory + file)
            cmds.file(anmFile, o=True, force=True)
            
            """ Get the name of the animation file to use as a starting point for naming the output from animLib """
            animName = cmds.file(q=True, sn=True, shn=True).replace(".ma", "")
            
            """ animationModuleSettings export settings File """
            animMods = animModSettings.AnimMod_Info()
            animMods.write_rig_settings(animName)
            
            fileName = (animName + '.ma')
            finalPath = (self.animDir + fileName)
            
            self.animLib = animLibrary.animLibFuncs()
    
            animCurves = self.animLib.getAnimCurves()[0]
            
            """ Insert code to verify the curve is valid (connected) """
            
            cmds.select(d=True)
            for curve in animCurves: 
                if cmds.objExists(curve) == True:   
                    cmds.select(curve, add=True)
            
            cmds.file(finalPath, es=True, type='mayaAscii', force=True)
            cmds.select(d=True)
            
    def batchLoadFromAnimLib(self, animationDirectory, rigFile, setupFile, saveDir):
        print ' Batch load initiated '
        
        import System.sceneSettings as settings
              
        animLib = animLibrary.animLibFuncs()
        #animationFiles = utils.findAllAnimFiles(animationDirectory)
        
        animFiles = utils.findAllAnimFiles(animationDirectory)
         
        for file in animFiles:
            cmds.file(new=True, pmt=False, force=True)
            
            finalPath = (animationDirectory + file)
                        
            tmpName = rigFile.rpartition('/')[2]
            self.characterName = tmpName.replace(".ma", "")
            """ use turbineUtils to find out the namespaces. """
            namespaces = turbineUtils.getCharacterNamespace(self.characterName)    
            characterNamespace = namespaces[0]
            characterName = self.characterName 
            
            settings.sceneSetup()
            
            refUtils = referenceUtils.Reference_Utils()

            refUtils.referenceFile(rigFile, characterNamespace, setupFile)            
        
            refUtils.setupConstraints(characterNamespace, characterName)
            
            animFile = cmds.file(finalPath, i=True, dns=True)
            
            """ Hide the Setup_grp """
            cmds.setAttr('Setup_grp.visibility', 0)
            
            """ Connect the animation curves to the controls """
            self.animLib = animLibrary.animLibFuncs()
            self.animLib.animConnectCurves(characterNamespace)
            
            """ Load the settings """
            self.animMods = animModSettings.AnimMod_Info()
            settingName = file.replace('.ma', '')
            loadSettings = self.animMods.load_rig_settings(settingName)
            
            """ Setup the nodes and layers """
            import System.setupTools as setupTools
            setupTools = setupTools.setup_Tools()
            createNode = setupTools.setupSceneForAnimation(file)
            
            saveFile = (saveDir + file)

            cmds.file( rename=saveFile )

            cmds.file(save=True, de=False, type='mayaAscii' )
            
            if loadSettings == None:
                cmds.headsUpMessage(file+ " has been loaded")
                print (file+ " has been loaded")
            else:
                print "---------Missing animation modules----------"
                for setting in loadSettings:
                    print setting
                cmds.headsUpMessage(file+ " has been loaded with --ERROR. /n Open the script editor for details")

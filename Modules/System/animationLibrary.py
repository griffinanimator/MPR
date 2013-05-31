import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.turbineSpecificUtils as turbineUtils

import animationModuleSettings as animModSettings


""" Currently I am only saving keys set by the animator.  We may want to get all the space switching and custom stuff as well"""

class animLibFuncs():    
    def __init__(self, *args):
        """ Call animationModuleSettings """
        self.animMods = animModSettings.AnimMod_Info()
        
        import System.directoryExtension as dirExt

        dirExt = dirExt.DirectoryExtension()
        self.animDir = dirExt.paths['animLib']
 
    def shortenCharacterName(self):

        characterNamespace = self.animMods.characterInfo['characterName']
        
        """ Get the character name.   Need a better util for this """
        tmpCharName = characterNamespace.partition("__")[2]
        characterShortName = tmpCharName.rpartition("_")[0]
        return (characterShortName)
    
    
    def getAnimCurves(self, *args):
        characterNamespace = self.animMods.characterInfo['characterName']
        
        animCurves = []
        tmpAnimCurves = []
        
        allAnimCurves = cmds.ls(type='animCurve')
        for curve in allAnimCurves:
            animCurves.append(curve)

        return (animCurves, tmpAnimCurves)
    

    
    def animConnectCurves(self, characterNamespace, *args):
        missingControls = []
        
        animCurves = self.getAnimCurves()[0]

        self.characterNamespace = characterNamespace
         
        for curve in animCurves:

            tmpControlName = curve.rpartition("_")[0]            
            tmpAttrName = curve.rpartition("_")[2]
            
            tmpControlName = tmpControlName.partition(':')[2]
            
            controlName = (self.characterNamespace + ':' + tmpControlName)

            attrName = (controlName + "." + tmpAttrName)
                    
            suffix = "_currentSpace"  
            result = curve.endswith(suffix)  
            if result == False:
                if cmds.objExists(controlName): 
                    try:
                        cmds.connectAttr(curve + '.output', attrName, force=True)
                    except: 
                        missingControls.append(controlName)
                        
        return missingControls
    
    def endFrame(self):
        lastFrame = cmds.playbackOptions( query = True, max = True )
        return lastFrame
        
        
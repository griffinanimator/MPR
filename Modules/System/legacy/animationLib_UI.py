import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.turbineSpecificUtils as turbineUtils

import animationModuleSettings as animModSettings

import System.animationLibrary as animLibrary


""" Currently I am only saving keys set by the animator.  We may want to get all the space switching and custom stuff as well"""

class AnimLib_UI():    
    def __init__(self, *args):
        import System.directoryExtension as dirExt
        dirExt = dirExt.DirectoryExtension()
        self.animDir = dirExt.paths['animLib']
        
        """ Call animationModuleSettings """      
        self.animMods = animModSettings.AnimMod_Info()
        #animMods = self.animMods
        
        self.animLib = animLibrary.animLibFuncs()
        #animLib = self.animLib

        try:
            characterName = self.animMods.characterInfo['characterName']
            
        except:
            cmds.headsUpMessage("no valid characters in this scene")
            if cmds.window("animLibWindow", exists=True):
                cmds.deleteUI("animLibWindow")
            return

            
        """ If the lib directory does not exist, create it. """
        turbineUtils.ensure_dir(self.animDir)
        """ Find all the files in the animation lib directory """
        anims = turbineUtils.findAllFiles('/GEPPETTO/Animation/animLib/', ".ma")
        
        """ Get the name of the animation file to use as a starting point for naming the output from animLib """
        sceneName = cmds.file(q=True, sn=True, shn=True).replace(".ma", "")
        
        """ Store the UI elements in a dictionary """
        self.animLibUIElements = {}
        
        """ If the window exists, delete it. """
        if cmds.window("animLibWindow", exists=True):
            cmds.deleteUI("animLibWindow")
            
        self.windowWidth = 440
        self.windowHeight = 320        
               
        buttonWidth = 100
        textWidth = 140
        columnOffset = 5
        buttonColumnWidth = buttonWidth + (2*columnOffset)
        textScrollWidth = (self.windowWidth - buttonColumnWidth)
        fieldWidth = (textScrollWidth -10 )
        fieldHeight = (self.windowHeight -40)
        
        # Create the main window
        mainWindow = self.animLibUIElements["window"] = cmds.window("animLibWindow", s=True, rtf=True )
        
        child1 = self.animLibUIElements["listBoxRowLayout"] = cmds.rowLayout(nc=2, columnWidth2=[buttonWidth, textScrollWidth], columnAttach=([1, "left", columnOffset], [2, "both", columnOffset]), rowAttach=([1, "top", columnOffset], [2, "top", columnOffset])) 
        
        # Create a couple flow layouts to hold the UI Elements for setup tools
        self.animLibUIElements["buttonColumnLayout"] = cmds.flowLayout(v=True) 
        cmds.setParent( '..' )        

        self.animLibUIElements["characterColumnLayout"] = cmds.flowLayout(v=True) 
        cmds.setParent( '..' )
    
        # Create the setup UI elements
        cmds.setParent(self.animLibUIElements["characterColumnLayout"])
        self.animLibUIElements["nameField"] = cmds.textField(tx=sceneName, width=fieldWidth)
        cmds.separator( height=7, style='in' )
        self.animLibUIElements["animationList"] = cmds.textScrollList(numberOfRows=4, allowMultiSelection=False, append=anims, selectIndexedItem=1, width=fieldWidth, h=fieldHeight)
        
        cmds.setParent(self.animLibUIElements["buttonColumnLayout"])
        self.animLibUIElements['saveAnimButton'] = cmds.button( label='Save Anim As', width=buttonWidth, c=self.exportAnimCurves )
        cmds.separator( height=5, style='in' )
        self.animLibUIElements['loadAnimButton'] = cmds.button( label='Load Animation', width=buttonWidth, h=100, c=self.importAnim )        
        
        cmds.setParent(self.animLibUIElements["window"])

        cmds.showWindow(self.animLibUIElements["window"])
        
        
    def exportAnimCurves(self, *args):
        characterNamespace = self.animMods.characterInfo['characterName']
        characterName = self.animLib.shortenCharacterName()
     
        animName = cmds.textField(self.animLibUIElements["nameField"], tx=True, q=True)
        
        """ animationModuleSettings export settings File """
        self.animMods.write_rig_settings(animName)
        
        finalPath = (self.animDir + animName)
    
        animCurves = self.animLib.getAnimCurves()[0]
        
        """ Insert code to verify the curve is valid (connected) """
        
        cmds.select(d=True)
        for curve in animCurves: 
            if cmds.objExists(curve) == True:   
                cmds.select(curve, add=True)
        
        cmds.file(finalPath, es=True, type='mayaAscii')
        cmds.select(d=True)
        #self.animLib.animPostExport(animCurves, characterNamespace)
        
    def importAnim(self, *args):
        characterNamespace = self.animMods.characterInfo['characterName']
        print "charNameSpace"
        print characterNamespace
        
        animName = cmds.textScrollList(self.animLibUIElements["animationList"], q=True, si=True)[0]
        animMaName = (animName + ".ma")
        finalPath = (self.animDir + animMaName)
        
        animFile = cmds.file(finalPath, i=True, dns=True)
        
        """ Connect the animation curves to the controls """
        self.animLib.animConnectCurves(characterNamespace)
        
        """ Load the settings """
        loadSettings = self.animMods.load_rig_settings(animName)
        
        if loadSettings == None:
            cmds.headsUpMessage(animName+ " has been loaded")
            print (animName+ " has been loaded")
        else:
            print "---------Missing animation modules----------"
            for setting in loadSettings:
                print setting
            cmds.headsUpMessage(animName+ " has been loaded with --ERROR. /n Open the script editor for details")
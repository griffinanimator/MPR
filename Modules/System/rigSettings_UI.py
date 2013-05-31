""" To run the UI """
#import maya.cmds as cmds

#import System.rigSettings_UI as rigSetUI
#reload (rigSetUI)

#rigSettingsUI = rigSetUI.RigSettings_UI()



import os
import maya.cmds as cmds
import System.utils as utils
import System.turbineSpecificUtils as turbineUtils

import System.animationModSettings as animModSettings


class RigSettings_UI:
    def __init__(self):
        """ Get all the settings files from the directory """
        dir = "Z:/art/character/GEPPETTO/Data/RigSettings/"
        settingsFiles = os.listdir(dir)
        
        self.UIElements = {}
        if cmds.window("rigSettings_UI_window", exists=True):
            cmds.deleteUI("rigSettings_UI_window")
            
        windowWidth = 200
        windowHeight = 400
        
        self.UIElements["window"]= cmds.window("rigSettings_UI_window", width=windowWidth, height=windowHeight, title="Rig Settings UI", sizeable = False)
        
        self.UIElements["buttonColumnLayout"] = cmds.flowLayout(v=True) 
        cmds.setParent( '..' )
        
        cmds.setParent(self.UIElements["buttonColumnLayout"])
        self.UIElements["settingsList"] = cmds.textScrollList(numberOfRows=4, allowMultiSelection=False, append=settingsFiles, selectIndexedItem=1, width=windowWidth, h=150)
        cmds.separator( height=5, style='in' )
        self.UIElements["loadButton"] = cmds.button(label="LOAD", width=windowWidth, c=self.loadSettings)
        
        cmds.setParent(self.UIElements["window"])

        cmds.showWindow(self.UIElements["window"])
        
    def loadSettings(self,*args):
        settingsFile = cmds.textScrollList(self.UIElements["settingsList"], q=True, si=True)[0]
        print settingsFile
        
        animModSet = animModSettings.AnimMod_Info().readAnimAttrs()
        
        for attr in animModSet:
            if cmds.objExists(attr[0]):

                try:                    
                    cmds.setAttr(attr[0], attr[1])
                    print "Hooray PASS"
                    print attr[0]
                    print attr[1]
                except: 
                    print "EPIC FAIL"
                    print attr[0]
                    print attr[1]
                
       
        
        
import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.referenceUtils as referenceUtils

import System.turbineSpecificUtils as turbineUtils

import __main__

class CharacterReferencer_UI:
    
    """ TODO:   The way I get the rig and setup files is BAD.  This method can cause lots of problems"""
    
    
    def __init__(self):
        # Setup the scene the Turbine way
        utils.sceneSetup(self)
        
        """ Dict for UIElements """
        self.UIElements = {}
        
        self.rigFiles = {}
        self.rigs = {}
        self.setupFile = {}
        self.rigFile = {}
        self.characterNamespace = {}
        self.setupDir = {}
        self.characterName = {}

        refUtils = referenceUtils.Reference_Utils()
         
        self.rigFiles['rigFiles'] = refUtils.findRigs()[0]
        self.rigs['rigs'] = refUtils.findRigs()[1]
        print self.rigFiles['rigFiles']
        print self.rigs['rigs']
        
        
        print self.rigs['rigs']

        """ If the window exists, delete it. """
        if cmds.window("charRefWindow", exists=True):
            cmds.deleteUI("charRefWindow")
                       
        self.windowWidth = 420
        self.windowHeight = 300        
        
        fieldWidth = (self.windowWidth - 10) 
        fieldHeight = (self.windowHeight - 60)      
        self.buttonWidth = fieldWidth
        
        columnOffset = 5
        buttonColumnWidth = self.buttonWidth + (2*columnOffset)
        textScrollWidth = (self.windowWidth - buttonColumnWidth)
        
        # Create the main window
        mainWindow = self.UIElements["window"] = cmds.window("charRefWindow", width=self.windowWidth, height=self.windowHeight, s=True)
       
        # Create a couple flow layouts to hold the UI Elements for setup tools
        self.UIElements["buttonColumnLayout"] = cmds.flowLayout(h=self.windowHeight, v=True) 
       
        self.UIElements["rigList"] = cmds.textScrollList(numberOfRows=20, allowMultiSelection=False, append=self.rigs['rigs'], width=fieldWidth, h=fieldHeight, fn="boldLabelFont", dcc=self.getFileForReference)
       
        cmds.separator( height=5, style='in' )
        
        
        self.UIElements['button'] = cmds.button( label='Reference Character', width=self.buttonWidth, c=self.setupPicker_UI)
        
        cmds.setParent(self.UIElements["buttonColumnLayout"])
               
        cmds.showWindow(self.UIElements["window"]) 
        
    def setupPicker_UI(self, *args): 

        """ First we will get the selected character and find the associated setup files """
        self.rigFile['currentRig'] = self.getFileForReference()[0]
        
        setupFile = self.getFileForReference()[1]
       
        cmds.textScrollList(self.UIElements["rigList"], edit=True, ra=True)
        cmds.textScrollList(self.UIElements["rigList"], edit=True, append=setupFile, dcc=self.getFileForReference)
       
        """ referenceFile """
        cmds.button( self.UIElements['button'], edit=True, label='Reference Setup', c=self.executeReferencing)

        
    def getFileForReference(self, *args):   
        fileName = cmds.textScrollList(self.UIElements["rigList"], q=True, si=True)[0]
        print "File Name"
        print fileName
        characterName = fileName.replace(".ma", "")
        self.characterName['characterName'] = characterName  
        
        """ use turbineUtils to find out the namespaces. """
        namespaces = turbineUtils.getCharacterNamespace(characterName)    
        self.characterNamespace['characterNamespace'] = namespaces[0]
              
      
        file = cmds.textScrollList(self.UIElements["rigList"], q=True, si=True)
        
        rigs = self.rigs['rigs']
        rigFiles = self.rigFiles['rigFiles']

        for index in range(len(rigs)):
            if rigs[index] == file[0]:
                rigFile = rigFiles[index]
                print rigFile
                setupFiles = rigFile.replace('/rig/', '/rig/setup/')
                setupDir = setupFiles.rpartition('/')[0]
        
        refUtils = referenceUtils.Reference_Utils()        
        setup = refUtils.findSetups(setupDir)
        
        self.setupDir['setupDir'] = setupDir
                
        return (rigFile, setup)


    def executeReferencing(self, *args): 
        self.setupFile['currentSetup'] = cmds.textScrollList(self.UIElements["rigList"], q=True, si=True)
        
        characterNamespace = self.characterNamespace['characterNamespace']
        rigFile = self.rigFile['currentRig']
        setupFile = (self.setupDir['setupDir'] + '/' + self.setupFile['currentSetup'][0])
        characterName = self.characterName['characterName']

           
        refUtils = referenceUtils.Reference_Utils()
        refUtils.referenceFile(rigFile, characterNamespace, setupFile) 
        
        refUtils.setupConstraints(characterNamespace, characterName)
        
        """ If the window exists, delete it. """
        if cmds.window("charRefWindow", exists=True):
            cmds.deleteUI("charRefWindow")
        
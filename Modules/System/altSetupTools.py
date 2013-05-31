import os
import maya.cmds as cmds
from functools import partial

from System.userUtils import getUser

import System.turbineSpecificUtils as turbineUtils

import System.utils as utils

import System.directoryExtension as dirExt

import System.jointUtils as jtUtils

import System.marking as marking

import System.skinning as skinning

import System.sceneSettings as sceneSettings

import csv

# Used to attach geometry
class Setup_Tools():    
    def __init__(self):
        """ Initialize class and variables """
        # Use the character name to determine the name of the setup node
        self.characterName = turbineUtils.getCharacterInfo()[0]
        self.characterPrefix = turbineUtils.getCharacterInfo()[2]
        self.exportPrefix = self.characterPrefix.replace('Character__', 'Export__')
        
        self.dirExt = dirExt.DirectoryExtension() 
        
        """ Define the character_container """
        self.characterContainer = (self.characterPrefix + ':character_container')

        """ Define the export_container """
        self.exportContainer = (self.exportPrefix + ':Setup')
        
    
    def setup_UI(self, *args): 
        characterName = self.characterName
     
        self.SaveTemplateUIElements = {}
        
        # If the window exists, delete it.
        if cmds.window("SetupNameWindow", exists=True):
            cmds.deleteUI("SetupNameWindow")
            
        self.windowWidth = 200
        self.windowHeight = 550        
                
        buttonWidth = (self.windowWidth -5)
        textWidth = 140
        columnOffset = 5

        
        # Create the main window
        mainWindow = self.SaveTemplateUIElements["window"] = cmds.window("SetupNameWindow", widthHeight=(240, 120), s=True )
        
        # Create a couple flow layouts to hold the UI Elements for setup tools
        self.SaveTemplateUIElements["buttonColumnLayout"] = cmds.flowLayout(v=True, w=buttonWidth) 
        cmds.setParent( '..' )        
    
        cmds.setParent(self.SaveTemplateUIElements["buttonColumnLayout"])

        cmds.separator( height=7, style='in' )
        cmds.button( label='Export Game Assets', width=buttonWidth, c=self.publishForExport )
        
        cmds.separator( height=7, style='in' )
        cmds.button( label='Add Holding Locs', width=buttonWidth, c=self.holdingLocations )
        
        cmds.separator( height=5, style='in' )
        self.SaveTemplateUIElements["skinBtn"] = cmds.button(label="Bind Skin", width=buttonWidth, c=self.attachWithSkinning ) 
        
        cmds.separator( height=5, style='in' )
        self.SaveTemplateUIElements["selJntsBtn"] = cmds.button(label="Select Game Joints", width=buttonWidth, c=self.selectGameJoints ) 
           
        cmds.setParent(self.SaveTemplateUIElements["window"])
        
        cmds.showWindow(self.SaveTemplateUIElements["window"])
        
    def exportAssets_UI(self, *args):
        self.UIElements = {}
        
        # If the window exists, delete it.
        if cmds.window("ExportAssets", exists=True):
            cmds.deleteUI("ExportAssets")
        
        # Create the main window
        self.UIElements["window"] = cmds.window("ExportAssets", widthHeight=(240, 200), s=True )
        
        # Create a flow layout to hold the UI Elements
        self.UIElements["radioFlowLayout"] = cmds.flowLayout(v=True, w=220) 
        cmds.setParent( '..' )  
        
        cmds.setParent(self.UIElements["radioFlowLayout"])
        
        cmds.radioCollection()
        self.UIElements['rigRadioButton'] = cmds.radioButton(l='Export Rig?')
        cmds.radioCollection()
        self.UIElements['setupRadioButton'] = cmds.radioButton(l='Export Setup?')
        
        cmds.separator( height=7, style='in' )
        cmds.text(l='  Rename the Setup?')
        
        self.UIElements['nameTxt'] = cmds.textField(w=220, tx=self.characterName)
        
        self.UIElements['exportButton'] = cmds.button(label='Export Game Assets', width=220, c=self.exportGameAssets)
        
        
        cmds.showWindow(self.UIElements["window"])


    def exportGameAssets(self, *args): 
        """ Query the state of the radio buttons so we know what to export """
        setupRadState = cmds.radioButton(self.UIElements['setupRadioButton'], q=True, sl=True)
        rigRadState = cmds.radioButton(self.UIElements['rigRadioButton'], q=True, sl=True)
        
        if setupRadState == True: 
            cmds.lockNode(self.exportContainer, l=False, lu=False)
            container = 'Geometry' 
            #self.verifySetupContainerContents(container)
                 
            self.exportSetup()
            
        if rigRadState == True:
                       
            self.removeNamespaces()
        
            self.exportRig()
            
        if cmds.window("ExportAssets", exists=True):
            cmds.deleteUI("ExportAssets")


    def exportWip(self, *args):   
        wipPath =(self.dirExt.paths['wipPath']  +  self.characterName + '.ma')
         
        self.dirExt.verifyDirectory(self.dirExt.paths['wipPath'])
        
        return wipPath
        
    def exportSetup(self):
        altCharacterName = cmds.textField(self.UIElements['nameTxt'], q=True, tx=True)
        
        if altCharacterName == self.characterName:        
            exportPath =(self.dirExt.paths['setupPath'] + self.characterName + '.ma')
        
        else:
            exportPath =(self.dirExt.paths['setupPath'] + altCharacterName + '.ma')
            
        # Remove the setup_grp and geometry group from it's container.
        cmds.lockNode(self.exportContainer, l=False, lu=False)
        
        self.removeConstraints()
            
        cmds.select(cl=True)

        cmds.select(self.exportContainer)
            
        self.dirExt.verifyDirectory(self.dirExt.paths['setupPath'])
        
        if cmds.file(exportPath, q=True, exists=True):
            turbineUtils.archiveFile(exportPath)
        
        cmds.file(exportPath, exportSelected=True, con=True, type="mayaAscii", f=True) 
        
        wipPath = self.exportWip()
        try:
            cmds.file(wipPath, open=True, f=True)
        except:pass
        cmds.lockNode(self.exportContainer, l=True, lu=True)
        
        
        
    def exportRig(self):
        #cmds.lockNode(self.characterContainer, l=False, lu=False)
        cmds.select(cl=True)
        
        cmds.select('character_container', cc=True)
        
        rigPath =(self.dirExt.paths['rigPath'] + self.characterName + '.ma')
        
        self.dirExt.verifyDirectory(self.dirExt.paths['rigPath'])
        
        if cmds.file(rigPath, q=True, exists=True):
            turbineUtils.archiveFile(rigPath)
            
        cmds.file(rigPath, exportSelected=True, con=False, type="mayaAscii", f=True)
        
        
    def createCharacterNameAttr(self, *args):

        """ Unlock character_container """
        cmds.lockNode(self.characterContainer, l=False, lu=False)
        cmds.addAttr(self.characterContainer, shortName='charName', dt='string')
        
        cmds.setAttr(self.characterPrefix + ':character_container.charName',  self.characterPrefix, type='string')
        
        """ lock character_container """
        cmds.lockNode(self.characterContainer, l=True, lu=True)
        
    def removeNamespaces(self, *args):
        cmds.namespace(set=':')
        """ Move objects out of the character namespace """
        cmds.namespace(mv=(self.characterPrefix, ':'), f=True)
        cmds.namespace(rm=self.characterPrefix)
        
        cmds.namespace(mv=(self.exportPrefix, ':'), f=True)
        cmds.namespace(rm=self.exportPrefix)
        
    def holdingLocations(self, *args):
        import System.marking as marking
        reload(marking)
        """ do the bone marking and holding locations """
        marking = marking.marking_Utils()
        
        if cmds.objExists(self.exportContainer):
            try:
                cmds.lockNode(self.exportContainer, l=False, lu=False)
            except: 
                print " No export container found for unlock "
        
        holdLocs = marking.loadHoldLocs()
        for loc in holdLocs:
            try:
                cmds.container(self.exportContainer, edit=True, addNode=loc)
            except: pass
            #cmds.parent(loc, 'Setup_grp')
        
        if cmds.objExists(self.exportContainer):
            try:
                cmds.lockNode(self.exportContainer, l=True, lu=True)
            except: pass
            
    
    def attachWithSkinning(self, *args):
        skinningTools = skinning.skinning_Tools()
        
        skinningTools.attachWithSkinning()
        
        
    def removeConstraints(self, *args):
        cmds.select('*_gjnt_parentConstraint*')
        try:
            cmds.select('*_gjnt_scaleConstraint*', add=True)
        except:
            pass
        parentConstraints = cmds.ls(sl=True)
        cmds.delete(parentConstraints)
        
    def verifySetupContainerContents(self, container, *args):
        relatives = cmds.listRelatives(container)
        for each in relatives:
            connections = cmds.listConnections(each)
            for node in connections:
                cmds.container(self.exportContainer, edit=True, an=node, isd=True)
                
    def selectGameJoints(self, *args):
        import System.jointUtils as jointUtils
        reload (jointUtils)

        gjUtils = jointUtils.gameJoint_Utils()

        gameJoints = gjUtils.getGameJoints()

        cmds.select(gameJoints)
        
    def publishForExport(self, *args):
        """ Let the user confirm they wish to proceed """
        confirmDialogue = cmds.confirmDialog( title='Confirm', message='Closing this file. Shall I proceed?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if confirmDialogue == 'No':
            return
        else:
            """ Try to move the character and setup containers into the default namespace """
            try:
                self.removeNamespaces()
            except:
                print "Failed to remove namespaces"
                return
    
            """ Export the setup and character containers to a rig file """
            """ Save the selection to a list and select """
            selection = ('character_container', 'Setup')
            cmds.select(d=True)
            for sel in selection:
                cmds.select(sel, add=True)
                
            rigFile = (self.dirExt.paths['rigPath'] +  self.characterName + '.ma')
            
            """ Export the selection to a rig file """
            cmds.file(rigFile, es=True, type='mayaAscii')  
            
            """ 
            Create a new file.
            Setup the scene.
            Define the namespace.
            Reference the character into the new file using the character namespace. 
            """
            cmds.file(new=True, force=True)
            sceneSettings.sceneSetup()
            characterNamespace = self.characterPrefix 
            cmds.file(rigFile, r=True, ns=characterNamespace)
            
            cmds.headsUpMessage( 'Save this file for export/animate with me' )
        
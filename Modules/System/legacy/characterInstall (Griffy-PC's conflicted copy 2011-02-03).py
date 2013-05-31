import maya.cmds as cmds
from System.userUtils import getUser
import getpass
import smtplib

import System.utils as utils
reload(utils)

import System.turbineSpecificUtils as turbineUtils
reload(turbineUtils)

import os

class InstallCharacter_UI:
    def __init__(self):
        # Setup the scene the Turbine way
        utils.sceneSetup(self)
        
        # Find all the available characters
        characters = turbineUtils.findAllRigFiles("\\GEPPETTO")
        # Warning if no characters exist
        if len(characters)==0:
            cmds.confirmDialog(title="Character Install", message="No published characters found, aborting install", button=["Accept"], defaultButton="Accept")
            return
            
        self.UIElements = {}
        
        if cmds.window("installCharacter_UI_window", exists=True):
            cmds.deleteUI("installCharacter_UI_window")
            
        windowWidth = 320
        windowHeight = 190
        self.UIElements["window"] = cmds.window("installCharacter_UI_window", width=windowWidth, height=windowHeight, title="Install Character", sizeable=False)
        
        self.UIElements["topColumn"] = cmds.columnLayout(adj=True, columnOffset=["both", 5], rs=3)
        
        self.UIElements["characterList"] = cmds.textScrollList(numberOfRows=9, allowMultiSelection=False, append=characters, selectIndexedItem=1)
        
        cmds.separator()
        
        self.UIElements["newCharacterButton"] = cmds.button(label="Create New Character", c=self.installCharacter)
        
        cmds.separator()
        
        cmds.showWindow(self.UIElements["window"])
        
    def installCharacter(self, listJoints):
        self.characterName = cmds.textScrollList(self.UIElements["characterList"], q=True, si=True)[0]

        self.installProc(self, self.characterName)


    def installProc(self, characterName, *args):

        # Return the directory names from setupDirs
        projectDirs = turbineUtils.setupDirs(self, self.characterName, create=False)       
        setupDir = projectDirs[1]
        xmlDir = projectDirs[2]
        rigDir = projectDirs[3]
        characterFileName = projectDirs[5]   
        setupFileName = projectDirs[6]        
        xmlFileName = projectDirs[7]
      
        # use turbineUtils to find out the namespaces.
        namespaces = turbineUtils.getCharacterNamespace(self, self.characterName)
    
        characterNamespace = namespaces[0]
        exportNamespace = namespaces[1]
        try:
            cmds.namespace(add=exportNamespace)
        except: pass
        
        characterNameString = (characterNamespace + ":")
       
        # Import the rig
        # Return the directory names from setupDirs
        projectDirs = turbineUtils.setupDirs(self, self.characterName, create=False) 
        characterFileName = projectDirs[5]
        print characterFileName
        if cmds.namespace(exists=characterNamespace):
            print "Rig Installed"
        else:
            cmds.file(characterFileName, i=True, namespace=characterNamespace)
          
        cmds.namespace(setNamespace=":")

        # Unlock 
        characterContainer = (characterNamespace + ":character_container")
        cmds.lockNode(characterContainer, lock=False, lockUnpublished=False)
        
        """ Check to see if a setup file already exists."""
        """If a setup exists, delete it."""               
        setupContainer = exportNamespace + ":Setup"
        if cmds.objExists(setupContainer):
            cmds.select(setupContainer)
            cmds.lockNode(lock=False, lu=False)
            cmds.delete(setupContainer)
        
        # Import the setup         
        # If the setup file exists on disk, import it.  Else we should build the setup
        if cmds.file(setupFileName, q=True, ex=True):
            cmds.file(setupFileName, i=True)
            cmds.setAttr("Setup_grp.visibility", 0)
            constraints = utils.parentToBlueprint(xmlFileName, characterNameString)
            parentConstraints = constraints[0]
            scaleConstraints = constraints[1]           
            
            """ Create the setup container if it does not exist """
            try:
                cmds.container(n=setupContainer)
            except: pass
            """ Add the setup and geometry groups to the setup container """
            cmds.container(setupContainer, edit=True, addNode="Setup_grp", ihb=True, force=True)
            try:
                cmds.container(setupContainer, edit=True, addNode="Geometry", ihb=True, force=True)
            except: pass
            
            """ Add the game_joint_parentConstraints to the Setup container """
            for constraint in parentConstraints:
                cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
            for constraint in scaleConstraints:
                cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
            
        else:
            cmds.group(n="Setup_grp", empty=True)
            cmds.setAttr("Setup_grp.visibility", 0)
            try:
                cmds.namespace(add=exportNamespace)
            except: pass   
            newSetupName = (exportNamespace + ":" + "Setup")
        
            cmds.select("Setup_grp")
            setupContents = cmds.listConnections("Setup_grp", type="joint")
    
            if setupContents != None and "game_joints" in (setupContents):
                constraints = utils.parentToBlueprint(xmlFileName, characterNameString)
                parentConstraints = constraints[0]
                scaleConstraints = constraints[1]
                """ Add the game_joint_parentConstraints to the Setup container """
                for constraint in parentConstraints:
                    cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
                for constraint in scaleConstraints:
                    cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
    
            else:     
                #Create the game joints and return the joint names
                cmds.select("Setup_grp")
                utilInfo = utils.importJointInfo(xmlFileName)
                listJoints = utilInfo
            
                # parent the joints into the setup group
                cmds.parent(listJoints, "Setup_grp")
            
                setupContainer = cmds.container(n="Setup", addNode="Setup_grp", inc=True, ihb=True, includeNetwork=True, force=True)
                              
                utils.setJointAttrs(xmlFileName)
                constraints = utils.parentToBlueprint(xmlFileName, characterNameString)
                parentConstraints = constraints[0]
                scaleConstraints = constraints[1]

                """ Add the game_joint_parentConstraints to the Setup container """
                for constraint in parentConstraints:
                    cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
                for constraint in scaleConstraints:
                    cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
                
                try:
                    cmds.namespace(add=exportNamespace)
                except: pass
                
                newSetupName = (exportNamespace + ":" + "Setup")   
                cmds.rename("Setup", newSetupName)
    
        newSetupName = (exportNamespace + ":" + "Setup")
        
        # Use turbineUtils to set bone marking and holding locations.
        turbineUtils.boneMarking()
        holdLocs = turbineUtils.loadHoldLocs()
    
        # add holding locs to the setup container
        cmds.container(newSetupName, edit=True, addNode=holdLocs, inc=True, ihb=True, includeNetwork=True, force=True)
        
        cmds.namespace(set=":")
           
        cmds.lockNode(characterContainer, lock=True, lockUnpublished=True)
        cmds.lockNode(newSetupName, lock=True, lockUnpublished=True)
        cmds.deleteUI(self.UIElements["window"])
               
        currentUser = getUser()
        
        niceName = (currentUser)[1]
        cmds.headsUpMessage(self.characterName+ " has been installed " + niceName)
        
        return (characterContainer, newSetupName)
        
        
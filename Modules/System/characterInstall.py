import maya.cmds as cmds
from System.userUtils import getUser
import getpass
import smtplib

import System.utils as utils

import System.turbineSpecificUtils as turbineUtils

import System.gameJointData as gjData

import System.jointUtils as jtUtils

import System.marking as marking

import System.setupTools as setupTools

import System.skinning as skinning

import os

class InstallCharacter_UI:
    def __init__(self):
        import pymel.core as pm
        pm.runtime.DisplayShaded()
        
        # Setup the scene the Turbine way
        utils.sceneSetup(self)
        
        # Find all the available characters
        characters = turbineUtils.findAllRigFiles("GEPPETTO/Rig")
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
        projectDirs = turbineUtils.setupDirs(self.characterName, create=False)       
        setupDir = projectDirs[1]
        xmlDir = projectDirs[2]
        rigDir = projectDirs[3]
        characterFileName = projectDirs[5]   
        setupFileName = projectDirs[6]        
        xmlFileName = projectDirs[7]
        meshDir = projectDirs[8]
        characterName = self.characterName
      
        """ use turbineUtils to find out the namespaces. """
        namespaces = turbineUtils.getCharacterNamespace(self.characterName)    
        characterNamespace = namespaces[0]        
        characterNameString = (characterNamespace + ":")
       
        """ Import the rig """
        # Return the directory names from setupDirs
        projectDirs = turbineUtils.setupDirs(self.characterName, create=False) 
        characterFileName = projectDirs[5]

        if cmds.namespace(exists=characterNamespace):
            print "Rig Installed"
        else:
            cmds.file(characterFileName, i=True, namespace=characterNamespace)
            cmds.namespace(set=characterNamespace)   
            
        cmds.namespace(setNamespace=":")  

        """ Unlock the character container """
        characterContainer = (characterNamespace + ":character_container")
        cmds.lockNode(characterContainer, lock=False, lockUnpublished=False)
        
        setupContainer = self.setupGameJoints(characterName, namespaces)

        """ Import the mesh if it exists """
        self.setupMesh(characterName, setupContainer)
        
        
        """ Lock the containers """
        cmds.lockNode(characterContainer, lock=True, lockUnpublished=True)
        cmds.lockNode(setupContainer, lock=True, lockUnpublished=True)
        
        """ Set namespace back to default """
        cmds.namespace(set=":")

        cmds.deleteUI(self.UIElements["window"])
        
                    
        """ Create all the necessary character directories if they do not exist """  
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()  
        dirExt.createAllDirs()
        dirExt.createBakDirs()
        
        """ Get the user name and inform of operation completion """       
        currentUser = getUser()        
        niceName = (currentUser)[1]
        cmds.headsUpMessage(self.characterName+ " has been installed " + niceName)
        
        
        
    def setupGameJoints(self, characterName, namespaces, *args):
        characterNamespace = namespaces[0]        
        characterNameString = (characterNamespace + ":")
        
        cmds.namespace(setNamespace=":") 
           
        """ Create a setup group """ 
        setupGrp = cmds.group(n="Setup_grp", empty=True)
        #cmds.setAttr("Setup_grp.visibility", 0)
        cmds.setAttr('Setup_grp.overrideEnabled', 1)
        cmds.setAttr('Setup_grp.overrideDisplayType', 1)
        
        """ Add an attribute to the setup group that tracks the version number """
        cmds.addAttr( shortName='ver', longName='version', at="long", r=True, k=True )
        
        
        """ Build the game skeleton """ 
        import System.gameJointData as gjData
        gjData = gjData.gameJoint_Data()
        
        listJoints = gjData.loadJointVars(characterName)
        
        """ parent the joints into the setup group """
        cmds.select(setupGrp)
        cmds.parent(listJoints, setupGrp)

        """ Set joint hierarchy """
        gjData.gameJointHierarchy(characterName)
        
        """ Orient the Joints """
        gjData.altOrientJoints(characterName)
       
            
        """ do the bone marking and holding locations """
        markingUtils = marking.marking_Utils()
        markingUtils.boneMarking()
        #Going to do this in the export file
        #holdLocs = markingUtils.loadHoldLocs()
        
        """ Create and add stuff to a setup container """
        """ Add a new namespace for the setup container """
        exportNamespace = namespaces[1]
        
        """ Set namespace back to default """
        cmds.namespace(set=":")   
        try:
            cmds.namespace(add=exportNamespace)
        except: pass
        
        cmds.namespace(set=exportNamespace)
        
        """ Build the setup container """
        setupContainerName = "Setup"
        if cmds.objExists(setupContainerName):
            pass
        else:
            setupContainer = cmds.container(n=setupContainerName)        

        """ add the setup grp to the setup container """
        cmds.container(setupContainer, edit=True, addNode="Setup_grp", inc=True, ihb=True, includeNetwork=True, force=True)
        """ Publish the version attribute to the setup container """
        cmds.container(setupContainer, edit=True, publishAndBind=["Setup_grp.version", "version"])

        """ Set namespace back to default """
        cmds.namespace(set=":")
        
        """ Constrain game joints to blueprint joints """
        constraints = gjData.parentGameToBlueprint(characterName, characterNamespace)
        parentConstraints = constraints
        #scaleConstraints = constraints[1]
             
        
        """ Add the game_joint_parentConstraints to the Setup container """
        for constraint in parentConstraints:
            cmds.container(setupContainer, edit=True, addNode=constraint, ihb=False, force=True)
        #for constraint in scaleConstraints:
            #cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
            
        return setupContainer
     
    def setupMesh(self, characterName, setupContainer):
        projectDirs = turbineUtils.setupDirs(self.characterName, create=False)
        meshDir = projectDirs[8]
        characterName = self.characterName
        #setupContainer = self.setupContainer
          
        """ Import the mesh if it exists """
        meshName = (meshDir + characterName + ".ma")
        
        geoGrp = "Geometry"
        if cmds.file(meshName, q=True, ex=True):
            """ Create a group for the mesh """
            cmds.file(meshName, i=True, gr=True, gn=geoGrp)
            cmds.select(geoGrp)
            """ Add an attribute to the geo group that toggles vis mode. """
            enumNames = "normal:template:reference"
            try:
                cmds.setAttr("Geometry.overrideEnabled", 1)
                cmds.container(setupNode, edit=True, publishAndBind=["Geometry.overrideDisplayType", "GeoDisplay"]) 
            except: print 'attribute exists'
        else:
            print "mesh does not exist on disk"
         
        """ Get the mesh into a var """
        if cmds.objExists(geoGrp):
            characterGeo = cmds.listRelatives(geoGrp, c=True, type="transform")

            """ Parent the geo to the geo grp """
            #for geo in characterGeo:
                #cmds.parent(geo, geoGrp) 
                
            """ Unlock the setup container """
            cmds.lockNode(setupContainer, lock=False, lockUnpublished=False)
            
            """ Add the Geo grp to the setup container """
            cmds.container(setupContainer, edit=True, addNode=geoGrp, inc=True, ihb=True, isd=True, includeNetwork=True, force=True)
            
        
            import System.skinning as skinning
            """ Skin the mesh """
            cmds.select(characterGeo)
            doSkin = skinning.skinning_Tools()
            doSkin.attachWithSkinning()
                    
            """ Apply skin weights if they exist """
            cmds.select(characterGeo)
            doSkin.loadSkinWeights(characterName)
        
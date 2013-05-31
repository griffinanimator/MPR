import os
import maya.cmds as cmds
import pymel.core as pm
from functools import partial

from System.userUtils import getUser

import System.turbineSpecificUtils as turbineUtils

import System.utils as utils

import csv

# Used to attach geometry

class setup_Tools():    
    def __init__(self):
        """ Initialize class and variables """
        # Use the character name to determine the name of the setup node
        self.characterName = turbineUtils.getCharacterInfo()[0]
        self.fullCharName = turbineUtils.getCharacterInfo()[2]
           
    def setup_UI(self, *args): 
        characterName = self.characterName

        # Find all the available characters
        characters = turbineUtils.findAllFiles("\\" + characterName + "\\export", ".ma")
     
        self.SaveTemplateUIElements = {}
        
        # If the window exists, delete it.
        if cmds.window("SetupNameWindow", exists=True):
            cmds.deleteUI("SetupNameWindow")
            
        self.windowWidth = 300
        self.windowHeight = 550        
                
        buttonWidth = 100
        textWidth = 140
        columnOffset = 5
        buttonColumnWidth = buttonWidth + (2*columnOffset)
        textScrollWidth = (self.windowWidth - buttonColumnWidth)
        
        # Create the main window
        mainWindow = self.SaveTemplateUIElements["window"] = cmds.window("SetupNameWindow", widthHeight=(240, 85), s=True )
        
        # Setup Tabs
        tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        
        child1 = self.SaveTemplateUIElements["listBoxRowLayout"] = cmds.rowLayout(nc=2, columnWidth2=[buttonWidth, textScrollWidth], columnAttach=([1, "left", columnOffset], [2, "both", columnOffset]), rowAttach=([1, "top", columnOffset], [2, "top", columnOffset])) 
        
        # Create a couple flow layouts to hold the UI Elements for setup tools
        self.SaveTemplateUIElements["buttonColumnLayout"] = cmds.flowLayout(v=True) 
        cmds.setParent( '..' )        

        self.SaveTemplateUIElements["characterColumnLayout"] = cmds.flowLayout(v=True) 
        cmds.setParent( '..' )
    
        # Create the setup UI elements
        cmds.setParent(self.SaveTemplateUIElements["characterColumnLayout"])
        self.SaveTemplateUIElements["nameField"] = cmds.textField(tx=self.characterName, width=textWidth)
        cmds.separator( height=7, style='in' )
        #self.SaveTemplateUIElements["characterList"] = cmds.textScrollList(numberOfRows=4, allowMultiSelection=False, append=characters, selectIndexedItem=1, width=textWidth, h=80)
        
        cmds.setParent(self.SaveTemplateUIElements["buttonColumnLayout"])
        cmds.button( label='Save Setup As', width=buttonWidth, c=self.saveSetup )
        cmds.separator( height=5, style='in' )
        #cmds.button( label='Load Setup', width=buttonWidth, h=100, c=self.loadSetup )        
        
        cmds.setParent(self.SaveTemplateUIElements["window"])

        child2 = cmds.flowLayout(v=True)
        self.SaveTemplateUIElements["skinBtn"] = cmds.button(label="Bind Skin", width=buttonWidth, c=self.attachWithSkinning ) 
        cmds.separator( height=7, style='in' )
        self.SaveTemplateUIElements["saveWtBtn"] = cmds.button(label="Save Weights", width=buttonWidth, c=self.saveSkinWeights )       
        self.SaveTemplateUIElements["loadWtBtn"] = cmds.button(label="Load Weights", width=buttonWidth, c=self.loadSkinWeights )
        cmds.separator( height=7, style='in' )
        self.SaveTemplateUIElements["editBtn"] = cmds.button(label="Edit Mode Off", width=buttonWidth, c=self.editModeToggle )
        
        cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Setup'), (child2, 'Skin')) )
        
        cmds.showWindow(self.SaveTemplateUIElements["window"])


    def loadSetup(self, *args):
        characterName = self.characterName
        #characterName = cmds.textScrollList(self.SaveTemplateUIElements["characterList"], q=True, si=True)[0]
        self.setupInstallProc(characterName)
    
    def setupInstallProc(self, characterName):
      # Return the directory names from setupDirs
        projectDirs = turbineUtils.setupDirs(characterName, create=False)       
        setupDir = projectDirs[1]
        xmlDir = projectDirs[2]
        rigDir = projectDirs[3]
        characterFileName = projectDirs[5]         
        xmlFileName = projectDirs[7]
        
        selItem = cmds.textScrollList(self.SaveTemplateUIElements["characterList"], q=True, si=True)
        
        setupFileName = (setupDir +  selItem[0] + ".ma")
          
        # use turbineUtils to find out the namespaces.
        fullCharName = turbineUtils.getCharacterInfo()[2]
    
        characterNamespace = fullCharName
        exportNamespace = fullCharName.replace("Character", "Export")

        try:
            cmds.namespace(add=exportNamespace)
        except: pass
        
        characterNameString = (characterNamespace + ":")
       
        # Unlock 
        characterContainer = (characterNamespace + ":character_container")
        cmds.lockNode(characterContainer, lock=False, lockUnpublished=False)
        
        """ Check to see if a setup container already exists."""
        """If a setup_grp exists, delete it."""  
                   
        setupContainer = turbineUtils.getCharacterInfo()[3]

        # Delete the contents of the setup container
        if cmds.objExists(setupContainer):
            cmds.select(setupContainer)
            cmds.lockNode(lock=False, lu=False)
            setupNodes = cmds.container(setupContainer, q=True, nl=True)
            cmds.delete(setupNodes)

        # Import the setup         
        # If the setup file exists on disk, import it.  Else we should build the setup
        if cmds.file(setupFileName, q=True, ex=True):
            cmds.file(setupFileName, i=True)
            #Setup_grp vis to 0
            cmds.setAttr("Setup_grp.visibility", 0)
               
            """ Create the setup container if it does not exist """  
            if cmds.objExists(setupContainer):
                pass
            else:
                cmds.container(n=setupContainer)
            
  
        """ Add the setup and geometry groups to the setup container """
        cmds.container(setupContainer, edit=True, addNode="Setup_grp", ihb=True, force=True)
        try:
            cmds.container(setupContainer, edit=True, addNode="Geometry", ihb=True, force=True)
        except: pass
            
        constraints = turbineUtils.parentToBlueprint(xmlFileName, characterNameString)
        parentConstraints = constraints[0]
        scaleConstraints = constraints[1] 
            
            
        """ Add the game_joint_parentConstraints to the Setup container """
        for constraint in parentConstraints:
            cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
        for constraint in scaleConstraints:
            cmds.container(setupContainer, edit=True, addNode=constraint, ihb=True, force=True)
     
        # Use turbineUtils to set bone marking and holding locations.
        turbineUtils.boneMarking()

        holdLocs = turbineUtils.loadHoldLocs()
    
        # add holding locs to the setup container
        cmds.container(setupContainer, edit=True, addNode=holdLocs, inc=True, ihb=True, includeNetwork=True, force=True)
        
        cmds.namespace(set=":")
           
        cmds.lockNode(characterContainer, lock=True, lockUnpublished=True)
        cmds.lockNode(setupContainer, lock=True, lockUnpublished=True)
        cmds.deleteUI(self.SaveTemplateUIElements["window"])
        
        # Get the user name and inform the user        
        currentUser = getUser()        
        niceName = (currentUser)[1]
        cmds.headsUpMessage(self.characterName+ " has been installed " + niceName)
        
        return (characterContainer, setupContainer)
    
    
        

    def saveSetup(self, *args):
        exportNodes = []
        
        # Query the text field from the saveSetupUI to see if the user chose a new name.
        setupName = cmds.textField(self.SaveTemplateUIElements["nameField"],q=True, text=True)
        
        characterName = self.characterName 
        tmpDir = turbineUtils.setupDirs(characterName, create=False)[0]
        characterDir = (tmpDir + "\export\\")
        
        # Find the setup node.
        fullCharName = self.fullCharName
        exportName = fullCharName.replace("Character__", "Export__")
        
        setupNode = (exportName + ":Setup")
        
        cmds.lockNode(setupNode, lock=False, lockUnpublished=False)    
        #tmpSetupNode = cmds.rename(setupNode, "Setup")
        # Define the path and name for the setup file.
        #setupFileName = characterDir + setupName + "_setup" + ".ma"
        setupFileName = characterDir + setupName + ".ma"
        cmds.select(cl=True)
        
        #gameJntConnections = cmds.container(tmpSetupNode,query=True,nodeList=True)
        gameJntConnections = cmds.container(setupNode,query=True,nodeList=True)
        
        # Remove the setup_grp and geometry group from it's container.
        cmds.container(setupNode, edit=True, removeNode="Setup_grp", ihb=True)
        if cmds.objExists("Geometry"):
            cmds.container(setupNode, edit=True, removeNode="Geometry", ihb=True)
            cmds.select("Geometry")
        cmds.select("Setup_grp", add=True)
        
        # ad some stuff here to query and remove from namespaces

        cmds.file(setupFileName, exportSelected=True, con=False, type="mayaAscii")       
        
        # Put the setup and geo groups back in the container.
        cmds.container(setupNode, edit=True, addNode="Setup_grp", ihb=True, force=True)
        if cmds.objExists("Geometry"):
            cmds.container(setupNode, edit=True, addNode="Geometry", ihb=True, force=True)

        # Confirm that the setup has been exported
        exportConfirm = (setupName + " has been exported to " + characterDir)
        cmds.confirmDialog(messageAlign="center", title="Create Directory", message= exportConfirm)

        cmds.lockNode(setupNode, lock=True, lockUnpublished=True)

        cmds.select(cl=True)
        
        
    """ All the skinning functions to follow"""  
      
    def attachWithParenting(self):
        self.parenting = True
        self.skinning = False
        self.processInitialSelection()
        
    def attachWithSkinning(self, *args):
        self.skinning = True
        self.parenting = False
        self.processInitialSelection()
        
    def processInitialSelection(self):
        selection = cmds.ls(selection=True)
        
        setupContents = []
        
        geometry = self.findGeometry(selection)
        
        characterContainer = turbineUtils.getCharacterInfo()[1]
        characterName = turbineUtils.getCharacterInfo()[0]
        # exportName will define the name of the export node and can also be used 
        # for the namespace the export node resides in
        
        setupNode = turbineUtils.getCharacterInfo()[3]

        # Use the joint class to identify the joints in the scene
        import System.jointUtils as jntUtils
        reload (jntUtils)
        
        joint = jntUtils.gameJoint_Utils()
        gameJoints = joint.getGameJoints()
        
        geoNode = ("Geometry")
        
        if geometry == None:
            cmds.headsUpMessage("please select the geometry you wish to attach to the specified blueprint joint.")
        else:      
            self.doSkin(geometry, gameJoints, geoNode, setupNode) 
       
        return (geometry, characterContainer, characterName, gameJoints, geoNode, setupNode)
        
        
    def findGeometry(self, selection):
        selection = cmds.ls(selection, transforms=True)
        
        nonJointSelection = []
        for node in selection:
            if not cmds.objectType(node, isType="joint"):
                nonJointSelection.append(node)
                
        if len(nonJointSelection) > 0:
            return nonJointSelection
        else:
            return None
        
    def findGameJoints(self, setupContents):
        if len(setupContents) > 0:
            return setupContents
        else:
            return None
             
    
    def doSkin(self, geometry, gameJoints, geoNode, setupNode):
        # Set the namespace to the export namespace
        characterName = turbineUtils.getCharacterInfo()[0]
        
        exportName = turbineUtils.getCharacterInfo()[3]
        
        cmds.namespace(set=":")
        
        # Create a geometry container

        if cmds.objExists(geoNode):
            print "Geo node exists"
        else:
            geoGrp = cmds.group(n=geoNode, empty=True)
        
        cmds.lockNode(setupNode, lock=False, lockUnpublished=False)
            
        for geo in geometry:
            cmds.select(d=True)
            import maya.mel as mel
            
            cmds.select(gameJoints, geo)
            
            skinClust = cmds.skinCluster(gameJoints, geo, tsb=True, maximumInfluences=2, omi=True, rui=False, sm=0, normalizeWeights=1, n=geo+"_skinCluster")
            try:
                cmds.parent(geo, geoNode)
            except: pass
            try:
                cmds.container(setupNode, edit=True, addNode=geoGrp, inc=True, ihb=True, it=True, ish=True, isd=True)
            except: pass           
            
        cmds.lockNode(setupNode, lock=True, lockUnpublished=True)
        # Set the namespace back to default
        cmds.namespace(set=":")
        
        
    def editModeToggle(self, *args):

        setupNode = turbineUtils.getCharacterInfo()[3]
   
        labelVal = cmds.button(self.SaveTemplateUIElements["editBtn"], q=True, l=True )
        if labelVal == "Edit Mode On":
            cmds.button(self.SaveTemplateUIElements["editBtn"], edit=True, l="Edit Mode Off" )
            cmds.lockNode(setupNode, lock=True, lockUnpublished=True)
                
        else:
            cmds.button(self.SaveTemplateUIElements["editBtn"], edit=True, l="Edit Mode On" )
            cmds.lockNode(setupNode, lock=False, lockUnpublished=False)
            
            
            
            
    def saveSkinWeights(self, *args):
        ''' This next block is used to define the path where the weights will be saved.
        I plan on putting this in the __init__ once I am done testing '''
        print "saving weights"
        #import tsapi.core.maya.animation as annie
        #reload(annie)
        
        try:
            character = cmds.ls(sl=True)[0]
        except:
            cmds.headsUpMessage("Please Select Valid Geometry")
            return
        annie = annie.animation()
        

        # Define the file name and path
        characterName = self.characterName 
        skinPath = turbineUtils.setupDirs(characterName, create=False)[4]
        outFileSuffix = '_skinWeight.csv'
        outFile = (character + outFileSuffix )
        finalPath = (skinPath + outFile)
        
        """ Delete the skin file if one already exists """
        if cmds.file(finalPath, q=True, ex=True):
            os.remove(finalPath)
                
        # Select the character here, then use GetValidSkinWeights to grab vert info.
        print " Annie used here"
        for char in annie.GetValidSkinWeights():
            vert = char[0]
        
            jointInfo = char[1]
            for each in jointInfo:
                joint = each[0]
                tmpWeight = each[1]

                weight = str("%.2f" % tmpWeight)
                weight = float(weight)

                value = (vert, joint, weight)
                   
                writer = csv.writer(open(finalPath, "a"))                
                writer.writerow(value)
        """ I need to make sure the file closes here """            
        # Close the file
        #file.close(finalPath)
        
         # Get the user name and inform the user the weights have been saved        
        currentUser = getUser()        
        niceName = (currentUser)[1]
        cmds.headsUpMessage("The weight file has been saved to " + finalPath)

       
    def loadSkinWeights(self, *args):
        import maya.mel as mel
        #import tsapi.core.maya.animation as annie
        #reload(annie)
        
        try:
            character = cmds.ls(sl=True)[0]
        except:
            cmds.headsUpMessage("Please Select Valid Geometry")
            return

        
        # Define the file name and path
        characterName = self.characterName 
        skinPath = turbineUtils.setupDirs(characterName, create=False)[4]
        outFileSuffix = '_skinWeight.csv'
        outFile = (character + outFileSuffix )
        finalPath = (skinPath + outFile)

        missingJoints = []
        allCV = []
        if cmds.file(finalPath, q=True, ex=True):
            reader = csv.reader(open(finalPath, 'rb'), delimiter=' ', quotechar='|')
        else:
            return
        
        # Find the skin cluster
        selection= cmds.ls(sl=True, fl=True)
        mel.eval("$selectionList = `ls -sl`")
        skCl = mel.eval('findRelatedSkinCluster $selectionList[0]')
    
        for row in reader:
            if row not in allCV:
                allCV.append(row)
                
        for cv in allCV:
            splitString1 = cv[0].partition(",")
            vert =  splitString1[0]
            splitString2 = splitString1[2].partition(",")
            joint = splitString2[0]
            value = float(splitString2[2])
        
            
            if cmds.objExists(joint):
                cmds.skinPercent( skCl, vert, transformValue=[(joint, value)])
            else:
                missingJoints.append(joint)
                
        """ Normalize the weights """
        cmds.skinPercent(skCl, normalize=True)
        
        if len(missingJoints) == 0:  
            cmds.headsUpMessage("The weight has been loaded from " + finalPath)
        else:
            cmds.headsUpMessage("Influences are missing.  Please view the script editor for details.")
            print "These influences do not exist"
            for joint in missingJoints:
                print joint
            
            
    def zeroModWeightsA(self, *args):
        import System.animationToolUtils as animUtils
        animUtils.zeroModWeights()
        
        
    def setupSceneForAnimation(self, file):
        print 'setup scene.........................'
        print file
        
        """ Create a fileType node set to animation """
        
        import tap.tools.maya.createFileTypeNode as createFileTypeNode

        """ Looks for the file type node, and creates one if it does not find one """
        turbineFileTypeNode = ""
    
        typeNode = pm.mel.eval("$temp = `getLayerTypeNode`;")

        dlgResult = True
        if dlgResult == True:
            createFileTypeNode.createFileTypeNode("AnimationNode") 
            
        """ Populate the node options with the character prefix and destination directory. """
        cmds.select('transform*')
        fileTypeNode = cmds.ls(sl=True)
        
        prefixAttr = (fileTypeNode[0] + '.FilePrefix')
        dataDirAttr = (fileTypeNode[0] + '.DataDirectory')
        
        dataDirVal = ('character/' + self.characterName + '/animation')
        prefixVal = self.characterName.partition('_')[0]
        
        cmds.setAttr(prefixAttr, prefixVal, type='string')
        cmds.setAttr(dataDirAttr, dataDirVal, type='string')
        
        """ Determine a layer name based off the file name """
        layerNameA = file.replace('.ma', '')
        prefixValExt = (prefixVal + '_')
        layerName = layerNameA.replace(prefixValExt, '')
               
        """ Put the setup on the layer """

        cmds.select('Setup_grp', hi=True)
        cmds.select(fileTypeNode, hi=True, add=True)
        setupContents = cmds.ls(sl=True)
        
        cmds.createDisplayLayer(n=layerName)
        
        print 'done........................'

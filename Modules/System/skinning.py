import os
import maya.cmds as cmds
from functools import partial

#import System.characterInstall as install
#reload (install)

import System.turbineSpecificUtils as turbineUtils

import csv

import tap.core.maya.animation as animation

# Used to attach geometry

class skinning_Tools:
    def __init__(self):
        self.characterName = turbineUtils.getCharacterInfo()[0]
        self.fullCharName = turbineUtils.getCharacterInfo()[2]
        
        
    def attachGeo_UI(self):
        
        # store UI elements in a dictionary
        self.UIElements = {}
        
        if cmds.window("attachGeo_UI_window", exists=True):
            cmds.deleteUI("attachGeo_UI_window")
            
        windowWidth = 200
        windowHeight = 200
        
        self.UIElements["window"]= cmds.window("attachGeo_UI_window", width=windowWidth, height=windowHeight, title="Attach Geometry UI", sizeable = False)
        
        # Create UI elements
        self.UIElements ["topLevelColumn"] = cmds.columnLayout(adjustableColumn=True, columnAlign = "center")
        
        # Buttons
        cmds.setParent(self.UIElements["topLevelColumn"])
        self.UIElements["skinSaveColumn"] = cmds.columnLayout(adj=True, columnAlign="center", rs=3)
        
        cmds.separator()
        
        self.UIElements["skinBtn"] = cmds.button(label="Skin", c=self.attachWithSkinning )
        
        self.UIElements["editBtn"] = cmds.button(label="Edit Mode Off", c=self.editModeToggle )
       
        cmds.separator()
        # Display Window
        cmds.showWindow(self.UIElements["window"])
        

      
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
            cmds.setAttr("Geometry.overrideEnabled", 1)

        cmds.lockNode(setupNode, lock=False, lockUnpublished=False)
        try:     
            """ Publish the displayType attribute to the setup container """
            cmds.container(setupNode, edit=True, publishAndBind=["Geometry.overrideDisplayType", "GeoDisplay"]) 
        except: print 'Attribute exists'
            
        for geo in geometry:
            cmds.select(d=True)
            import maya.mel as mel
            
            cmds.select(gameJoints, geo)
            
            """ I need to find out if the skin cluster exists.  If so, index the name +1"""
            skinClusterName = (geo+"_skinCluster")                
            skinClust = cmds.skinCluster(gameJoints, geo, tsb=True, maximumInfluences=4, omi=True, rui=False, sm=0, normalizeWeights=1, n=skinClusterName)
            try:
                cmds.parent(geo, geoNode)
            except: pass
            try:
                cmds.container(setupNode, edit=True, addNode=geoGrp, inc=True, ihb=True, it=True, ish=True, isd=True)
            except: pass           
            
        #cmds.lockNode(setupNode, lock=True, lockUnpublished=True)
        # Set the namespace back to default
        cmds.namespace(set=":")
        
        
    def editModeToggle(self, *args):

        setupNode = turbineUtils.getCharacterInfo()[3]
   
        labelVal = cmds.button(self.UIElements["editBtn"], q=True, l=True )
        if labelVal == "Edit Mode On":
            cmds.button(self.UIElements["editBtn"], edit=True, l="Edit Mode Off" )
            cmds.lockNode(setupNode, lock=True, lockUnpublished=True)
                
        else:
            cmds.button(self.UIElements["editBtn"], edit=True, l="Edit Mode On" )
            cmds.lockNode(setupNode, lock=False, lockUnpublished=False)
   
   
    def saveSkinWeights(self, *args):
        ''' This next block is used to define the path where the weights will be saved.
        I plan on putting this in the __init__ once I am done testing '''
        print "saving weights"
        
        try:
            character = cmds.ls(sl=True)[0]
        except:
            cmds.headsUpMessage("Please Select Valid Geometry")
            return
        weights = animation.Weights()
        

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

        for char in Weights.getValidSkinWeights():
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
import os
import maya.cmds as cmds
from functools import partial
import System.characterInstall as install
reload (install)
import System.turbineSpecificUtils as turbineUtils
reload(turbineUtils)

import tsapi.core.maya.animation as annie
reload(annie)

import csv

# Used to attach geometry

class skinning_Tools:
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
        import tsapi.core.maya.joint as joint
        reload (joint)
        
        joint = joint.joint()
        #ignoreBones = joint.GetGameJointInfo()[2]
        gameJoints = joint.GetGameJointInfo()[0]
        
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
            mel.eval ("SmoothBindSkinOptions")
            
            #skinClust = cmds.skinCluster(gameJoints, geo, tsb=True, n=geo+"_skinCluster")
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
   
        labelVal = cmds.button(self.UIElements["editBtn"], q=True, l=True )
        if labelVal == "Edit Mode On":
            cmds.button(self.UIElements["editBtn"], edit=True, l="Edit Mode Off" )
            cmds.lockNode(setupNode, lock=True, lockUnpublished=True)
                
        else:
            cmds.button(self.UIElements["editBtn"], edit=True, l="Edit Mode On" )
            cmds.lockNode(setupNode, lock=False, lockUnpublished=False)
          
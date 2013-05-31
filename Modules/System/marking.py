import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.turbineSpecificUtils as turbineUtils

import System.jointUtils as jointUtils

class marking_Utils():    
    def __init__(self):
        """ Initialize class and variables """
        self.jointUtils = jointUtils.gameJoint_Utils()
  
    
    def loadHoldLocs(self, *args):
        import xml.dom.minidom
        import xml.dom

        characterName = ""
        xmlDir = turbineUtils.setupDirs(characterName, create=False)[2]
        # The name of the holding location
        allLocs=[]
        allJoints=[]

        bindJoints = self.jointUtils.getGameJoints()
        
        if bindJoints == None:
            cmds.headsUpMessage( 'No game joints exist in this scene.  Holding locations will not be added.')
            return
        else:
            # We should create a holding loc for each game joint.    
            cmds.select( clear=True )
    
            # open the xml file for reading 
            holdLocFile = (xmlDir + "/holdLocList.xml")
    
            fileObject = file(holdLocFile, 'r')
           
            # parse the xml file to get all of it's elements
            xmlDoc = xml.dom.minidom.parse(fileObject)
            # Get the joint elements into a list
            joints = xmlDoc.getElementsByTagName('joint')
            # iterate through all of the joint elements
            #Loads joint positions
            for joint in joints:
                # get the child elements of the joint in order to get the loc name
                children = joint.childNodes            
                # loop through the child elements
                for child in children:
                    # make sure the the current node type is not a text node
                    if child.nodeType != child.TEXT_NODE:
                    
                    # Deal with holding loc name. #########################################################
                        if child.tagName == "locName":
                            # if the node is locName node get it's children
                            # to get the locName
                            locAxis = child.childNodes
                            for axis in locAxis:
                                if axis.nodeType != axis.TEXT_NODE:
                                    locValue = axis.getAttribute("value")
    
                                    
                # get the name of the joint from the name attribute attached to the joint element.
                jointName = joint.getAttribute("name")                                 
    
                if cmds.objExists(jointName):     
                    allJoints.append(jointName)
                    jointPos = cmds.xform(jointName, q=True, ws=True, t=True, a=True)
                    # Final name for the holding location 
                                                            
                    locName = ("HoldingLocation_" + jointName + "_" + locValue)
            
                    allLocs.append(locName)
                    
                    if cmds.objExists(locName) == False:
    
                        locGrp = pm.group(em=True, w=True, n=locName)
        
                        locGrp = cmds.ls(sl=True)
                        locGrp = (locGrp)[0]
        
                        # Move locGrp to joints position
                        cmds.move(jointPos[0], jointPos[1], jointPos[2], locGrp, r=True)
                        
                        cmds.setAttr(locGrp + '.displayHandle', 1)
                        cmds.setAttr(locGrp + '.displayLocalAxis', 1)
    
                        # Add an "LocationType" attr to the holding loc
                        cmds.addAttr(ln="LocationType", dt="string", k=False)
                        cmds.setAttr(locGrp+".LocationType", locValue, type="string")
                        # parent the holdLoc to the joint
                        cmds.parent(locGrp, jointName)

                  
            # close the file
            fileObject.close()
            
        # Return some info to let the user know if the holding locs were created.
        jntLen = len(allJoints)
        locLen = len(allLocs)
    
        return allLocs
    
    def boneMarking(self):
        ignoreBones = self.jointUtils.getIgnoreBones()
        bindJoints = self.jointUtils.getGameJoints()
        """ Mark the ignore bones """
        for joint in ignoreBones:
            cmds.select (joint)
            try:
                cmds.setAttr(joint + ".ignore", 1)
            except:
                cmds.addAttr(ln="ignore", at="bool", k=False)
                cmds.setAttr(joint + ".ignore", 1)
                
        parentJnt = self.jointUtils.getParentJoint()
        if parentJnt != None:
            for joint in parentJnt:
                cmds.select (joint)
                try:
                    cmds.setAttr(joint + ".game_root", 1)
                except:
                    cmds.addAttr(ln="game_root", at="bool", k=False)
                    cmds.setAttr(joint + ".game_root", 1)
               
                
        """ Create a bone marking for each joint """        
        for joint in bindJoints:
            cmds.select (joint)
            splitString = joint.partition("_gjnt")
            tmpName = splitString[0]
    
            markName = (tmpName + "_boneMarking")
                    
            try:
                cmds.setAttr (joint + '.boneType', markName, type="string" )
            except:
                cmds.addAttr (ln="boneType", nn= 'BoneType', dt='string', k=False)
                cmds.setAttr (joint + '.boneType', markName, type="string" )
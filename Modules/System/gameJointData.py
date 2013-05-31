""" The way I am determining joint names and parent joint is crap.  The concept is sound but the tool is not innately designed to support that.  
User defined names must be formated like this (arm__li1, arm__mi1)"""

import os
import maya.cmds as cmds
import pymel.core as pm
from functools import partial

import System.turbineSpecificUtils as turbineUtils
reload(turbineUtils)

import System.utils as utils
reload(utils)

import System.userUtils as userUtils
reload(userUtils)

import csv

import __main__

# Used to attach geometry

class gameJoint_Data():    
    def __init__(self):
        """ Initialize class and variables """
        
    def initCsvReader(self, characterName):
        
        self.characterName = characterName

        # Define the file name and path        
        userName = userUtils.getUser()[0]
        outFileSuffix = '_gameJntInfo.csv'
        outFile = (characterName + outFileSuffix )

        """ Define the artPath """
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()
        artPath = dirExt.artPath
            
        filePath = artPath + "/character/GEPPETTO/Data/Character/" 
        
        finalPath = (filePath  + outFile)
        
        reader = csv.reader(open(finalPath, 'rb'), delimiter=',')
        
        return reader
    
    def getUserSpecNameFromHook(self, hookObject):
        tmpPrefix = hookObject.partition("__")[2]
        userSpecFromHook = tmpPrefix.partition(":")[0]
        userSpecFromHook = userSpecFromHook.replace("__", "_")
        jntInt = self.getNumJtsInHook(hookObject)
        prefix = userSpecFromHook.partition("_")[0]
        suffix = userSpecFromHook.partition("_")[2]
        userSpecFromHook = (prefix + jntInt + "_" + suffix)

        return userSpecFromHook
    
    def getNumJtsInHook(self, hookObject):
        p1 = hookObject.partition(":")[2]
        p2 = p1.replace("_joint_translation_control", "")
        p3 = p2.partition("_")[2]
        
        instNum = p3
        return instNum

    
    def pruneInstName(self, moduleNamespace):
        instNameVar = moduleNamespace.partition("__")[2]
        instNameVar = instNameVar.partition(":")[0]
        instNameVar = instNameVar.replace("instance_", "i")
        
        return instNameVar
    
    def pruneUSpecName(self, userSpecifiedName):
        instNameVarA = userSpecifiedName.partition("__")[0]
        instNameVarB = userSpecifiedName.partition("__")[2]

        return (instNameVarA, instNameVarB) 
        
        

    def getTranslationControls(self, containerName):
        allTransControls = []
        
        transControl = pm.container(containerName, query=True, nodeList=True, ish=False, isd=False, inc=True )

        for control in transControl:

            suffix = "joint_translation_control_container"        
            result = control.endswith(suffix)
        
            if result == True:
                control = control.replace("_container", "")
                allTransControls.append(control)
        
        return allTransControls
        
           
        
    """ This def will collect the following information."""
    """ game_joint name, blueprint joint name, parent name, rotation order, and orientation """    
    def getGJNames(self, containerName, moduleInfo, jointInfo, userSpecifiedName):  
        """ Get all the attributes we need into a list """        
        """  I am changing the way we get the parent joint and game joint names.  I do not need a new attr because the info is already
        contained in the module via the "gameJntNames and hookObject """
        blueprintJointNames = []
        gameJointNames = []
        parentJointNames = []
        jointRotateOrder = []
        jointOrient = []
        jointOrientX = []
        jointOrientY = []
        jointOrientZ = []
        jointPositionX = []
        jointPositionY = []
        jointPositionZ = []
 
        """ Get the namespace from the module container """
        nameSpace = containerName.replace("module_container", "")        
        moduleNamespace = moduleInfo[6]
        
        """ Get game joint names """   
        
        for index in range(len(jointInfo)):
            instPrefix = self.pruneUSpecName(userSpecifiedName)[0]
            instSuffix = self.pruneUSpecName(userSpecifiedName)[1]
            jointNum = str(index + 1)

            joint = (instPrefix + jointNum + "_" + instSuffix + "_gjnt")

            gameJointNames.append(joint)
            

            
        """ Get blueprint joint names """
        for info in jointInfo:
            bpSufix = info[0]
            bpJointName = (nameSpace + "blueprint_" + bpSufix)            
            blueprintJointNames.append(bpJointName)
    
        """ Get the position """
        jointPosition = (moduleInfo)[0]
        for pos in jointPosition:
            
            jointPositionX.append(pos[0])
            jointPositionY.append(pos[1])
            jointPositionZ.append(pos[2])
                       
        """ get the joint orientations """
        jointOrientations = moduleInfo[1]
        """ Determine how the joint is oriented """
        orientWithAxis = False
        pureOrientations = False
        if jointOrientations[0] == None:
            orientWithAxis = True
            jointOrientations = jointOrientations[1]
        else:
            pureOrientations = True
            jointOrientations = jointOrientations[0]
        
        numOrientations = len(jointOrientations)
        numJoints = len(jointInfo)      
        
        for i in range(numJoints):
            if orientWithAxis:
                # Spine breaking because jointOrient passed without a value.  Adding this for testing
                jointOrientation = [0.0, 0.0, 0.0]
                if i != 0:
                    offsetIndex = i-1
                    if offsetIndex < numOrientations:
                        jointOrientation = (jointOrientations[offsetIndex][0])

            else:                
                jointOrientation = [0.0, 0.0, 0.0]
                if i < numOrientations:
                    jointOrientation = [jointOrientations[i][0],jointOrientations[i][1],jointOrientations[i][2]]
            
            jointOrient.append(jointOrientation) 
 
        """ Split the vars into axis """
        for orient in jointOrient:
            jointOrientX.append(orient[0])
            jointOrientY.append(orient[1])
            jointOrientZ.append(orient[2])

      
        """ Retrieve the parent joint """
        hookObject = moduleInfo[4]

        if hookObject == None:
            parentJointNames.append("None")
        if hookObject != None:
            userSpecFromHook = self.getUserSpecNameFromHook(hookObject)

            parentName = (userSpecFromHook + "_gjnt")
            parentJointNames.append(parentName)
            
        for index in range(len(gameJointNames)):
            current = gameJointNames[index]
            if current == gameJointNames[0]:
                pass
            else:
                parent = (gameJointNames[index -1])
                if parent not in parentJointNames:
                    parentJointNames.append(parent)
        
         
        """ Get the rotateOrder from the translation control """
        attrs = cmds.listAttr(containerName)

        for attr in attrs:
          
            roSuffix = "rotateOrder" 
            result = attr.endswith(roSuffix)
            if result == True:
                roAttr = cmds.getAttr(containerName + "." + attr)
                jointRotateOrder.append(roAttr)
            else:
                """ This breaking on select modules """
                jointRotateOrder.append(0)
                
 
        self.storeJointVars(gameJointNames, parentJointNames, jointPositionX, jointPositionY, jointPositionZ, jointRotateOrder, blueprintJointNames, jointOrientX, jointOrientY, jointOrientZ, containerName)

     
    def storeJointVars(self, gameJointNames, parentJointNames, jointPositionX, jointPositionY, jointPositionZ, jointRotateOrder, blueprintJointNames, jointOrientX, jointOrientY, jointOrientZ, containerName):  
        # Define the file name and path        
        userName = userUtils.getUser()[0]
        outFileSuffix = '_gameJntInfo.csv'
        outFile = (userName + outFileSuffix )
        

        """ Define the artPath """
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()
        artPath = dirExt.artPath
            
        filePath = artPath + "/character/GEPPETTO/Data/" 
        
        finalPath = (filePath  + outFile)
             
        for index in range(len(gameJointNames)):
            int = str(index)

            value = (gameJointNames[index], parentJointNames[index], jointPositionX[index], jointPositionY[index], jointPositionZ[index], jointRotateOrder[index], blueprintJointNames[index], jointOrientX[index], jointOrientY[index], jointOrientZ[index])  
        
            writer = csv.writer(open(finalPath, "a"))                
            writer.writerow(value)

        """ I need to make sure the file closes here """            
        # Close the file
        #file.close(finalPath)
        
        cmds.headsUpMessage("The temp data file has been saved to " + finalPath)       
        
        
    def loadJointVars(self, characterName):
        self.characterName = characterName
        # Define the file name and path        
        reader = self.initCsvReader(characterName)
      
        gameJoints = []
        numRows = []

        for row in reader:
            numRows.append(row)   
            gjntData = list(row)
            gameJoints.append(gjntData[0])
            self.createGameJoint(gjntData)

        return gameJoints

            
    def createGameJoint(self, gjntData):
        self.gjntData = gjntData
        """ The game joint name"""
        jntName = self.gjntData[0]
        """ Create the game joint"""
        cmds.select(d=True)
        newJoint = cmds.joint(n=jntName)
        """ Position the joint """
        cmds.xform(newJoint, ws=True, t=(self.gjntData[2],self.gjntData[3],self.gjntData[4]))  
        
        """ Set the Rotate Order """
        orderValue = float(gjntData[5])
        cmds.setAttr(newJoint + ".rotateOrder", orderValue)


    def orientJoints(self):
        # Define the file name and path        
        reader = self.initCsvReader()
        
        gameJoints = []
        parentJoints = []
        numRows = []
        
        for row in reader:
            numRows.append(row)   
            gjntData = list(row)
            gameJoints.append(gjntData[0])
         
            newJoint = gjntData[0]
           
            """ Set the orientation """
            """ Using the DataBase will remove the need for changing to float. """ 

            orientValueX = float(gjntData[7])
            orientValueY = float(gjntData[8])
            orientValueZ = float(gjntData[9])
  
            cmds.setAttr(newJoint + ".jointOrientX", orientValueX)
            cmds.setAttr(newJoint + ".jointOrientY", orientValueY)
            cmds.setAttr(newJoint + ".jointOrientZ", orientValueZ)
            
            cmds.makeIdentity(newJoint, apply=True, rotate=True)
            
    def altOrientJoints(self, characterName):
        # Define the file name and path        
        reader = self.initCsvReader(characterName)
        
        gameJoints = []
        parentJoints = []
        numRows = []
        
        for row in reader:
            numRows.append(row)   
            gjntData = list(row)
            gameJoints.append(gjntData[0])
        for joint in gameJoints:
            cmds.makeIdentity(joint, apply=True, rotate=True)
            cmds.select(joint)
            cmds.joint(e=True, zso=True, oj='xyz')
            cmds.makeIdentity(joint, apply=True, rotate=True)
    


    def gameJointHierarchy(self, characterName):
        # Define the file name and path        
        reader = self.initCsvReader(characterName)
        
        numRows = []
        gameJoints = []
        parentJoints = []
        
        for row in reader:
            numRows.append(row)   
            gjntData = list(row)
            gameJoints.append(gjntData[0])
            parentJoints.append(gjntData[1])
   
        for index in range(len(gameJoints)):
            if parentJoints[index] != "None":
                cmds.parent(gameJoints[index], parentJoints[index])

        
    def saveDelCharFile(self, characterName):
        """ This process happens at character publish.  The temp .csv file will be saved to a new directory with the character name as prefix """
        self.characterName = characterName
        """ Write the csv with all the character info """                
        """ Define the artPath """
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()
        artPath = dirExt.artPath

        # Define the file name and path        
        userName = userUtils.getUser()[0]
        
        outFileSuffix = '_gameJntInfo.csv'
        outFileSuffixBU = '_gameJntInfo_BU.csv'
        
        outFileD = (userName + outFileSuffix )# Delete this
        outFileS = (self.characterName + outFileSuffix )# Save as this
        outFileBU = (self.characterName + outFileSuffixBU )# Save as this
    
    
        filePath = artPath + "/character/GEPPETTO/Data/" 
        filePathS = artPath + "/character/GEPPETTO/Data/Character/" 
        filePathBU = artPath + "/character/GEPPETTO/Data/Character/BU/" 
        
        finalPathD = (filePath  + outFileD)
        finalPathS = (filePathS  + outFileS)
        finalPathBU = (filePathBU + outFileBU)
              
        if cmds.file(finalPathS, q=True, ex=True):
            turbineUtils.archiveFile(finalPathS)

        
        if cmds.file(finalPathD, q=True, ex=True):
            import shutil
            shutil.copy(finalPathD, finalPathS)
            os.remove(finalPathD)
        else:
            cmds.headsUpMessage("No character data file exists for publish.  Please lock a character.")
                        
    def parentGameToBlueprint(self, characterName, characterNamespace):
        # Define the file name and path        
        reader = self.initCsvReader(characterName)
        
        gameJoints = []
        parentJoints = []
        numRows = []
        parentConstraints = []
        
        for row in reader:
            numRows.append(row)   
            gjntData = list(row)
            gameJoints.append(gjntData[0])
            parentJoints.append(gjntData[6])
        for index in range(len(gameJoints)):
            bpJoint = (characterNamespace + ":" + parentJoints[index])
            if cmds.objExists(gameJoints[index]):
                parentConstraint = cmds.parentConstraint(bpJoint, gameJoints[index], mo=True)
                scaleConstraint = cmds.scaleConstraint(bpJoint, gameJoints[index])
                parentConstraints.append(parentConstraint)
                parentConstraints.append(scaleConstraint)
            else:
                print (gameJoints[index] + 'is missing')
            
        return parentConstraints

                   
    def buildGameSkel(self):

        self.loadJointVars()
        self.gameJointHierarchy()
        self.altOrientJoints()
        

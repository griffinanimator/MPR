import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils



def jointRename(self): 
    # Find the setup group
    setupGrp = "Setup_grp"
    # Find and unlock the setup container
    setupContainer = cmds.container(q=True, fc=setupGrp)
    cmds.lockNode(setupContainer, l=False, lu=False)
    
    # find all the game joint by querying the contents of the container.
    setupNodes = cmds.container(setupContainer, q=True, nl=True) 

    # If the joint is the last in a chain, we need to make sure we add "cap" to the name.
    for nodes in setupNodes:
        isEndJoint = cmds.listConnections(nodes, s=False, d=True, t="joint")   
        if isEndJoint == None:
            newName = nodes.replace("_game", "_game_cap")
            if cmds.objExists(newName):
                pass
            else:
                cmds.rename(nodes, newName)

    cmds.lockNode(setupContainer, l=True, lu=True)


# This function will return all the character specific paths and names
#  If needed, will also setup the directories.    
def setupDirs(self, characterName, create=False): 
    import tsapi.core.environment as environment
    reload(environment)  
    
    #characterName = self.characterName

    # get the path to source art
    environment = environment.environment()
    
    """ Using this to switch art path for now """
    #artPath = environment.paths['art_source']
    artPath = "Z:\\\\art\\"
 
    characterDir = artPath + "Product_Art\\Characters\\" + characterName
    setupDir = characterDir + "\\Setup\\"

    xmlDir = characterDir + "\\XML\\"
    rigDir = artPath + "Product_Art\\Characters\\GEPPETTO\\" 
    skinDir = characterDir + "\\Skin\\"
    
    # Specific paths to specific character files

    characterFileName = rigDir + characterName + ".ma" 
    setupFileName = setupDir + characterName + "_setup" + ".ma"
    xmlFileName = xmlDir + characterName + "_xml" + ".xml"
    
    #characterNameString = (characterNamespace + ":")
        
    # I am going to create a directory setup for this character if one does not exist. 
    if create:
        directories = (characterDir, setupDir, xmlDir, rigDir, skinDir)
        for dir in directories:
            try:
                os.makedirs(dir)            
            except OSError:
                pass
            
    # Should we try to create the directory if it does not exist?
    # The user may have deleted it.
          
    return (characterDir, setupDir, xmlDir, rigDir, skinDir, characterFileName, setupFileName, xmlFileName)

def getCharacterNamespace(self, characterName):
    #characterName = self.characterName

    baseNamespace = "Character__" + self.characterName + "_"
    extraNamespace = "Export__" + self.characterName + "_"
        
    cmds.namespace(setNamespace=":")
    namespaces=cmds.namespaceInfo(listOnlyNamespaces=True)
        
    highestSuffix = utils.findHighestTrailingNumber(namespaces, baseNamespace)
    highestSuffix += 1
        
    characterNamespace = baseNamespace + str(highestSuffix)

    exportNamespace = extraNamespace + str(highestSuffix)
    
    
    return (characterNamespace, exportNamespace)
            
        
# I need to replace the function from utils that saves/loads files from a relative directory.  This is only used to find the rig file.
# relative director refers to a path variable the user passes when calling the function.
def findAllRigFiles(relativeDirectory):
    return findAllFiles(relativeDirectory, ".ma")
    

"""  I need to be able to use this on a directory passed in as a string"""
def findAllFiles(relativeDirectory, fileExtension):
    # get the path to source art
    import tsapi.core.environment as environment
    reload(environment)

    environment = environment.environment()
    
    
    """ Using this to switch art path for now """
    #artPath = environment.paths['art_source']
    artPath = "Z:\\\\art\\"
    
    rigDir = artPath + "Product_Art\\Characters\\" 
        
    # Search the relative directory for all files with the given extension.
    # Return a list of all file names, excluding the file extension

    fileDirectory = rigDir + "/" + relativeDirectory + "/"
    
    allFiles = os.listdir(fileDirectory)
    
    # Refine all files, listing only those of the specified file extension
    returnFiles = []
    for f in allFiles:
        splitString = str(f).rpartition(fileExtension)
        
        if not splitString[1] == "" and splitString[2] == "":
            returnFiles.append(splitString[0])

    return returnFiles




def boneMarking():
    import tsapi.core.maya.joint as joint
    reload (joint)
    
    # Use the joint class to identify the joints in the scene
    joint = joint.joint()
    ignoreBones = joint.GetGameJointInfo()[2]
    bindJoints = joint.GetGameJointInfo()[0]
    
    for joint in ignoreBones:
        cmds.select (joint)
        try:
            cmds.setAttr (joint + '.boneType', "ignore", type="string" )
        except:
            cmds.addAttr (ln="boneType", nn= 'BoneType', dt='string', k=False)
            cmds.setAttr (joint + '.boneType', "ignore", type="string" )
            
    for joint in bindJoints:
        cmds.select (joint)
        splitString = joint.partition("_game_")
        tmpName = splitString[0]

        markName = (tmpName + "_boneMarking")
                
        try:
            cmds.setAttr (joint + '.boneType', markName, type="string" )
        except:
            cmds.addAttr (ln="boneType", nn= 'BoneType', dt='string', k=False)
            cmds.setAttr (joint + '.boneType', markName, type="string" )
            

            
def loadHoldLocs():
    import xml.dom.minidom
    import xml.dom
    import tsapi.core.maya.joint as joint
    reload (joint)

    # The name of the holding location
    allLocs=[]
    
    # Use the joint class to identify the joints in the scene
    joint = joint.joint()
    bindJoints = joint.GetGameJointInfo()[0]
    
    if bindJoints == None:
        cmds.headsUpMessage( 'No game joints exist in this scene.  Holding locations will not be added.')
        return
    else:
        # We should create a holding loc for each game joint.    
        cmds.select( clear=True )
        #listJoints=[]
        # open the xml file for reading 
        fileObject = file("Z://geppetto/holdLocList.xml", 'r')
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
                jointPos = cmds.xform(jointName, q=True, ws=True, t=True)
                # Final name for the holding location 
                                                        
                locName = ("HoldingLocation_" + jointName + "_" + locValue)
        
                allLocs.append(locName)

                locGrp = pm.group(em=True, w=True, n=locName)

                """ Once the group is created, I get a |  at the begining of the name. WTF??? """
                locGrp = cmds.ls(sl=True)
                locGrp = (locGrp)[0]

                # Move locGrp to joints position
                cmds.xform(locGrp, t=jointPos)
                # Add an "LocationType" attr to the holding loc
                cmds.addAttr(ln="LocationType", dt="string", k=False)
                cmds.setAttr(locGrp+".LocationType", locValue, type="string")
                # parent the holdLoc to the joint
                cmds.parent(locGrp, jointName)
                  
        # close the file
        fileObject.close()
        
        return allLocs

           
            
def blueprintToGameName(self, capJoint, joint, capVar=True):
    self.capJoint = capJoint
    self.joint = joint
    self.capVar = capVar
    if self.capVar == True:
        nameVar1=self.capJoint
        nameVar2="_cap_game_joint"
    if self.capVar == False:
        nameVar1=self.joint
        nameVar2="_game_joint"
        
    # Create a name to use for the game joint                                                                    
    midName = nameVar1.replace("_joint", "")                                         
    tmpName = midName.split("blueprint")
                                                                                    
    tmpPrefix = utils.stripLeadingNamespace(tmpName[0])
    tmpName1 =  (tmpPrefix[0] + tmpName[1])
    tmpName2 = tmpName1.split("__")
    gameJointName = (tmpName2[1] + nameVar2)
    
    return gameJointName

def createGameJointAttrs(gameJoint, parentObject, joint):
    
    # Create attributes on the game joint to define 
    #(parent, corresponding BP joint name, position, rotate order and orientation)
    cmds.select(gameJoint)
    cmds.addAttr(longName="parentJoint", k=True, dt="string")
    cmds.setAttr(gameJoint +".parentJoint", parentObject,  type="string")
                        
    # Make bp joint attr
    cmds.addAttr(longName="bpJoint", k=True, dt="string")
    cmds.setAttr(gameJoint +".bpJoint", joint,  type="string")
    # Joint position
    jointPos = cmds.xform(joint, q=True, ws=True, t=True)
    cmds.xform(gameJoint, ws=True, t=jointPos)
    # Rotate order
    jointRotOrder = cmds.getAttr(joint + ".rotateOrder")
    cmds.setAttr(gameJoint + ".rotateOrder", jointRotOrder)
    # Orient
    jointOrientX = cmds.getAttr(joint + ".jointOrientX")
    jointOrientY = cmds.getAttr(joint + ".jointOrientY")
    jointOrientZ = cmds.getAttr(joint + ".jointOrientZ")
    cmds.setAttr(gameJoint + ".jointOrientX", jointOrientX)
    cmds.setAttr(gameJoint + ".jointOrientY", jointOrientY)
    cmds.setAttr(gameJoint + ".jointOrientZ", jointOrientZ)
    
    
    
def getCharacterInfo(self):
    cmds.namespace(set=":")
    namespaces = cmds.namespaceInfo(lon=True)
    characterName = []
    for name in namespaces:        
        characterContainer = (name + ":character_container")
        if cmds.objExists (characterContainer):
            fullCharName = name
            tmpCharName = name.split("__")[1]
            tmpCharName = tmpCharName[:tmpCharName.rfind("_")]
            characterName = tmpCharName 
            return (characterName, characterContainer, fullCharName)  
                  
        else:
            # Warn no character in the scene
            charConfirm = ("No character exists in this scene")
            cmds.confirmDialog(messageAlign="center", title="Create Directory", message= charConfirm)
            


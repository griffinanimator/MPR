import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import __main__

# This function will return all the character specific paths and names
#  If needed, will also setup the directories.    
def setupDirs(characterName, create=False):  
    
    """ Using this to switch art path for now """
    """ Define the artPath """
    import System.directoryExtension as directoryExtension
    dirExt = directoryExtension.DirectoryExtension()
    artPath = dirExt.artPath

    
    characterDir = artPath + "character\\" + characterName
        
    setupDir = characterDir + "\\export\\"
    xmlDir = artPath + "character\\GEPPETTO\\Data\\"
    rigDir = artPath + "character\\GEPPETTO\\Rig\\" 
    skinDir = characterDir + "\\skin\\"
    meshDir = characterDir + "\\mesh\\"
    #setDir = characterDir + "\\setup\\"
    wipDir = characterDir + "\\rig\\wip\\"
    
    # Specific paths to specific character files

    characterFileName = rigDir + characterName + ".ma" 
    #setupFileName = setupDir + characterName + "_setup" + ".ma"
    setupFileName = setupDir + characterName + ".ma"
    xmlFileName = xmlDir + characterName + "_xml" + ".xml"

        
    # I am going to create a directory setup for this character if one does not exist. 
    if create:
        #directories = (characterDir, setupDir, xmlDir, rigDir, skinDir)
        directories = (characterDir, setupDir, skinDir, wipDir)
        for dir in directories:
            try:
                os.makedirs(dir)            
            except OSError:
                pass
            
    # Should we try to create the directory if it does not exist?
    # The user may have deleted it.
          
    return (characterDir, setupDir, xmlDir, rigDir, skinDir, characterFileName, setupFileName, xmlFileName, meshDir)

def getCharacterNamespace(characterName):

    baseNamespace = "Character__" + characterName + "_"
    extraNamespace = "Export__" + characterName + "_"
        
    cmds.namespace(setNamespace=":")
    namespaces=cmds.namespaceInfo(listOnlyNamespaces=True)
        
    highestSuffix = utils.findHighestTrailingNumber(namespaces, baseNamespace)
    highestSuffix += 1
        
    characterNamespace = baseNamespace + str(highestSuffix)

    exportNamespace = extraNamespace + str(highestSuffix)
    
    return (characterNamespace, exportNamespace)


def getCharacterInfo():
    cmds.namespace(set=":")
    namespaces = cmds.namespaceInfo(lon=True)
    characterName = []
    for name in namespaces: 
        """ TODO: """
        """ I need a global check for valid characters in the scene """
        characterContainer = (name + ":character_container")
        setupContainer = name.replace("Character__", "Export__")
        setupContainer = (setupContainer + ":Setup")

        if cmds.objExists (characterContainer):
            fullCharName = name
            tmpCharName = name.split("__")[1]
            tmpCharName = tmpCharName[:tmpCharName.rfind("_")]
            characterName = tmpCharName
            return (characterName, characterContainer, fullCharName, setupContainer)  
                  
        else:
            characterContainer = 'Character__tmp_1:character_container'
            fullCharName = name
            tmpCharName = name.split("__")[1]
            tmpCharName = tmpCharName[:tmpCharName.rfind("_")]
            characterName = tmpCharName

            return (characterName, characterContainer, fullCharName, setupContainer)
            # Warn no character in the scene
            #charConfirm = ("No character exists in this scene")
            #cmds.confirmDialog(messageAlign="center", title="Create Directory", message= charConfirm)
            characterName = 'Character__tmp'
            return characterName
            
        
# I need to replace the function from utils that saves/loads files from a relative directory.  This is only used to find the rig file.
# relative director refers to a path variable the user passes when calling the function.
def findAllRigFiles(relativeDirectory):
    return findAllFiles(relativeDirectory, ".ma")

"""  I need to be able to use this on a directory passed in as a string"""
def findAllFiles(relativeDirectory, fileExtension):
    
    """ Using this to switch art path for now """
    """ Define the artPath """
    import System.directoryExtension as directoryExtension
    dirExt = directoryExtension.DirectoryExtension()
    artPath = dirExt.artPath
    
    rigDir = artPath + "character/" 
        
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



""" Re-writing the functions that generate the game joints and holding locs """

""" Find containers would be a good general util """
def findModuleContainers():    
    # Get all the module_containers
    allContainers = []
    containerNodes = pm.ls(type="container")
    
    for container in containerNodes:
        #selContainer = container.encode("ascii","ignore")
  
        suffix = "module_container"
        
        result = container.endswith(suffix)
        
        if result == True:
            allContainers.append(container)

    return allContainers

def findTransControlContainers():    
    # Get all the module_containers
    allTransContainers = []
    containerNodes = pm.ls(type="container")
    
    for container in containerNodes:
  
        suffix = "translation_control_container"
        
        result = container.endswith(suffix)
        
        if result == True:
            allTransContainers.append(container)

    return allTransContainers

def extractGameJointData():
    """ Queries the blueprint modules to get the game joint name, associated blueprint joint,
    parent, and position """
    """ Find all the bluprint translation controls """
    return findModuleContainers()

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        print "Dir Created"
        
def archiveFile(file):  
    import userUtils as userUtils
    import shutil
    
    # Define the file name and path        
    userName = userUtils.getUser()[0]
    
    """ Get the current date and time to use as the backup name """
    import datetime
    now = datetime.datetime.now()
    dateTime = now.strftime("%Y-%m-%d-%M")
    
    """ Define a suffix to add to the file path """
    fileSuffix = (userName + dateTime)
    
    """ Define a new file path """
    filePartition = file.rpartition('/')
    bakFile = ('/' + fileSuffix + '_' + filePartition[2] )
    bakFilePath = (filePartition[0] + '/Bak' + bakFile) 
            
    if cmds.file(file, q=True, ex=True):
        cmds.headsUpMessage("This file already exists" + file + ".  Backing it up.")
        shutil.copy(file, bakFilePath) 
        
def traverseDirectory(directory):
    print directory
    
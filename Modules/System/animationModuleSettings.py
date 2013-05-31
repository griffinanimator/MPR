import maya.cmds as cmds

import System.utils as utils
reload(utils)

from ctypes import *

from System.userUtils import getUser

import csv

class AnimMod_Info():
    def __init__(self, *args):
        """ Create a dictionary to store the character name
        Run a function to get character name """
        self.characterInfo = {}
        try:
            self.characterInfo['characterNamespace'] = self.findCharacterNames()[0]
            self.characterInfo['characterName'] = self.findCharacterNames()[1]
        except: return
        

        import System.moduleMaintenanceEx as moduleMaintenance
        #modMaintenance = moduleMaintenance.ModuleMaintenanceEx(self)
        import System.directoryExtension as dirExt
        dirExt = dirExt.DirectoryExtension()
        self.animDir = dirExt.paths['animLib']
         
    def write_rig_settings(self, customName):
        animModAttrSettings = []
        animModInfo = self.animModInfo()

        for each in animModInfo:
            """ Remove the character name and save to a new list """
            animModAttr = each[0].replace(self.characterInfo['characterName'], "")
            animModAttrSettings.append([animModAttr, each[1]])
        
        """ get the last frame of the animation """
        endFrame = self.endFrame()
        animModAttrSettings.append(['endFrame', endFrame])
        
                    
        """ This is the path where the csv will be written. """
        characterName = self.characterInfo['characterName']
        characterName = self.shortenCharacterName()
        fileName = (self.animDir + characterName + '/' + customName + "_rigSettings.csv")
        print fileName    
        self.writeAnimAttrs(animModAttrSettings, fileName)
        
        
    def load_rig_settings(self, currentDirectory, customName):
        animModAttrSettings = []
        endFrame = []
        
        fileName = (currentDirectory + customName + "_rigSettings.csv")

        if cmds.file(fileName, q=True, exists=True):
            animModAttr = self.readAnimAttrs(fileName)
            """ Add the character name to the attribute """
            
            for each in animModAttr:

                if each[0] != 'endFrame':
                    attribute = (self.characterInfo['characterName'] + each[0])
                    animModAttrSettings.append([attribute, each[1]])              
                else:          
                    animModAttrSettings.append([each[0], each[1]])
            
            missingControls = self.missingControls(animModAttrSettings)
            #self.installAnimModFromCsv(missingControls)

            self.setAttrsFromModInfo(animModAttrSettings)                
            return missingControls
        
        else:
            cmds.headsUpMessage (fileName + " Not on disk")
            
    def setAttrsFromModInfo(self, animModAttrSettings): 
        allAnimNodes = [] 
        print ' SetAttrFromModInfo'   
        for each in animModAttrSettings:
            
            attribute = each[0]
            value = float(each[1])

            if attribute != 'endFrame':   
                """ Strip the attribute down to the node name""" 
                """so we can verify it exists """           
                animNode = self.stripAttrNameFromGrp(attribute)

                
            
 
                if cmds.objExists(animNode) == True:
                    try:
                        cmds.setAttr(attribute, value)
                    except: 
                        print (attribute + " .........could not be set ")
                    #else:
                        #try:
                            #self.installAnimModFromCsv(animNode)
                        #except:
                            #pass
                        
            else:
                cmds.playbackOptions( minTime='0sec', maxTime=value)
                        
    
    """ Functions to read and write data to csv """
    """ Make this a base class """
    def writeAnimAttrs(self, animModInfo, fileName):      
        path = (fileName)
    
        """ Open the csv in maya for writing """
        writer = csv.writer(open(path, 'wb'), delimiter=',') 
        
        for info in animModInfo: 
            writer.writerow(info)  
            
    def readAnimAttrs(self, fileName):  
        attrs = []
        
        reader = csv.reader(open(fileName, 'rb'), delimiter=',', quotechar='"')
        
        for row in reader:
            attrs.append(row)
      
        return attrs        
        
    def animModInfo(self):
        """ Call on getInstalledAnimModules to get bp mod name, anim mod class
        and anim mod container name"""
        modSets = self.getModuleInformation()
        
        """ Create an empty list to store all the info retrieved from getAnimModAttrs """
        animModInfo = []

        for set in modSets: 
            animContainer = set[2]
            moduleContainer = set[3]
            moduleGroup = set[4]
            blueprintContainer = moduleContainer.replace("module_container", "blueprint_container")
            animModAttrs = self.getAnimModAttrs(moduleGroup, moduleContainer)
        
            for attr in animModAttrs:
                animModInfo.append(attr)
                
        """ If no mods exist, a character is probably not installed """
        if animModInfo == None:
            cmds.headsUpMessage ("No character in the scene ")
        
        return animModInfo
        
    def findCharacterNames(self, *args):
        characterNamespace = utils.findInstalledCharacters()
        if len(characterNamespace) != 0:
            characterNamespace = characterNamespace[0]
    
            characterName = (characterNamespace)
        else:
            cmds.headsUpMessage("No valid character in the scene")
            return

        return (characterNamespace, characterName)   
        
                
    def getModuleInformation(self):
        modSets = []
        
        """ Find the character_container """
        character = self.characterInfo['characterNamespace']
        fullCharacterNamespace = (character + ':')
        
        characterContainer = character + "character_container"
 
        """ Find the blueprint modules in the scene"""  
        blueprintInstances = utils.findInstalledBlueprintInstances(character)   
        
        for blueprintInstance in blueprintInstances:
            moduleContainer = fullCharacterNamespace + blueprintInstance+":module_container"
           
            """ Do we have animation modules installed? """
            blueprintJointsGrp = fullCharacterNamespace + blueprintInstance+":blueprint_joints_grp"
            
            if cmds.getAttr(blueprintJointsGrp+".controlModulesInstalled"):
                nodes = cmds.container(moduleContainer, q=True, nl=True)
                for node in nodes:
                    suffix = ":module_container"  
                    result = node.endswith(suffix)  
                    if result == True:
                        """ The module container holds all the attr info we need to save"""
                        animContainer = node
                        tmpVar = node.rpartition(":module_container")
                        tmpVar = tmpVar[0].rpartition(":")
                        className = tmpVar[2]
                        
                        """ Get the module group """
                        containerNodes = cmds.container(node, q=True, nl=True)
                        for node in containerNodes:
                            suffix = ":module_grp"  
                            result = node.endswith(suffix)  
                            if result == True:
                                moduleGroup = node
     
                        modSets.append([blueprintInstance, className, animContainer, moduleContainer, moduleGroup])
                         
        return (modSets) # Contains the bp module name, anim mod class name, anim mod container
    
    """ Get all the attribute value needed to configure the rig """
    def getAnimModAttrs(self, moduleGroup, moduleContainer):
        """ Get the attrs we need from the module_group """
        moduleGroupAttrs = cmds.listAttr(moduleGroup)
        
        """ Empty list for storing attributes and values """
        animSettings = []

        for attr in moduleGroupAttrs:
            """ I want to capture the following attrs """
            targetAttrs = ("lod", "iconScale", "overrideColor")
            for tAttr in targetAttrs:
                result = attr.endswith(tAttr)  
                if result == True:
                    finAttr = (moduleGroup + "." + attr)
                    val = cmds.getAttr(finAttr)
                    try:
                        val = str("%.2f" % val)
                    except: pass
                    """ Append the attribute and value to animSettings """
                    animSettings.append([finAttr, val])
                    
        
        """ Get the attrs we need from the SETTINGS """ 
        """ Get the settings locator by replacing :module_container with :SETTINGS """
        settingsLocator = moduleContainer.replace(":module_container", ":SETTINGS")
        
        settingsLocatorAttrs = cmds.listAttr(settingsLocator)
        for attr in settingsLocatorAttrs:
            """ I want to capture the following attrs """
            targetAttrs = ("weight", "creationPoseWeight", "activeModule")
            for tAttr in targetAttrs:
                result = attr.endswith(tAttr)  
                if result == True:
                    finAttr = (settingsLocator + "." + attr)
                    val = cmds.getAttr(finAttr)
                    try:
                        val = str("%.2f" % val)
                    except: pass
                    """ Append the attribute and value to animSettings """
                    animSettings.append([finAttr, val]) 
                    
        return animSettings 
    

    
    def stripAttrNameFromGrp(self, attribute):
        node = attribute.partition(".")[0]
        return node
    
    def endFrame(self):
        lastFrame = cmds.playbackOptions( query = True, max = True )
        return lastFrame
    
    def shortenCharacterName(self):

        characterNamespace = self.characterInfo['characterName']
        
        """ Get the character name.   Need a better util for this """
        tmpCharName = characterNamespace.partition("__")[2]
        characterShortName = tmpCharName.rpartition("_")[0]
        return (characterShortName)
    
    """ Locate the controls that were installed when the animation was saved """
    def missingControls(self, animModAttrSettings):
        missingControls = []
        for each in animModAttrSettings:
            """ Strip the attribute down to the node name""" 
            """so we can verify it exists """           
            animNode = self.stripAttrNameFromGrp(each[0])
            
            if cmds.objExists(animNode)== False:
                
                if animNode not in (missingControls):
                    missingControls.append(animNode)
                            
        return missingControls
               
                
    """ The final step is to create the control if it does not exist """
    """ I will need to access controlModule """
    """ Extract the name of the missing module and the blueprint to install it on """
    def installAnimModFromCsv(self, missingControls):
        print "Install Mod ............................"
        for animNode in missingControls:
            module_group = animNode.replace(self.characterInfo['characterNamespace'], "")
            anim_moduleIns = module_group.replace(":module_grp", "")
            bpMod = anim_moduleIns.partition(":")[0]
            animMod = anim_moduleIns.partition(":")[2]

        """ This loads module maintenance and places the character in mm mode """
        import System.moduleMaintenanceEx as moduleMaintenanceEx
        moduleMaintenance = moduleMaintenanceEx.ModuleMaintenanceEx()
        
        blueprintContainer = (self.characterInfo['characterName'] + ":" + bpMod + ":blueprint_container")
        cmds.select(blueprintContainer)
        
        moduleMaintenance.setModuleMaintenanceVisibility(vis=True)
        
        moduleMaintenance.objectSelected()
        
        controlModSelected = moduleMaintenance.controlModuleSelected(animMod)
        
        moduleMaintenance.setModuleMaintenanceVisibility(vis=False)
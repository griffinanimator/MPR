import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.turbineSpecificUtils as turbineUtils
import System.referenceUtils as referenceUtils

import animationModuleSettings as animModSettings

import System.utils as utils


"""
TODO:
    TEST MULTIPLE CHARACTERS IN THE SCENE
"""

""" Currently I am only saving keys set by the animator.  We may want to get all the space switching and custom stuff as well"""

class AnimLib_UI():    
    def __init__(self, *args):
        import System.directoryExtension as dirExt
        reload(dirExt)
        dirExt = dirExt.DirectoryExtension()
        self.animDir = dirExt.paths['animLib']
        
        """
        TODO:
            MOVE ALL FILE FINDING UTILS INTO A CLASS
        """
        """ Find all the valid rigs and store them in a dictionary """
        self.rigFiles = {}
        self.rigs = {}
        
        refUtils = referenceUtils.Reference_Utils()
   
        self.rigFiles['rigFiles'] = refUtils.findRigs()[0]
        self.rigs['rigs'] = refUtils.findRigs()[1]
        
        self.currentRefs = {}
        
        """ Call animationModuleSettings """
        self.animMods = animModSettings.AnimMod_Info()
   
        """ Find all the files in the animation lib directory """
        """ Using this to switch art path for now """
        """ Define the artPath """
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()
        self.artPath = dirExt.artPath
        
        self.fileDirectory = (self.artPath + 'character/GEPPETTO/Animation/animLib/')
        self.currentDirectory = {}
        self.currentDirectory['newDirectory'] = self.fileDirectory
        self.anims = os.listdir(self.fileDirectory)
        
        """ Get the name of the animation file to use as a starting point for naming the output from animLib """
        self.sceneName = self.getSceneName()        
        
        """ The UI """
        """ Store the UI elements in a dictionary """
        self.UIElements = {}
        
        """ Create a dictionary to store the character name
        Run a function to get character name """
        self.characterInfo = {}
        
        UIInit = self.initializeInitVars()
        if UIInit == False:
            return
        else:
            self.animLibUI()

        
    def getSceneName(self, *args): 
        sceneName = cmds.file(q=True, sn=True, shn=True).replace(".ma", "")
        return sceneName
       
    def animLibUI(self, *args):
        """ If the window exists, delete it. """
        if cmds.window("animLibWindow", exists=True):
            cmds.deleteUI("animLibWindow")
                        
        buttonWidth_A = 100
        buttonHieght_A = 44
        columnAWidth = 100
        columnBWidth = 260
        columnCWidth = 360
        totalColumnWidth = (columnAWidth, columnBWidth, columnCWidth)

        columnOffset = 5
        
        
        windowHeight = 320 
        windowWidth = (columnAWidth + columnBWidth + columnCWidth + 15) 
      
        # Create the main window
        mainWindow = self.UIElements["window"] = cmds.window("animLibWindow", h=windowHeight, w=windowWidth, s=True, rtf=True )
        
        child1 = self.UIElements["listBoxRowLayout"] = cmds.rowLayout(nc=3, columnWidth3=totalColumnWidth, columnAttach=([1, "left", columnOffset], [2, "both", columnOffset], [3, "right", columnOffset]), rowAttach=([1, "top", columnOffset], [2, "top", columnOffset], [3, "top", columnOffset])) 
        #child1 = self.UIElements["listBoxRowLayout"] = cmds.flowLayout(v=False, w=400)
        # Create a couple flow layouts to hold the UI Elements for setup tools
        self.UIElements["buttonColumnLayout"] = cmds.flowLayout(v=True, w=columnAWidth, h=windowHeight) 
        cmds.setParent( '..' )        

        self.UIElements["listColumnLayout"] = cmds.flowLayout(v=True, w=columnBWidth, h=windowHeight) 
        cmds.setParent( '..' )
        
        self.UIElements["fcheckColumnLayout"] = cmds.flowLayout(v=True, w=columnCWidth, h=windowHeight, p=self.UIElements["listBoxRowLayout"]) 
        cmds.setParent( '..' )
        
        self.UIElements["imagePaneLayout"] = cmds.paneLayout( w=columnCWidth, h=240, p=self.UIElements["fcheckColumnLayout"]) 
        
        """ First column """
        cmds.setParent(self.UIElements["buttonColumnLayout"])
        #self.UIElements['loadDirButton'] = cmds.button( label='Load Library', width=80, c=self.chooseDirectory )
        
        cmds.separator( height=5, style='in' )
        self.UIElements['saveAnimButton'] = cmds.button( label='Save Animation', width=buttonWidth_A, h=buttonHieght_A, c=self.switchToCamerView ) 
                
        cmds.separator( height=5, style='in' )
        self.UIElements['loadAnimButton'] = cmds.button( label='Load Animation', width=buttonWidth_A, h=buttonHieght_A, c=self.importAnim ) 
        
        cmds.separator( height=5, style='in' )
        self.UIElements['batchExportButton'] = cmds.button( label='Batch Save', width=buttonWidth_A, h=buttonHieght_A, c=self.batchSaveToAnimLib )
        
        """ Second Column """
        # Create the setup UI elements
        cmds.setParent(self.UIElements["listColumnLayout"])
        #self.UIElements['checkBoxA'] = cmds.radioButtonGrp (labelArray2=['AnimLib', 'AnimDir'], numberOfRadioButtons=2 )
        self.UIElements["nameField"] = cmds.textField(tx=self.sceneName, width=columnBWidth)
        
        cmds.separator( height=7, style='in' )
        self.UIElements["animationList"] = cmds.textScrollList(numberOfRows=4, allowMultiSelection=True, append=self.anims, selectIndexedItem=1, width=columnBWidth, h=200, sc=self.displayImageSequence, dcc=self.goForeward)
              
        self.UIElements['backButton'] = cmds.button( label='<-- back', width=80, c=self.backButton ) 
 
        """ The UI will initialize with the image viewer """
        """ The image layout will switch to a custom model panel when a save animation runs """
        self.imageViewer()
        
        cmds.setParent(self.UIElements["fcheckColumnLayout"])       
        cmds.separator( height=7, style='in' )
        self.UIElements['imageSlider'] = (cmds.intSlider( min=1, max=100, value=1, step=1, w=columnCWidth ))
        
        
        cmds.showWindow(self.UIElements["window"])
        
    def switchToCamerView(self, *args):
        iplContents = cmds.paneLayout(self.UIElements["imagePaneLayout"], q=True, ca=True)
        if iplContents != None:
            cmds.deleteUI(iplContents)
        """ Make a camera """
        self.playblastCam()
        """ Create a new model panel layout """ 
        cmds.setParent(self.UIElements["imagePaneLayout"])   
        self.UIElements['modelPanel'] = cmds.modelPanel(mbv=False, label="PlayblastWindow")
        """ Show the playblastCam in the model panel """
        cmds.modelPanel(self.UIElements['modelPanel'], edit=True, cam=self.UIElements['playblastCam'][0])
        cmds.setParent(self.UIElements["window"])
        """ Edit the save animation button """
        cmds.button(self.UIElements['saveAnimButton'], edit=True, label='Continue', c=self.exportCurrentAnimation ) 
        
        
        
    def playblastCam(self, *args):
        self.UIElements['playblastCam'] = cmds.camera(n='playblastCam')
        
    def playBlastScrubber(self, *args):
        cmds.intSlider( min=-1, max=100, value=1, step=1 )
        
    def imageViewer(self, *args):
        iplContents = cmds.paneLayout(self.UIElements["imagePaneLayout"], q=True, ca=True)
        if iplContents != None:
            cmds.deleteUI(iplContents)
        cmds.setParent(self.UIElements["imagePaneLayout"]) 
        """ Create an area for displaying images """
        #image = 'Z:/tap/tools/maya/geppetto/Icons/Epic_Win.jpg'
        image = '//corp-nas01/DC/dc_art/character/GEPPETTO/Animation/animLib/chr_superman/chr_superman_trans_run_to_idle_short/chr_superman_trans_run_to_idle_short.iff'
        self.UIElements['image'] = cmds.image( image=image )
 
        cmds.setParent(self.UIElements["window"])
        
    def displayImageSequence(self, *args):
        selection = cmds.textScrollList(self.UIElements["animationList"], q=True, si=True)

        imageDir = (self.currentDirectory['newDirectory'] + selection[0] + '/' )
        imageFile = (imageDir + selection[0] + '.iff')
        
        contents = os.listdir(imageDir)
        if contents == None:
            return

        iplContents = cmds.paneLayout(self.UIElements["imagePaneLayout"], q=True, ca=True)
        if iplContents != None:
            print iplContents
            cmds.deleteUI(iplContents)
        cmds.setParent(self.UIElements["imagePaneLayout"]) 
        """ Create an area for displaying images """
        image = '//corp-nas01/DC/dc_art/character/GEPPETTO/Animation/animLib/chr_superman/chr_superman_trans_run_to_idle_short/Epic_Win.jpg'
        self.UIElements['image'] = cmds.image( image=image )
 

      

    def initializeInitVars(self, *args):
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
        for name in namespaces:
            var = 'Character'
            result = name.startswith(var)
            if result == True:
                self.characterInfo['characterNamespace'] = self.findCharacterNames()[0]
                self.characterInfo['characterName'] = self.findCharacterNames()[1]
                self.getCurrentReferences()
                return True
            else:
                cmds.headsUpMessage("No valid character in the scene")
                return False
    
    def getCurrentReferences(self):
        refs = cmds.file(r=True, q=True)
        self.currentRefs['refs'] = refs
            
        
    def chooseDirectory(self, *args):
        """ Define the artPath """
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()
        artPath = dirExt.artPath
        
        radioState = cmds.radioButtonGrp(self.UIElements['checkBoxA'], q=True, sl=True)

        if radioState == 1:
            directory = (artPath + 'character/GEPPETTO/Animation/animLib/')
        if radioState == 2:
            directory = (artPath + 'character/')
    
    def goForeward(self, *args):
        selection = cmds.textScrollList(self.UIElements["animationList"], q=True, si=True)
        path = (self.artPath + 'character/GEPPETTO/Animation/animLib/')
        directory = (path + selection[0] + '/')
        ext = '.ma'
        self.traverseDirectory(directory, ext)
    
    def backButton(self, *args):
        currentDirectory = self.fileDirectory
        #currentDirectory = currentDirectory.rpartition('/')[0]
        #directory = (currentDirectory + '/')
        self.traverseDirectory(currentDirectory, None)
        
    def traverseDirectory(self, directory, ext, *args):
        returnFiles = self.findFiles(directory, ext)

        cmds.textScrollList(self.UIElements["animationList"], e=True, ra=True)
        cmds.textScrollList(self.UIElements["animationList"], e=True, append=returnFiles)
        
        
        

    def findFiles(self, directory, ext, *args):
        allFiles = os.listdir(directory)
    
        # Refine all files, listing only those of the specified file extension
        returnFiles = []
        if ext != None:
            for f in allFiles:
                splitString = str(f).rpartition(ext)
            
                if not splitString[1] == "" and splitString[2] == "":
                    returnFiles.append(splitString[0])
        else:
            for f in allFiles:
                returnFiles.append(f)
        
        self.currentDirectory['newDirectory'] = directory
        
        return returnFiles
    
    def loadImageSequence(self):
        print ''
        
    def saveImageSequence(self):
        """ Query the current camera so we can come back here """
        try:
            cam = cmds.modelPanel(cmds.getPanel(wf=True), q=True, cam=True)
        except:
            cam = 'persp'

        """ Create a camera and set to active view """
        cameraName = cmds.camera()
        cameraShape = cameraName[1]
        
    def exportCurrentAnimation(self, *args):
        animName = cmds.textField(self.UIElements["nameField"], tx=True, q=True)
        self.exportAnim(animName)
        
        """ Switch back to image viewer"""
        self.imageViewer()
        
    def batchSaveToAnimLib(self, *args):
        """ Define the artPath """
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()
        artPath = dirExt.artPath
        
        extension = "*.ma"
        
        files = cmds.fileDialog2(fileFilter=extension, cap='Select Animations', dialogStyle=2, fm=4, okc='OK', dir=artPath)
        try:
            for file in files:
                cmds.file(file, open=True)
                animName = self.getSceneName()
                self.exportAnim(animName)
        except: print "Browser window closed or export failed. """

    def exportAnim(self, animName, *args):
        #animName = cmds.textField(self.UIElements["nameField"], tx=True, q=True)

        """ animationModuleSettings export settings File """

        self.animMods.write_rig_settings(animName)
        
        characterName = self.characterInfo['characterName']
        characterName = self.shortenCharacterName()
        
        finalPath = (self.animDir + characterName + '/' + animName)
    
        animCurves = self.getAnimCurves()[0]
        
        """ Insert code to verify the curve is valid (connected) """

        cmds.select(d=True)
        for curve in animCurves: 
            if cmds.objExists(curve) == True:   
                cmds.select(curve, add=True)
        
        cmds.file(finalPath, es=True, type='mayaAscii')
        cmds.select(d=True)

        #self.animLib.animPostExport(animCurves, characterNamespace)
      
    def importAnim(self, *args): 
        """ Define the artPath """
        import System.directoryExtension as directoryExtension
        dirExt = directoryExtension.DirectoryExtension()
        artPath = dirExt.artPath
        
        
        animName = cmds.textScrollList(self.UIElements["animationList"], q=True, si=True)
        print animName
        animLen = len(animName)
        print animLen
        characterShortName = self.shortenCharacterName()
        print characterShortName
        if animLen == 1:
            print "FUICKU"
            self.importAnimProc(animName)
        if animLen > 1:
            print "poop"
            directory = cmds.fileDialog2(cap='Choose Directory', dialogStyle=2, fm=3, okc='OK', dir=artPath)
            for anim in animName:
                self.refCharacterInNewFile()
                
                
                #self.importAnimProc(anim)


            
    def refCharacterInNewFile(self, *args):
        import System.sceneSettings as settings
        reload(settings)
        
        cmds.file(new=True, pmt=False, force=True)
        
        refUtils = referenceUtils.Reference_Utils() 
        refUtils.referenceFile(self.currentRefs['refs'][0], self.characterInfo['characterNamespace'], self.currentRefs['refs'][1]) 
        charName = self.shortenCharacterName()
         
        refUtils.setupConstraints(self.characterInfo['characterNamespace'], charName)
        
        
            
            
    def importAnimProc(self, animName, *args):
        currentDirectory = self.currentDirectory['newDirectory'] 
        print currentDirectory
        print animName
        
        animMaName = (animName[0] + ".ma")
    
        finalPath = (self.currentDirectory['newDirectory'] + animMaName)
       
        animFile = cmds.file(finalPath, i=True, dns=True)
        print animFile
       
        """ Connect the animation curves to the controls """
        self.animConnectCurves()
       
        """ Load the settings """
        loadSettings = self.animMods.load_rig_settings(currentDirectory, animName[0])
       
        if loadSettings == None:
            cmds.headsUpMessage(animName[0]+ " has been loaded")
            print (animName[0]+ " has been loaded")
        else:
            print "---------Missing animation modules----------"
            for setting in loadSettings:
                print setting
            cmds.headsUpMessage(animName[0]+ " has been loaded with --ERROR. /n Open the script editor for details")
      

    def animConnectCurves(self, *args):
        missingControls = []
        
        animCurves = self.getAnimCurves()[0]
        
        for curve in animCurves:

            tmpControlName = curve.rpartition("_")[0]            
            tmpAttrName = curve.rpartition("_")[2]
            
            tmpControlName = tmpControlName.partition(':')[2]
            
            controlName = (self.characterInfo['characterNamespace'] + ':' + tmpControlName)

            attrName = (controlName + "." + tmpAttrName)

            suffix = "_currentSpace"  
            result = curve.endswith(suffix)  
            if result == False:
                if cmds.objExists(controlName): 
                    try:
                        cmds.connectAttr(curve + '.output', attrName, force=True)     
                    except: 
                        missingControls.append(controlName)
                        
        return missingControls 
    

    def getAnimCurves(self, *args):     
        animCurves = []
        tmpAnimCurves = []
        
        allAnimCurves = cmds.ls(type='animCurve')
        for curve in allAnimCurves:
            animCurves.append(curve)

        return (animCurves, tmpAnimCurves)  


    def findCharacterNames(self, *args):
        characterNamespace = utils.findInstalledCharacters()
        if len(characterNamespace) != 0:
            characterNamespace = characterNamespace[0]
    
            characterName = (characterNamespace)
        else:
            cmds.headsUpMessage("No valid character in the scene")
            return

        return (characterNamespace, characterName)   
    
    def shortenCharacterName(self):

        characterNamespace = self.animMods.characterInfo['characterName']
        
        """ Get the character name.   Need a better util for this """
        tmpCharName = characterNamespace.partition("__")[2]
        characterShortName = tmpCharName.rpartition("_")[0]
        return (characterShortName)

 #----------------------------------------------------------------------------------- 
 #
 # Script: geppetto_UI.py
 # Author: Ryan Griffin
 # Date: 12/20/2010
 # Description: V.1  # This will serve as a wrapper UI for all the various UI windows used in the geppetto MPR tool.
 # Use: initiate the Geppetto_UI class
 #
 #-----------------------------------------------------------------------------------

import os
import sys
import maya.cmds as cmds



class Geppetto_UI:
    def __init__(self):
        # store UI elements in a dictionary
        self.UIElements = {}
        
        if cmds.window("geppetto_UI_window", exists=True):
            cmds.deleteUI("geppetto_UI_window")
        
        buttonSize = 66 
        buttonSize2 = 86    
        windowWidth = 66
        windowHeight = 520
        
        self.UIElements["geppettoWindow"]= cmds.window("geppetto_UI_window", width=windowWidth, height=windowHeight, title="Geppetto UI", sizeable=True, rtf=True, mnb=False, mxb=False, tlb=True)
        
        # Create UI elements
        self.UIElements ["flowLayout"] = cmds.flowLayout(v=True, columnSpacing=5, w=windowWidth, h=windowHeight)
        
        
        cmds.setParent(self.UIElements["flowLayout"])
        
        icon7 = os.environ["GEPPETTO"] + "/Icons/geppetto.bmp"
        self.UIElements["geppetto_But"] = cmds.symbolButton(width=buttonSize, height=buttonSize2, image=icon7, annotation='View the Geppetto Documentation', command=self.geppetto_doc_Button)
        
        
        icon = os.environ["GEPPETTO"] + "/Icons/blueprintUI.bmp"
        self.UIElements["bpUI_But"] = cmds.symbolButton(width=buttonSize, height=buttonSize, image=icon, annotation='Open the Blueprint UI.', command=self.Blueprint_UI_Button)
        
               
        icon3 = os.environ["GEPPETTO"] + "/Icons/characterInstall.bmp"
        self.UIElements["charInst_But"] = cmds.symbolButton(width=buttonSize, height=buttonSize, image=icon3,  annotation='Install a Character', command=self.characterInstall_Button)

        icon4 = os.environ["GEPPETTO"] + "/Icons/modMaintenance.bmp"
        self.UIElements["modMaint_But"] = cmds.symbolButton(width=buttonSize, height=buttonSize, image=icon4, annotation='Put the Character in Maintenance mode to add Animation Modules', command=self.moduleMaintenanace_Button)
     
       
        icon6 = os.environ["GEPPETTO"] + "/Icons/setup_button.bmp"
        self.UIElements["setup_But"] = cmds.symbolButton(width=buttonSize, height=buttonSize, image=icon6, annotation='Load and Save Setup Files', command=self.setup_Button)
        
     
        cmds.separator( height=5, style='in' )
        cmds.text(label='  Animation', fn="boldLabelFont")
        
        icon5 = os.environ["GEPPETTO"] + "/Icons/animationUI.bmp"
        self.UIElements["animUI_But"] = cmds.symbolButton(width=buttonSize, height=buttonSize, image=icon5, annotation='Tools for Animators', command=self.animation_UI_Button)
        
        #icon8 = os.environ["GEPPETTO"] + "/Icons/animLib_button.bmp"
        #self.UIElements["animLib_But"] = cmds.symbolButton(width=buttonSize, height=buttonSize, image=icon8, annotation='Animation Library', command=self.animation_Lib_Button)
        
  
        # Display Window
        cmds.showWindow(self.UIElements["geppettoWindow"])
        

    # These are all the shelf buttons needed for Gepetto v.001

    def Blueprint_UI_Button(self, *args):        
        try:
            riggingToolRoot = os.environ["GEPPETTO"]
        except:
            print "GEPPETTO environment variable not correctly configured"
        else: 
            print riggingToolRoot
            path = riggingToolRoot + "/Modules"
        
            if not path in sys.path:
                sys.path.append(path)
        
            import System.blueprint_UI as blueprint_UI
        
            
            UI = blueprint_UI.Blueprint_UI()
    
    
    def characterInstall_Button(self, *args):
        try:
            riggingToolRoot = os.environ["GEPPETTO"]
        except:
            print "GEPPETTO environment variable not correctly configured"
        else: 
            print riggingToolRoot
            path = riggingToolRoot + "/Modules"
        
            if not path in sys.path:
                sys.path.append(path)
        
            import System.characterInstall as characterInstall
        
            inst = characterInstall.InstallCharacter_UI()

    def moduleMaintenanace_Button(self, *args):      
        try:
            riggingToolRoot = os.environ["GEPPETTO"]
        except:
            print "GEPPETTO environment variable not correctly configured"
        else: 
            print riggingToolRoot
            path = riggingToolRoot + "/Modules"
        
            if not path in sys.path:
                sys.path.append(path)
        
            import System.moduleMaintenance_shelfTool as moduleMaintenance_shelfTool
            #reload if changes are made to "moduleMaintenance" or moduleMaintenance_shelf
            #reload (moduleMaintenance_shelfTool)
        
            inst = moduleMaintenance_shelfTool.ModuleMaintenance_shelfTool()
            
    def animation_UI_Button(self, *args):
        try:
            riggingToolRoot = os.environ["GEPPETTO"]
        except:
            print "GEPPETTO environment variable not correctly configured"
        else: 
            print riggingToolRoot
            path = riggingToolRoot + "/Modules"
        
            if not path in sys.path:
                sys.path.append(path)
        
            import System.animation_UI as animation_UI
        
            UI = animation_UI.Animation_UI()
            
    def skinning_Button(self, *args):
        try:
            riggingToolRoot = os.environ["GEPPETTO"]
        except:
            print "GEPPETTO environment variable not correctly configured"
        else: 
            print riggingToolRoot
            path = riggingToolRoot + "/Modules"
        
            if not path in sys.path:
                sys.path.append(path)
        
            import System.skinning as skin
        
            dudes = skin.skinning_Tools()
            dudes.attachGeo_UI()
            
    def setup_Button(self, *args):
        
        import System.altSetupTools as animMods
        reload(animMods)

        animModInfo = animMods.Setup_Tools()

        readModInfo = animModInfo.setup_UI()
            
    def animation_Lib_Button(self, *args):
        try:
            riggingToolRoot = os.environ["GEPPETTO"]
        except:
            print "GEPPETTO environment variable not correctly configured"
        else: 
            print riggingToolRoot
            path = riggingToolRoot + "/Modules"
            
            if not path in sys.path:
                sys.path.append(path)
            
            import System.animationLib_UI_v2 as animLib_UI
    
            UI = animLib_UI.AnimLib_UI()

        
    def characterTracker_Button(self, *args):
        import System.characterTracker as characterTracker
        CharacterTracker = characterTracker.CharacterTracker()    
        
            
    def geppetto_doc_Button(self, *args):
       import webbrowser
       url = "http://creativestudio.turbine.wiki/index.php/Geppetto"
       webbrowser.open_new_tab(url)


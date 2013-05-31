import maya.cmds as cmds
from functools import partial
import System.utils as utils
reload (utils)

# 129
# Used to attach geometry
class AttachGeoToBlueprint_ShelfTool:
    def attachWithParenting(self):
        self.parenting = True
        self.skinning = False
        self.processInitialSelection()
        
    def attachWithSkinning(self):
        self.skinning = True
        self.parenting = False
        self.processInitialSelection()
        
    def processInitialSelection(self):
        print self.skinning
        print self.parenting
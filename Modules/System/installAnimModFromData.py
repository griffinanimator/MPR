
import maya.cmds as cmds

import os

import System.animationModSettings as animModSettings

class Stuff:
    def __init__(self, *args):
        import System.moduleMaintenance as moduleMaintenance
        modMaintenance = moduleMaintenance.ModuleMaintenance(self)

        modMaintenance.setAttrsFromModInfo()
        
        
        

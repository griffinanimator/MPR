import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.directoryExtension as directoryExtension


import __main__

class Namespace_Utils:
    def __init__(self):
        self.gjData = gjData.gameJoint_Data()
        
        
    def queryNamespaces(self):
        cmds.namespace(set=':')
        info = cmds.namespaceInfo(lon=True)
        print info
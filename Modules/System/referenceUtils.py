import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.directoryExtension as directoryExtension

import System.gameJointData as gjData

import __main__

class Reference_Utils:
    def __init__(self):
        self.gjData = gjData.gameJoint_Data()

    def queryRefences(self):
        print "qr"
        
    def setNS_default(self):
        print "snd"
        
    def referenceFile(self, file, characterNamespace, setupFile, *args):
        cmds.namespace(set=':')

        cmds.file(file, r=True, ns=characterNamespace)
        cmds.file(setupFile, r=True, dns=True)
        
    
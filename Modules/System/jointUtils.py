import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils

import System.turbineSpecificUtils as turbineUtils


class gameJoint_Utils():    
    def __init__(self):
        """ Initialize class and variables """

    def isEndJoint(self):
        """ Get the game joints into a list """
        cmds.select("*_gjnt")
        gameJoints = cmds.ls(sl=True, type="joint")
        
        """ Is the joint an end joint? """
        endJoints = []
    
        for joint in gameJoints:
            connections = cmds.listConnections(joint, s=False, type="joint")
            if connections == None:
                endJoints.append(joint)
     
        return endJoints
    
    def getPhysicsJoint(self):
        cmds.select(d=True)
        try:
            cmds.select("physics*_*_gjnt")
            physicsJoint = cmds.ls(sl=True, type="joint")
            cmds.select(d=True)
            return physicsJoint
        except:
            print "physics does not exist"
   
    def getParentJoint(self):
        cmds.select(d=True)
        try:
            cmds.select("parent*_*_gjnt")
            parentJoint = cmds.ls(sl=True, type="joint")
            cmds.select(d=True)
            return parentJoint
        except:
            print "parent does not exist"
        

    """ Returns all the game joints in the scene """
    def getGameJoints(self):
        cmds.select(d=True)
        parentJoint = self.getParentJoint()
        ignoreBones = self.getIgnoreBones()
        
        cmds.select("*_gjnt")

        cmds.select(ignoreBones, d=True)
         
        cmds.select(parentJoint, d=True)
        
        """ Throwing this in as a temp fix"""
        optDslJoints = ("parent1_mi1_gjnt", "clavicle2_ri1_gjnt", "clavicle2_li1_gjnt" )
        for joint in optDslJoints:
            try:
                cmds.select(joint, d=True)
            except:
                pass
        
        gameJoints = cmds.ls(sl=True, type="joint")        
        cmds.select(d=True)
        
        return gameJoints
    
    def getIgnoreBones(self):
        endJoints = self.isEndJoint()
        physJoint = self.getPhysicsJoint()
        parentJoint = self.getParentJoint()
        
        cmds.select(d=True)
        cmds.select(endJoints)
        if physJoint != None:
            cmds.select(physJoint, add=True)
        if parentJoint != None:
            cmds.select(parentJoint, add=True)
            
        ignoreBones = cmds.ls(sl=True, type="joint")
            
        cmds.select(d=True)

        return ignoreBones
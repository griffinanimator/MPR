import maya.cmds as cmds
import pymel.core as pm

animCurves = []

allKeys = []

allAnimCurves = cmds.ls(type='animCurve')
for curve in allAnimCurves:
    if curve.startswith ("Character"):
        animCurves.append(curve)

for aCurve in animCurves:
    print aCurve
    inTangentType = cmds.keyTangent(aCurve, q=True, inTangentType=True)
    print inTangentType
    outTangentType = cmds.keyTangent(aCurve, q=True, outTangentType=True)
    print outTangentType
    
    numKeys = cmds.keyTangent(aCurve, q=True, time=(":",))
    print numKeys
    
    cmds.select("Character__npc_robot_minion_1:character_container")
    cmds.lockNode(l=False, lu=False)
    
cmds.select("Character__npc_robot_minion_1:LegFoot__lt_leg:LegIK_ReverseFoot_1:footControl")
control = cmds.ls(sl=True)    
    
time = cmds.findKeyFrame(control, time=(25,25), which="next" )
print time
 
    

Character__npc_robot_minion_1:LegFoot_lt_leg:LegIK_ReverseFoot_1:footControl







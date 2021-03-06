import maya.cmds as cmds
import os

import System.utils as utils
import System.blueprint as blueprintMod
#reload(blueprintMod)

CLASS_NAME = "PhysicsJointChain"

TITLE = "Physics Joint Chain"
DESCRIPTION = "Creates 2 physics joint chain.  Suggested use: Physics"
ICON = os.environ["GEPPETTO"] + "/Icons/physics_button.bmp"

class PhysicsJointChain(blueprintMod.Blueprint):
    def __init__(self, userSpecifiedName, hookObject):
        jointInfo = [["physics_1_joint", [0.0, 0.0, 0.0]], ["physics_2_joint", [0.0, 0.0, -4.0]]]
        
        gameJntNames = ["physics_", "physics1_"]
               
        # Call on the blueprints initialization
        blueprintMod.Blueprint.__init__(self, CLASS_NAME, userSpecifiedName, jointInfo, hookObject, gameJntNames, altCtrl=3)
        #self.canBeMirrored
    def install_custom(self, joints):
        self.createOrientationControl(joints[0], joints[1])

    def lock_phase1(self):
        jointPositions = []
        jointOrientationValues = []
        jointRotationOrders =[]
        #v036
        joints = self.getJoints()
        
        for joint in joints:
            jointPositions.append(cmds.xform(joint, q=True, worldSpace=True, translation=True))
        #v036 
        cleanParent = self.moduleNamespace+":joints_grp"    
        orientationInfo = self.orientationControlledJoint_getOrientation(joints[0], cleanParent)
        cmds.delete(orientationInfo[1])
        jointOrientationValues.append(orientationInfo[0])
        jointOrientations = (jointOrientationValues, None)

        jointRotationOrders.append(cmds.getAttr(joints[0]+".rotateOrder"))
        
        jointPreferredAngles = None
        hookObject = self.findHookObjectForLock()
        rootTransform = True
                
        moduleNamespace = self.moduleNamespace
            
        moduleInfo = (jointPositions, jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, rootTransform, moduleNamespace, True)
        #moduleInfo = (jointPositions , jointOrientations, jointRotationOrders, jointPreferredAngles, hookObject, True)
        #moduleInfo[5]=True
        return moduleInfo
    
        #v046
    #Custom UI 
    def UI_custom(self):
        joints = self.getJoints()
        self.createRotationOrderUIControl(joints[0])
    # 081    
    def mirror_custom(self, originalModule):
        jointName = self.jointInfo[0][0]
        originalJoint = originalModule+":"+jointName
        newJoint = self.moduleNamespace+":"+jointName
        
        originalOrientationControl = self.getOrientationControl(originalJoint)
        newOrientationControl = self.getOrientationControl(newJoint)
        
        cmds.setAttr(newOrientationControl+".rotateX", cmds.getAttr(originalOrientationControl+".rotateX"))
        
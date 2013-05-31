import maya.cmds as cmds
import os
import sys
import __main__

def findAllModules(relativeDirectory):
    # search the relative directory  for all available modules
    # Return a list of all module names (excluding the ".py" extension)
    fileDirectory = os.environ["GEPPETTO"] + "/" + relativeDirectory + "/"
    allPyFiles = findAllFiles(relativeDirectory, fileDirectory, ".py")
    
    returnModules = []
    
    for file in allPyFiles:
        if file != "__init__":
            returnModules.append(file)
            
    return returnModules
    
# Remove any name spaces that are not module related 
# Looks at the module root and returns module names
# v034 
def findAllModuleNames(relativeDirectory):
    validModules = findAllModules(relativeDirectory)
    validModuleNames = []
    
    packageFolder = relativeDirectory.partition("/Modules/")[2]
    
    for m in validModules:
        mod = __import__(packageFolder+"."+m, {}, {}, [m])
        reload(mod)  
        
        validModuleNames.append(mod.CLASS_NAME)
 
    return(validModules, validModuleNames)

def findAllTemplateFiles(relativeDirectory):
    import System.directoryExtension as directoryExtension
    dirExt = directoryExtension.DirectoryExtension()
    artPath = dirExt.artPath
    
    fileDirectory = artPath + relativeDirectory + "/"

    return findAllFiles(relativeDirectory, fileDirectory, ".ma")

def findAllMayaFiles(relativeDirectory):
    fileDirectory = os.environ["GEPPETTO"] + "/" + relativeDirectory + "/"
    return findAllFiles(relativeDirectory, fileDirectory, ".ma")


def findAllAnimFiles(animationDirectory):
        animFiles = os.listdir(animationDirectory)
        # Refine all files, listing only those of the specified file extension
        returnFiles = []
        for f in animFiles:
            splitString = str(f).rpartition('.ma')
            
            if not splitString[1] == "" and splitString[2] == "":
                returnFiles.append(f)
        print returnFiles
        return returnFiles
    
def findAllFiles(relativeDirectory, fileDirectory, fileExtension):
    
    # Search the relative directory for all files with the given extension.
    # Return a list of all file names, excluding the file extension
    
    """  I made a change to this.  This function was looking in the tool root.  Now it is the art tree."""    
    #fileDirectory = os.environ["GEPPETTO"] + "/" + relativeDirectory + "/"
    allFiles = os.listdir(fileDirectory)
    
    # Refine all files, listing only those of the specified file extension
    returnFiles = []
    for f in allFiles:
        splitString = str(f).rpartition(fileExtension)
        
        if not splitString[1] == "" and splitString[2] == "":
            returnFiles.append(splitString[0])

    return returnFiles

#v013
def findHighestTrailingNumber(names, basename):
    import re
       
    highestValue = 0
    
    for n in names:
        if n.find(basename) == 0:
            suffix = n.partition(basename)[2]
            if re.match("^[0-9]*$", suffix):
                numericalElement = int(suffix)
                
                if numericalElement > highestValue:
                    highestValue = numericalElement
             
    return highestValue

# v016
def stripLeadingNamespace(nodeName):
    if str(nodeName).find(":") == -1:
        return None
    
    splitString = str(nodeName).partition(":") 
    
    return [splitString[0], splitString[2]]

def stripAllNamespaces(nodeName):
    if str(nodeName).find(":") == -1:
        return None
    
    splitString = str(nodeName).rpartition(":")
    return [splitString[0], splitString[2]]


def basic_stretchy_IK(rootJoint, endJoint, container=None, lockMinimumLength=True, poleVectorObject=None, scaleCorrectionAttribute=None):
    from math import fabs
    
    containedNodes = []
 
    # v024
    totalOriginalLength = 0.0
    
    done = False
    parent = rootJoint
    
    childJoints = []
    
    while not done:
        children = cmds.listRelatives(parent, children=True)
        children = cmds.ls(children, type="joint")
        
        if len(children) == 0:
            done = True
        else:
            child = children[0]
            childJoints.append(child)
            """  This is where we adjust to make this work with meters """
            totalOriginalLength  += fabs(cmds.getAttr(child+".translateX"))
            
            parent = child
            
            if child == endJoint:
                done =  True
            
   
    # create RP IK on joint chain
    ikNodes = cmds.ikHandle(sj=rootJoint, ee=endJoint, sol="ikRPsolver", n=rootJoint+"_ikHandle")
    ikNodes[1] = cmds.rename(ikNodes[1], rootJoint+"_ikEffector")
    ikEffector = ikNodes[1]
    ikHandle = ikNodes[0]
    
    cmds.setAttr (ikHandle+".visibility", 0)
    containedNodes.extend(ikNodes)
    
    # Create pole vector locator
    if poleVectorObject == None:
        poleVectorObject = cmds.spaceLocator(n=ikHandle+"_poleVectorLocator")[0]
        containedNodes.append(poleVectorObject)
        
        cmds.xform(poleVectorObject, ws=True, absolute=True, translation=cmds.xform(rootJoint, q=True, ws=True, translation=True))
        cmds.xform(poleVectorObject, ws=True, relative=True, translation=[0.0, 1.0, 0.0])
        
        cmds.setAttr(poleVectorObject+".visibility", 0)
        
    poleVectorConstraint = cmds. poleVectorConstraint(poleVectorObject, ikHandle)[0]
    containedNodes.append(poleVectorConstraint)    
    
    # Create root and end locators
    rootLocator = cmds.spaceLocator(n=rootJoint+"_rootPosLocator")[0]
    rootLocator_pointConstraint = cmds.pointConstraint(rootJoint, rootLocator, maintainOffset=False, n=rootLocator+"_pointConstraint")
    
    endLocator = cmds.spaceLocator(n=endJoint+"_endPosLocator")[0]
    cmds.xform(endLocator, worldSpace=True, absolute=True, translation=cmds.xform(ikHandle, q=True, worldSpace=True, translation=True))
    ikHandle_pointConstraint = cmds.pointConstraint(endLocator, ikHandle, maintainOffset=False, n=ikHandle+"_pointConstraint")[0]
    
    containedNodes.extend([rootLocator, endLocator, rootLocator_pointConstraint, ikHandle_pointConstraint])
    
    cmds.setAttr(rootLocator+".visibility", 0)
    cmds.setAttr(endLocator+".visibility", 0)
    
    #v024
    # Grab distance between locators
    rootLocatorWithoutNamespace = stripAllNamespaces(rootLocator)[1]
    endLocatorWithoutNamespace = stripAllNamespaces(endLocator)[1]
    
    moduleNamespace = stripAllNamespaces(rootJoint)[0]
   
    distNode = cmds.shadingNode("distanceBetween", asUtility=True, n=moduleNamespace+":distBetween_"+rootLocatorWithoutNamespace+"_"+endLocatorWithoutNamespace)
    
    containedNodes.append(distNode)
    
    cmds.connectAttr(rootLocator+"Shape.worldPosition[0]", distNode+".point1")
    cmds.connectAttr(endLocator+"Shape.worldPosition[0]", distNode+".point2")   
    
    scaleAttr = distNode+".distance"
    
    #167
    if scaleCorrectionAttribute != None:
        scaleCorrection = cmds.shadingNode("multiplyDivide", asUtility=True, n=ikHandle+"_scaleCorrection")
        containedNodes.append(scaleCorrection)
        
        cmds.setAttr(scaleCorrection+".operation", 2) # divide
        cmds.connectAttr(distNode+".distance", scaleCorrection+".input1X")
        cmds.connectAttr(scaleCorrectionAttribute, scaleCorrection+".input2X")
        
        scaleAttr = scaleCorrection+".outputX"

    
    # Divide distance by total original length = scale factor
    scaleFactor = cmds.shadingNode("multiplyDivide", asUtility=True, n=ikHandle+"_scaleFactor")
    containedNodes.append(scaleFactor)
    
    cmds.setAttr(scaleFactor+".operation", 2) #Divide
    cmds.connectAttr(scaleAttr, scaleFactor+".input1X")
    cmds.setAttr(scaleFactor+".input2X", totalOriginalLength)
    
    translationDriver = scaleFactor + ".outputX"
    

    if lockMinimumLength:
        conditionNode = cmds.shadingNode("condition", asUtility=True, n=ikHandle+"_scaleCondition")
        containedNodes.append(conditionNode)
        
        cmds.connectAttr(scaleAttr, conditionNode+".firstTerm")
        cmds.setAttr(conditionNode+".secondTerm", totalOriginalLength)
        
        cmds.setAttr(conditionNode+".operation", 2) # (>)
        
        cmds.connectAttr(scaleFactor+".outputX", conditionNode+".colorIfTrueR")
        cmds.setAttr(conditionNode+".colorIfFalseR", 1)
        
        translationDriver = conditionNode +".outColorR"
        
    lockBlend = cmds.shadingNode("blendColors", asUtility=True, n=ikHandle+"_lockBlend")
    containedNodes.append(lockBlend)
    
    cmds.connectAttr(translationDriver, lockBlend+".color1R")
    cmds.setAttr(lockBlend+".color2R", 1)
    
    stretchinessAttribute = lockBlend + ".blender"
    cmds.setAttr(stretchinessAttribute, 1)
    
     #<167   
    
    # Connect joints to stretch calculations
    for joint in childJoints:
        multNode = cmds.shadingNode("multiplyDivide", asUtility=True, n=joint+"_scaleMultiply")
        containedNodes.append(multNode)
        
        cmds.setAttr(multNode+".input1X", cmds.getAttr(joint+".translateX"))
        cmds.connectAttr(translationDriver, multNode+".input2X")
        cmds.connectAttr(multNode+".outputX", joint+".translateX")
 
    if container != None:
        # Edit v023
        addNodeToContainer(container, containedNodes, ihb=True)

    returnDict = {}
    returnDict["ikHandle"] = ikHandle
    returnDict["ikEffector"] = ikEffector
    returnDict["rootLocator"] = rootLocator
    returnDict["endLocator"] = endLocator
    returnDict["poleVectorObject"]= poleVectorObject
    returnDict["ikHandle_pointConstraint"] = ikHandle_pointConstraint
    returnDict["rootLocator_pointConstraint"] = rootLocator_pointConstraint
    returnDict["stretchinessAttribute"] = stretchinessAttribute
    
    return returnDict


# Force scene update
def forceSceneUpdate():
    cmds.setToolTo( "moveSuperContext" )
    nodes = cmds.ls()
    
    for node in nodes:
            cmds.select(node, replace=True)
            
    cmds.select(clear=True)
    
    cmds.setToolTo( "selectSuperContext" )
    
# v023    
def addNodeToContainer(container, nodesIn, ihb=False, includeShapes=False, force=False):
    import types

    nodes = []
    
    if type(nodesIn) is types.ListType:
        nodes = list(nodesIn)
    else:
        nodes = [nodesIn]
    
    conversionNodes = []    
    for node in nodes:
        node_conversionNodes = cmds.listConnections(node, source=True, destination=True)
        node_conversionNodes = cmds.ls(node_conversionNodes, type="unitConversion")
        
        conversionNodes.extend(node_conversionNodes)
        
    nodes.extend(conversionNodes)
    # Hacked this.  Was getting Unicode error
    for node in nodes:
        cmds.container(container, edit=True, addNode=node, ihb=ihb, includeShapes=includeShapes, force=force)
        
        
#048
# Find out if user specified name exists
def doesBlueprintUserSpecifiedNameExist(name):
    cmds.namespace(setNamespace=":")
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
    
    names = []
    for namespace in namespaces:
        if namespace.find("__") !=-1:
            names.append(namespace.partition("__")[2])
           
    return name in names 

# 106

def RP_2segment_stretchy_IK(rootJoint, hingeJoint, endJoint, container=None, scaleCorrectionAttribute=None):
    moduleNamespaceInfo = stripAllNamespaces(rootJoint)
    moduleNamespace = ""
    if moduleNamespaceInfo != None:
        moduleNamespace = moduleNamespaceInfo[0]
        
    rootLocation = cmds.xform(rootJoint, q=True, ws=True, t=True)
    elbowLocation = cmds.xform(hingeJoint, q=True, ws=True, t=True)
    endLocation = cmds.xform(endJoint, q=True, ws=True, t=True)
    
    ikNodes = cmds.ikHandle(sj=rootJoint, ee=endJoint, n=rootJoint+"_ikHandle", solver="ikRPsolver")
    ikNodes[1] = cmds.rename(ikNodes[1], rootJoint+"_ikEffector")
    ikEffector = ikNodes[1]
    ikHandle = ikNodes[0]
    
    cmds.setAttr(ikHandle + ".visibility", 0)
    
    rootLoc = cmds.spaceLocator(n=rootJoint+"_positionLocator")[0]
    cmds.xform(rootLoc, worldSpace=True, absolute=True, translation=rootLocation)
    cmds.parent(rootJoint, rootLoc, a=True)
    
    endLoc = cmds.spaceLocator(n=ikHandle+"_positionLocator")[0]
    cmds.xform(endLoc, worldSpace=True, absolute=True, translation=endLocation)
    cmds.parent(ikHandle, endLoc, a=True)
    
    elbowLoc = cmds.spaceLocator(n=hingeJoint+"_positionLocator")[0]
    cmds.xform(elbowLoc, worldSpace=True, absolute=True, translation=elbowLocation)
    elbowLocatorConstraint = cmds.poleVectorConstraint(elbowLoc, ikHandle)[0]
    
    #  Make it stretchy
    # make empty list for appending utility nodes
    utilityNodes = []
    for locators in ((rootLoc, elbowLoc, hingeJoint), (elbowLoc, endLoc, endJoint)):
        from math import fabs
        
        startLocNamespaceInfo = stripAllNamespaces(locators[0])
        startLocWithoutNamespace = ""
        if startLocNamespaceInfo != None:
            startLocWithoutNamespace = startLocNamespaceInfo[1]

        endLocNamespaceInfo = stripAllNamespaces(locators[0])
        endLocWithoutNamespace = ""
        if endLocNamespaceInfo != None:
            endLocWithoutNamespace = endLocNamespaceInfo[1]
        
        startLocShape = locators[0]+"Shape"
        endLocShape = locators[1]+"Shape"
        
        distNode = cmds.shadingNode("distanceBetween", asUtility=True, name=moduleNamespace+":distBetween_"+startLocWithoutNamespace+"_"+endLocWithoutNamespace)
        
        cmds.connectAttr(startLocShape+".worldPosition[0]", distNode+".point1")
        cmds.connectAttr(endLocShape+".worldPosition[0]", distNode+".point2")
        
        utilityNodes.append(distNode)
        
        scaleFactor = cmds.shadingNode("multiplyDivide", asUtility=True, n=distNode+"_scaleFactor")
        utilityNodes.append(scaleFactor)
        
        cmds.setAttr(scaleFactor+".operation", 2)  # divide
        originalLength = cmds.getAttr(locators[2]+".translateX")
        
        cmds.connectAttr(distNode+".distance", scaleFactor+".input1X")
        cmds.setAttr(scaleFactor+".input2X", originalLength)
        
        translationDriver = scaleFactor+".outputX"
        
        translateX = cmds.shadingNode("multiplyDivide", asUtility=True, n=distNode+"_translationValue")
        utilityNodes.append(translateX)
        cmds.setAttr(translateX+".input1X", fabs(originalLength))
        cmds.connectAttr(translationDriver, translateX+".input2X")
        
        cmds.connectAttr(translateX+".outputX", locators[2]+".translateX")
        
    if container != None:
        containedNodes = list(utilityNodes)
        containedNodes.extend(ikNodes)
        containedNodes.extend( [rootLoc, elbowLoc, endLoc])
        containedNodes.append(elbowLocatorConstraint)
                    
        addNodeToContainer(container, containedNodes, ihb=True)
        
    return (rootLoc, elbowLoc, endLoc, utilityNodes)


# 111
def findJointChain(rootJoint):
    joints = [rootJoint]
    parent = rootJoint
    done = False
    while not done:
        children = cmds.listRelatives(parent, children=True)
        children = cmds.ls(children, type="joint")
        
        if len(children) == 0:
            done = True
        else: 
            child = children[0]
            joints.append(child)
            parent = child
            
    return joints

# 141
def findInstalledCharacters():
    cmds.namespace(setNamespace=":")
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True)
    
    characterNamespaces = []
    
    for n in namespaces:
        print n
        if n.find("Character__") == 0:
            characterNamespaces.append(n) 
    return characterNamespaces

#144
def findInstalledBlueprintInstances(characterNamespaces):
    cmds.namespace(setNamespace = characterNamespaces)
    moduleInstances = cmds.namespaceInfo(listOnlyNamespaces=True)
    returnModuleInstances = []
    
    for module in moduleInstances:
        returnModuleInstances.append(stripLeadingNamespace(module)[1])
        
    cmds.namespace(setNamespace = ":")
    
    return returnModuleInstances

#151
def findFirstFreeConnection(attribute):
    found = False
    index = 0
    
    while not found:
        if cmds.connectionInfo(attribute+"["+str(index)+"]", isDestination=True):
            index += 1
        else:
            found=True
            
    return index


# 171
def matchTwistAngle(twistAttribute, ikJoints, targetJoints):
    forceSceneUpdate()
    
    currentVector = []
    targetVector = []
    
    # Get the current and target vector
    # Is this a single or multiple joint segment?
    if len(ikJoints) <= 2:
        currentVector = calculateTwistVectorForSingleJointChain(ikJoints[0])
        targetVector = calculateTwistVectorForSingleJointChain(targetJoints[0])
    else:
        currentVector = calculateTwistVector(ikJoints[0], ikJoints[1], ikJoints[len(ikJoints)-1])
        targetVector = calculateTwistVector(targetJoints[0], targetJoints[1], targetJoints[len(targetJoints)-1])
        
    targetVector = normaliseVector(targetVector)
    currentVector = normaliseVector(currentVector)
    
    offsetAngle = calculateAngleBetweenNormalisedVectors(targetVector, currentVector)
    
    cmds.setAttr(twistAttribute, cmds.getAttr(twistAttribute)+offsetAngle)
    
    if len(ikJoints) <= 2:
        currentVector = calculateTwistVectorForSingleJointChain(ikJoints[0])
    else:
        currentVector = calculateTwistVector(ikJoints[0], ikJoints[1], ikJoints[len(ikJoints)-1])
        
    currentVector = normaliseVector(currentVector)
    
    newAngle = calculateAngleBetweenNormalisedVectors(targetVector, currentVector)
    if newAngle > 0.1:
        offsetAngle *= -2
        cmds.setAttr(twistAttribute, cmds.getAttr(twistAttribute)+offsetAngle)
        
    
        
def calculateTwistVectorForSingleJointChain(startJoint):
    tempLocator = cmds.spaceLocator()[0]
    
    cmds.setAttr(tempLocator+".visibility", 0)
    
    cmds.parent(tempLocator, startJoint, relative=True)
    cmds.setAttr(tempLocator+".translateZ", 5.0)
    
    jointPos = cmds.xform(startJoint, q=True, ws=True, translation=True)
    locatorPos = cmds.xform(tempLocator, q=True, ws=True, translation=True)
    
    twistVector = [ locatorPos[0]-jointPos[0], locatorPos[1]-jointPos[1], locatorPos[2]-jointPos[2]]
    
    cmds.delete(tempLocator)
    
    return twistVector

def calculateTwistVector(startJoint, secondJoint, endJoint):
    a = cmds.xform(startJoint, q=True, ws=True, t=True)
    endPos = cmds.xform(endJoint, q=True, ws=True, t=True)
    
    b = [endPos[0] - a[0], endPos[1] - a[1], endPos[2] -a[2]]
    b = normaliseVector(b)
    
    p = cmds.xform(secondJoint, q=True, ws=True, t=True)
    
    p_minus_a = [p[0]-a[0], p[1]-a[1], p[2]-a[2]]
    p_minus_a__dot__b = p_minus_a[0]*b[0] + p_minus_a[1]*b[1] + p_minus_a[2]*b[2]
    
    p_minus_a__dot__b__multiply_b = [p_minus_a__dot__b * b[0], p_minus_a__dot__b * b[1], p_minus_a__dot__b * b[2]]
    
    q = [a[0] + p_minus_a__dot__b__multiply_b[0], a[1] + p_minus_a__dot__b__multiply_b[1], a[2] + p_minus_a__dot__b__multiply_b[2]]
    
    twistVector = [p[0] - q[0], p[1] - q[1], p[2] - q[2]]
    
    return twistVector
    
    
def normaliseVector(vector):
    from math import sqrt
    returnVector = list(vector)
    
    vectorLength = sqrt( returnVector[0]*returnVector[0] + returnVector[1]*returnVector[1] + returnVector[2]*returnVector[2])
    
    if vectorLength != 0:
        returnVector[0] /= vectorLength
        returnVector[1] /= vectorLength
        returnVector[2] /= vectorLength
    else:
        returnVector[0] = 1.0
        returnVector[1] = 0.0
        returnVector[2] = 0.0
        
    return returnVector

def calculateAngleBetweenNormalisedVectors(VectA, VectB):
    from math import acos, degrees
    
    dotProduct = VectA[0]*VectB[0] + VectA[1]*VectB[1] + VectA[2]*VectB[2]\
    
    if dotProduct <= -1.0:
        dotProduct = -1.0
    elif dotProduct >= 1.0:
        dotProduct = 1.0
        
    radians = acos(dotProduct)
    return degrees(radians)

def sceneSetup(self):
    cmds.currentUnit(linear="m")
    cmds.setAttr("perspShape.nearClipPlane", 0.001)
    cmds.setAttr("perspShape.farClipPlane", 10000)
    cmds.grid(size=10, spacing=5.0, d=5)
    
def exportJointInfo(xmlFileName):
    import xml.dom.minidom
    import xml.dom
    
    translatexValue=[]
    translateyValue=[]
    translatezValue=[]
    parentValue=[]
    jointName=[]
    bpValue=[]
    rotValue=[]
    orientValX=[]
    orientValY=[]
    orientValZ=[]
    
    
    # Select Joints
    cmds.select( '*game*joint' )
    jointName = (cmds.ls(sl=True))
    jointName.reverse()
    
    #Print the number of joints############################
    arrayLength = len(jointName)
    
    for joint in jointName:
        cmds.select (joint)  
        # Get parent value
        parent = cmds.getAttr(joint + ".parentJoint")
        parentValue.append(parent)
        # Get bpJoint value
        bpJoint = cmds.getAttr(joint + ".bpJoint")
        bpValue.append(bpJoint)
        # Get world positions      
        tv = cmds.xform ( q=True, ws=True, t=True)
        translatexValue.append (tv[0])        
        translateyValue.append (tv[1])        
        translatezValue.append (tv[2])
        # Get rotation order
        rotOrder = cmds.getAttr(joint + ".rotateOrder")
        rotValue.append(rotOrder)
        # Get joint orientations
        jointOrientX = cmds.getAttr(joint + ".jointOrientX")
        orientValX.append(jointOrientX)
        jointOrientY = cmds.getAttr(joint + ".jointOrientY")
        orientValY.append(jointOrientY)
        jointOrientZ = cmds.getAttr(joint + ".jointOrientZ")
        orientValZ.append(jointOrientZ)       
       
        
    #This is the section that writes the xml-------
    #### Create root elements of XML doc
    doc = xml.dom.minidom.Document()
    rootelement = doc.createElement("Pose")
    doc.appendChild(rootelement)
    rootelement.setAttribute("name", "buildPose")
    elements = doc.createElement("elements")
    rootelement.appendChild(elements)
    
       
    for x in range  (len (jointName)):
        # Format the .xml
        joint = doc.createElement("joint")
        elements.appendChild(joint)

        joint.setAttribute("name", jointName[x])
        
        parentElement = doc.createElement("parentJoint")        
        joint.appendChild(parentElement)
        
        bpElement = doc.createElement("bpJoint")        
        joint.appendChild(bpElement)
        
        transElement = doc.createElement("translation")
        joint.appendChild(transElement)
        
        rotElement = doc.createElement("rotOrder")
        joint.appendChild(rotElement)
        
        orientElement = doc.createElement("orientation")
        joint.appendChild(orientElement)
        
        # Fill the elements with data
        # Parent
        parentJnt = doc.createElement("parent")
        parentJnt.setAttribute("value", str (parentValue[x]))
        parentElement.appendChild(parentJnt)
        
        # bpJoint
        bpJnt = doc.createElement("bp")
        bpJnt.setAttribute("value", str (bpValue[x]))
        bpElement.appendChild(bpJnt)
        
        # Rotation order
        order = doc.createElement("bp")
        order.setAttribute("value", str (rotValue[x]))
        rotElement.appendChild(order)
  
        #### Create Translate elements       
        # TranslateX
        xAxis = doc.createElement("x")
        xAxis.setAttribute("value", str (translatexValue[x]))
        transElement.appendChild(xAxis)
        # TranslateY    
        yAxis = doc.createElement("y")
        yAxis.setAttribute("value", str (translateyValue[x]))
        transElement.appendChild(yAxis)
        # Translatez    
        zAxis = doc.createElement("z")
        zAxis.setAttribute("value", str (translatezValue[x]))
        transElement.appendChild(zAxis)
        
        #### Create orientation elements       
        # OrderX
        xAxis = doc.createElement("x")
        xAxis.setAttribute("value", str (orientValX[x]))
        orientElement.appendChild(xAxis)
        # OrderY    
        yAxis = doc.createElement("y")
        yAxis.setAttribute("value", str (orientValY[x]))
        orientElement.appendChild(yAxis)
        # OrderZ    
        zAxis = doc.createElement("z")
        zAxis.setAttribute("value", str (orientValZ[x]))
        orientElement.appendChild(zAxis)
        
        
        xmlString = doc.toprettyxml("    ")
 
        # File to save to
        myfile = file(xmlFileName, 'w')

        # Write File
        myfile.write(xmlString)
        
        # close the file
        myfile.close()
        
        cmds.select(cl=True)
        
        
# Read the joint info from xml, then build the joints.        
def importJointInfo(xmlFileName):
    import xml.dom.minidom
    import xml.dom
    
    cmds.select( clear=True )
    listJoints=[]
    # open the xml file for reading 
    fileObject = file(xmlFileName, 'r')
    # parse the xml file to get all of it's elements
    xmlDoc = xml.dom.minidom.parse(fileObject)
    # Get the joint elements into a list
    joints = xmlDoc.getElementsByTagName('joint')
    # iterate through all of the joint elements
    #Loads joint positions
    for joint in joints:
        # get the child elements of the joint in order to get the translation values
        children = joint.childNodes            
        # loop through the child elements
        for child in children:
            # make sure the the current node type is not a text node
            if child.nodeType != child.TEXT_NODE:
                # get the name of the joint from the name attribute attached to the joint element.
                jointName = joint.getAttribute("name")                                    
                listJoints.append(jointName)
                # create a joint named the joint name 
                if not cmds.objExists(jointName):                        
                    cmds.joint( n = jointName )                     
                    cmds.select( clear=True) 
    # close the file
    fileObject.close()
    return listJoints

# Read the joint info from xml, then position, parent and orient the joints.        
def setJointAttrs(xmlFileName):
    import xml.dom.minidom
    import xml.dom
    
    cmds.select( clear=True )
    listJoints=[]
    # open the xml file for reading 
    fileObject = file(xmlFileName, 'r')
    # parse the xml file to get all of it's elements
    xmlDoc = xml.dom.minidom.parse(fileObject)
    # Get the joint elements into a list
    joints = xmlDoc.getElementsByTagName('joint')
    # iterate through all of the joint elements
    #Loads joint positions
    for joint in joints:
        # get the child elements of the joint in order to get the translation values
        children = joint.childNodes            
        # loop through the child elements
        for child in children:
            # make sure the the current node type is not a text node
            if child.nodeType != child.TEXT_NODE:
                # get the name of the joint from the name attribute attached to the joint element.
                jointName = joint.getAttribute("name")                                    
                listJoints.append(jointName)
                
                # Deal with joint positioning. #########################################################
                # look to see if the tag name of the current child element is
                # named translation
                if child.tagName == "translation":
                    # if the node is the translation node get it's children
                    # to get the x,y,z value
                    translationAxis = child.childNodes
                    # loop through each of the axis
                    for axis in translationAxis:
                          # once again make sure that we do not have a text node element
                            if axis.nodeType != axis.TEXT_NODE:
            
                                # get the axis attribute value
                                axisValue = axis.getAttribute("value")
                                #print "%s:%s" % (axis.tagName, axisValue)
            
                                # set the attribute name by combining the joint name and the
                                # axis name
                                attribute = "%s.translate%s" % (jointName, axis.tagName.upper())
            
                                # convert the string to a float value
                                intValue = float(axisValue)
        
                                # set the attribute value
                                cmds.setAttr(attribute, intValue)
                                cmds.select( clear=True )    
                                
    

    for joint in joints:
        children = joint.childNodes            
        # loop through the child elements
        for child in children:
            if child.nodeType != child.TEXT_NODE:
                jointName = joint.getAttribute("name")                                    
                listJoints.append(jointName)
                                
                # Deal with rotate order. #########################################################  
                if child.tagName == "rotOrder":
                    # if the node is the parentJoint node get it's children
                    # to get the parent value
                    rotAxis = child.childNodes
                    # loop through each of the axis
                    for axis in rotAxis:
                        # once again make sure that we do not have a text node element
                        if axis.nodeType != axis.TEXT_NODE:
                            # get the axis attribute value
                            axisValue = axis.getAttribute("value")
                            # set the attribute name by combining the joint name and the
                            # axis name
                            attribute = jointName + ".rotateOrder"
                            # convert the string to a float value
                            intValue = float(axisValue)
                            # set the attribute value
                            cmds.setAttr(attribute, intValue)
                            cmds.select( clear=True )
                            
                # Deal with orientation. #########################################################  
                if child.tagName == "orientation":
                    # if the node is the translation node get it's children
                    # to get the x,y,z value
                    orientAxis = child.childNodes
                    # loop through each of the axis
                    for axis in orientAxis:
                          # once again make sure that we do not have a text node element
                            if axis.nodeType != axis.TEXT_NODE:
            
                                # get the axis attribute value
                                axisValue = axis.getAttribute("value")
            
                                # set the attribute name by combining the joint name and the
                                # axis name
                                attribute = "%s.jointOrient%s" % (jointName, axis.tagName.upper())
            
                                # convert the string to a float value
                                intValue = float(axisValue)
        
                                # set the attribute value
                                cmds.setAttr(attribute, intValue)
                                cmds.select( clear=True )
                                
    for joint in joints:
        children = joint.childNodes            
        # loop through the child elements
        for child in children:
            if child.nodeType != child.TEXT_NODE:
                jointName = joint.getAttribute("name")                                    
                listJoints.append(jointName) 
                            
                # Deal with joint parent. #########################################################
                if child.tagName == "parentJoint":
                    # if the node is the parentJoint node get it's children
                    # to get the parent value
                    parentAxis = child.childNodes
                    for axis in parentAxis:
                        if axis.nodeType != axis.TEXT_NODE:
                            parentValue = axis.getAttribute("value")
                            if parentValue == "World":
                                pass
                            else:
                                try:
                                    cmds.parent(jointName, parentValue, a=True )
                                except: pass
                                 
                                
                                
# Read the joint info from xml, then parent game joints to blueprint joints.        
def parentToBlueprint(xmlFileName, characterNameString):
    import xml.dom.minidom
    import xml.dom
    
    cmds.select( clear=True )
    
    listJoints=[]
    gameParentConstraints=[]
    gameScaleConstraints=[]
    
    # open the xml file for reading 
    fileObject = file(xmlFileName, 'r')
    # parse the xml file to get all of it's elements
    xmlDoc = xml.dom.minidom.parse(fileObject)
    # Get the joint elements into a list
    joints = xmlDoc.getElementsByTagName('joint')
    # iterate through all of the joint elements
    
    for joint in joints:
        children = joint.childNodes            
        # loop through the child elements
        for child in children:
            if child.nodeType != child.TEXT_NODE:
                jointName = joint.getAttribute("name")                                    
                listJoints.append(jointName) 
                            
                # Parent to blueprint joints. #########################################################
                if child.tagName == "bpJoint":
                    # if the node is the parentJoint node get it's children
                    # to get the parent value
                    parentAxis = child.childNodes
                    for axis in parentAxis:
                        if axis.nodeType != axis.TEXT_NODE:
                            parentValue = axis.getAttribute("value")
                            parentValue = (characterNameString + parentValue)
                            if parentValue == "World":
                                gameScaleCon = cmds.scaleConstraint(parentValue, jointName, sk=None) 
                                gameScaleConstraints.append(gameScaleCon)
                            else:
                                gameParentCon = cmds.parentConstraint(parentValue, jointName, mo=True )
                                gameParentConstraints.append(gameParentCon) 
                                gameScaleCon = cmds.scaleConstraint(parentValue, jointName, sk="none")
                                gameScaleConstraints.append(gameScaleCon)
                         
    return (gameParentConstraints, gameScaleConstraints)                         
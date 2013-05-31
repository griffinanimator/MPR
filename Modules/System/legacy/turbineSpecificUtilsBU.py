import os
import maya.cmds as cmds
import pymel.core as pm
import System.utils as utils
import tsapi.core.environment as environment
reload(environment) 

def jointRename(self): 
    # Find the setup group
    setupGrp = "Setup_grp"
    # Find and unlock the setup container
    setupContainer = cmds.container(q=True, fc=setupGrp)
    cmds.lockNode(setupContainer, l=False, lu=False)
    
    # find all the game joint by querying the contents of the container.
    setupNodes = cmds.container(setupContainer, q=True, nl=True) 

    # If the joint is the last in a chain, we need to make sure we add "cap" to the name.
    for nodes in setupNodes:
        isEndJoint = cmds.listConnections(nodes, s=False, d=True, t="joint")   
        if isEndJoint == None:
            newName = nodes.replace("_game", "_game_cap")
            if cmds.objExists(newName):
                pass
            else:
                cmds.rename(nodes, newName)

    cmds.lockNode(setupContainer, l=True, lu=True)


# This function will return all the character specific paths and names
#  If needed, will also setup the directories.    
def setupDirs(characterName, create=False):  

    environment = environment.environment()  
        
    """ Using this to switch art path for now """

    artPath = environment.paths['art_path']
 
    characterDir = artPath + "character\\" + characterName
    setupDir = characterDir + "\\setup\\"

    xmlDir = characterDir + "\\xml\\"
    # For Lotro
    #rigDir = artPath + "Product_Art\\Characters\\GEPPETTO\\" 
    #for DC
    rigDir = artPath + "character\\GEPPETTO\\" 
    skinDir = characterDir + "\\skin\\"
    
    # Specific paths to specific character files

    characterFileName = rigDir + characterName + ".ma" 
    setupFileName = setupDir + characterName + "_setup" + ".ma"
    xmlFileName = xmlDir + characterName + "_xml" + ".xml"
    
        
    # I am going to create a directory setup for this character if one does not exist. 
    if create:
        directories = (characterDir, setupDir, xmlDir, rigDir, skinDir)
        for dir in directories:
            try:
                os.makedirs(dir)            
            except OSError:
                pass
            
    # Should we try to create the directory if it does not exist?
    # The user may have deleted it.
          
    return (characterDir, setupDir, xmlDir, rigDir, skinDir, characterFileName, setupFileName, xmlFileName)

def getCharacterNamespace(characterName):

    baseNamespace = "Character__" + characterName + "_"
    extraNamespace = "Export__" + characterName + "_"
        
    cmds.namespace(setNamespace=":")
    namespaces=cmds.namespaceInfo(listOnlyNamespaces=True)
        
    highestSuffix = utils.findHighestTrailingNumber(namespaces, baseNamespace)
    highestSuffix += 1
        
    characterNamespace = baseNamespace + str(highestSuffix)

    exportNamespace = extraNamespace + str(highestSuffix)
    
    return (characterNamespace, exportNamespace)


def getCharacterInfo():
    cmds.namespace(set=":")
    namespaces = cmds.namespaceInfo(lon=True)
    characterName = []
    for name in namespaces:        
        characterContainer = (name + ":character_container")
        setupContainer = name.replace("Character__", "Export__")
        setupContainer = (setupContainer + ":Setup")
        if cmds.objExists (characterContainer):
            fullCharName = name
            tmpCharName = name.split("__")[1]
            tmpCharName = tmpCharName[:tmpCharName.rfind("_")]
            characterName = tmpCharName 
            return (characterName, characterContainer, fullCharName, setupContainer)  
                  
        else:
            # Warn no character in the scene
            charConfirm = ("No character exists in this scene")
            cmds.confirmDialog(messageAlign="center", title="Create Directory", message= charConfirm)
            
        
# I need to replace the function from utils that saves/loads files from a relative directory.  This is only used to find the rig file.
# relative director refers to a path variable the user passes when calling the function.
def findAllRigFiles(relativeDirectory):
    return findAllFiles(relativeDirectory, ".ma")

"""  I need to be able to use this on a directory passed in as a string"""
def findAllFiles(relativeDirectory, fileExtension):
    # get the path to source art
    import System.environment as environment
    reload (environment)

    environment = environment.environment()  
        
    """ Using this to switch art path for now """

    artPath = environment.paths['art_path']
    print "here"
    print artPath
    #artPath = "Z:\\\\art\\"
    
    rigDir = artPath + "character\\" 
        
    # Search the relative directory for all files with the given extension.
    # Return a list of all file names, excluding the file extension
    print " Eat Shit ###########################################################"
    fileDirectory = rigDir + "/" + relativeDirectory + "/"

    allFiles = os.listdir(fileDirectory)
    
    # Refine all files, listing only those of the specified file extension
    returnFiles = []
    for f in allFiles:
        splitString = str(f).rpartition(fileExtension)
        
        if not splitString[1] == "" and splitString[2] == "":
            returnFiles.append(splitString[0])

    return returnFiles




def boneMarking():
    import tsapi.core.maya.joint as joint
    reload (joint)
    
    # Use the joint class to identify the joints in the scene
    joint = joint.joint()
    ignoreBones = joint.GetGameJointInfo()[2]
    bindJoints = joint.GetGameJointInfo()[0]
    
    for joint in ignoreBones:
        cmds.select (joint)
        try:
            cmds.setAttr (joint + '.boneType', "ignore", type="string" )
        except:
            cmds.addAttr (ln="boneType", nn= 'BoneType', dt='string', k=False)
            cmds.setAttr (joint + '.boneType', "ignore", type="string" )
            
    for joint in bindJoints:
        cmds.select (joint)
        splitString = joint.partition("_game_")
        tmpName = splitString[0]

        markName = (tmpName + "_boneMarking")
                
        try:
            cmds.setAttr (joint + '.boneType', markName, type="string" )
        except:
            cmds.addAttr (ln="boneType", nn= 'BoneType', dt='string', k=False)
            cmds.setAttr (joint + '.boneType', markName, type="string" )
            

            
def loadHoldLocs():
    import xml.dom.minidom
    import xml.dom
    import tsapi.core.maya.joint as joint
    reload (joint)

    # The name of the holding location
    allLocs=[]
    
    # Use the joint class to identify the joints in the scene
    joint = joint.joint()
    bindJoints = joint.GetGameJointInfo()[0]
    
    if bindJoints == None:
        cmds.headsUpMessage( 'No game joints exist in this scene.  Holding locations will not be added.')
        return
    else:
        # We should create a holding loc for each game joint.    
        cmds.select( clear=True )
        #listJoints=[]
        # open the xml file for reading 
        fileObject = file("Z://geppetto/holdLocList.xml", 'r')
        # parse the xml file to get all of it's elements
        xmlDoc = xml.dom.minidom.parse(fileObject)
        # Get the joint elements into a list
        joints = xmlDoc.getElementsByTagName('joint')
        # iterate through all of the joint elements
        #Loads joint positions
        for joint in joints:
            # get the child elements of the joint in order to get the loc name
            children = joint.childNodes            
            # loop through the child elements
            for child in children:
                # make sure the the current node type is not a text node
                if child.nodeType != child.TEXT_NODE:
                
                # Deal with holding loc name. #########################################################
                    if child.tagName == "locName":
                        # if the node is locName node get it's children
                        # to get the locName
                        locAxis = child.childNodes
                        for axis in locAxis:
                            if axis.nodeType != axis.TEXT_NODE:
                                locValue = axis.getAttribute("value")

                                
            # get the name of the joint from the name attribute attached to the joint element.
            jointName = joint.getAttribute("name")                                 

            if cmds.objExists(jointName):
                jointPos = cmds.xform(jointName, q=True, ws=True, t=True)
                # Final name for the holding location 
                                                        
                locName = ("HoldingLocation_" + jointName + "_" + locValue)
        
                allLocs.append(locName)

                locGrp = pm.group(em=True, w=True, n=locName)

                """ Once the group is created, I get a |  at the begining of the name. WTF??? """
                locGrp = cmds.ls(sl=True)
                locGrp = (locGrp)[0]

                # Move locGrp to joints position
                cmds.xform(locGrp, t=jointPos)
                # Add an "LocationType" attr to the holding loc
                cmds.addAttr(ln="LocationType", dt="string", k=False)
                cmds.setAttr(locGrp+".LocationType", locValue, type="string")
                # parent the holdLoc to the joint
                cmds.parent(locGrp, jointName)
                  
        # close the file
        fileObject.close()
        
        return allLocs

           
            
def blueprintToGameName(self, capJoint, joint, capVar=True):
    self.capJoint = capJoint
    self.joint = joint
    self.capVar = capVar
    if self.capVar == True:
        nameVar1=self.capJoint
        nameVar2="_cap_game_joint"
    if self.capVar == False:
        nameVar1=self.joint
        nameVar2="_game_joint"
        
    # Create a name to use for the game joint                                                                    
    midName = nameVar1.replace("_joint", "")                                         
    tmpName = midName.split("blueprint")
                                                                                    
    tmpPrefix = utils.stripLeadingNamespace(tmpName[0])
    tmpName1 =  (tmpPrefix[0] + tmpName[1])
    tmpName2 = tmpName1.split("__")
    gameJointName = (tmpName2[1] + nameVar2)
    
    return gameJointName

def createGameJointAttrs(gameJoint, parentObject, joint):
    
    # Create attributes on the game joint to define 
    #(parent, corresponding BP joint name, position, rotate order and orientation)
    cmds.select(gameJoint)
    cmds.addAttr(longName="parentJoint", k=True, dt="string")
    cmds.setAttr(gameJoint +".parentJoint", parentObject,  type="string")
                        
    # Make bp joint attr
    cmds.addAttr(longName="bpJoint", k=True, dt="string")
    cmds.setAttr(gameJoint +".bpJoint", joint,  type="string")
    # Joint position
    jointPos = cmds.xform(joint, q=True, ws=True, t=True)
    cmds.xform(gameJoint, ws=True, t=jointPos)
    # Rotate order
    jointRotOrder = cmds.getAttr(joint + ".rotateOrder")
    cmds.setAttr(gameJoint + ".rotateOrder", jointRotOrder)
    # Orient
    jointOrientX = cmds.getAttr(joint + ".jointOrientX")
    jointOrientY = cmds.getAttr(joint + ".jointOrientY")
    jointOrientZ = cmds.getAttr(joint + ".jointOrientZ")
    cmds.setAttr(gameJoint + ".jointOrientX", jointOrientX)
    cmds.setAttr(gameJoint + ".jointOrientY", jointOrientY)
    cmds.setAttr(gameJoint + ".jointOrientZ", jointOrientZ)
    
    
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

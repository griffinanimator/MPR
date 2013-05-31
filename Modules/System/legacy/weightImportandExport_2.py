import maya.cmds as cmds
import maya.mel as mel
import xml.dom.minidom
import xml.dom

def printSomething(*args):
    """ print text from a textfield """    
    currentText = cmds.textField(textf, q = True, tx = True)
    print currentText
        
""" create a simple window with a column layout and a button that prints something"""
# try to delete the window if it exists
try:
    cmds.deleteUI( 'simpleWindow' )
except: pass


#make window
mainWindow = cmds.window('simpleWindow', title="Skin weight importer/exporter", widthHeight=(600, 100) )    
cmds.rowColumnLayout( numberOfColumns=2, columnWidth= [(1, 500), (2, 80)] )
#export path and feild
exportPath = cmds.textField()
cmds.textField(exportPath, edit=True)

cmds.button (label ="Export Weights", height = 26, width = 80, command = 'exportWeights()' )
#import path and feild
importPath = cmds.textField()
cmds.textField(importPath, edit=True)

cmds.button (label ="Import Weights", height = 26, width = 80, command = 'importWeights()' )

cmds.showWindow(mainWindow)



#weight exporter
def exportWeights():
	#grab item put into list
	selection= cmds.ls(sl=True,fl=True)
	mel.eval("$selectionList = `ls -sl`")
	skCl = mel.eval('findRelatedSkinCluster $selectionList[0]')
	print skCl


	#turn list into string
	newStr= " ".join(["%s" % item for item in selection])

	#select verts in selected object using string etc..
	cmds.select(newStr + '.vtx[*:*]',r=True)
	verts = cmds.ls(sl=True, fl=True)
	#print verts

	doc = xml.dom.minidom.Document()
	rootelement = doc.createElement("GeoName")
	doc.appendChild(rootelement)

	#get info for each feild, x=value, y=joints, z=positions
	for eachVert in verts:
		cmds.select(eachVert)
		value = cmds.skinPercent(skCl,query=True, value=True)
		joints = cmds.skinCluster(query=True,inf=True)
		pos = cmds.xform(eachVert,query=True,t=True)
	
		vertName= doc.createElement("vertName")
		rootelement.appendChild(vertName)
		vertName.setAttribute("name", eachVert)

		for eachJoint in joints:
			JointName= doc.createElement("joint")
			vertName.appendChild(JointName)
			JointName.setAttribute("name", eachJoint)	

		for eachValue in value:	
			eachValue = str(eachValue)
			value= doc.createElement("value")
			JointName.appendChild(value)
			value.setAttribute("value", eachValue)

		for eachPOS in pos:
			eachPOS = str(eachPOS)
			vertPos= doc.createElement("vertPos")
			vertName.appendChild(vertPos)
			vertPos.setAttribute("position", eachPOS)

	#save out xml using toprettyxml

	xmlString = doc.toprettyxml(indent="  ")
	
	#filename from inital selection & path from textfeild
	filename = str(selection)
	savePath =  cmds.textField(exportPath,query=True, tx=True)
	savedocname = (filename+".xml")

	myfile = file(savePath + savedocname, 'w')

	myfile.write(xmlString)


#weight importer
def importWeights ():
	#get the filename via selection
	selection= cmds.ls(sl=True,fl=True)

	filename = str(selection)
	 
	docname = (filename+".xml")
	
	pathname = cmds.textField(importPath,query=True,tx=True)	



	docname = (pathname+ docname)
	#parse xml file
	xmlDoc = xml.dom.minidom.parse(docname)

	#get selected object's skinCluster (for skinPercent later)
	selection= cmds.ls(sl=True,fl=True)
	mel.eval("$selectionList = `ls -sl`")
	skCL = mel.eval('findRelatedSkinCluster $selectionList[0]')
	print skCL

	def weightapply(i,m):
		cmds.skinPercent(skCL, transformValue = [joints [i+m+q],skinWeights [i+m+q]])



	# get the amount of joints in a scene
	mel.eval("select -r `ls -type joint`")
	scene_jnts = cmds.ls(sl=True)
	jnt_amount = len(scene_jnts)



	#make empty varibles
	skinWeights = []
	joints = []
	vert_names = []
	
	#reading through xml doc
	#first get the vert names then select the vert (for skinPercent)
	name = xmlDoc.getElementsByTagName('vertName')
	for names in name:
		vert = names.getAttribute("name")
		cmds.select(vert, r=True)
		children = names.childNodes
		#append vert to varible
		vert_names.append(vert)
	#grab child of vert name (joints, then grab the child of the joints (weights)
		for child in children:
			if child.nodeType != child.TEXT_NODE:
				jnts = child.getAttribute("name")
				values = child.childNodes
				if jnts != '':
					#append joints to varible
					joints.append(jnts)
				for value in values:
					if value.nodeType != value.TEXT_NODE:
						#append weights to varible
						weights = value.getAttribute("value")
						weight = float(weights)
						skinWeights.append(weight)


	#create iteration amount and varibles					
	y = len(vert_names)
	q = []
	q = 0
	#create offset for the for in range based on the amount of joints in the scene
	offset = (jnt_amount - 1)
	
	for i in range(y):
		print vert_names[i]
		#select verts
		cmds.select(vert_names[i])
		for m in range (jnt_amount):
			weightapply(i,m)
				
		q = (q+offset)
	print "DONE!"
""" characterTracker.py """
""" Author: Ryan Griffin  07-25-2011 """
""" Tools for accessing the CharacterTracker.csv located in the GEPPETTO folder of each character tree. """

import csv

import maya.cmds as cmds

class CharacterTracker():
    def __init__(self):
        """ Dictionary containing a key for each character.  Each key has data pairs of value label and value """
        self.trackerInfo = {}
        self.characterNames = {}
        self.csvToArrays()
        
        """ Declare the character tracker file """
        self.file = '//corp-nas01/DC/dc_art/character/GEPPETTO/CharacterTracker.csv'
        
        """ The UI """
        self.UIElements = {}
        self.UIElementsButtons = {}
        
        """ If the window exists, delete it."""
        if cmds.window("CharacterTrackerWindow", exists=True):
            cmds.deleteUI("CharacterTrackerWindow")
            
        self.windowWidth = 200
        self.windowHeight = 550        
                
        buttonWidth = (self.windowWidth -5)
        textWidth = 140
        columnOffset = 5
   
        """ Create the main window"""
        mainWindow = self.UIElements["window"] = cmds.window("CharacterTrackerWindow", widthHeight=(self.windowWidth, self.windowHeight), s=True )
        
        """ Create a flow layout to hold the UI Elements for setup tools"""
        self.UIElements["flowLayout"] = cmds.flowLayout(v=True, w=buttonWidth)      
    
        cmds.setParent(self.UIElements["flowLayout"])

        cmds.separator( height=7, style='in' )
        self.UIElements['characterName'] = cmds.textScrollList(numberOfRows=4, width=self.windowWidth -10, height=120, append=self.characterNames['characterKeys'], dcc=self.updateVersionNumber)
        
        """ Create text entries based of the keys recovered from the csv """
        keys = self.trackerInfo.keys()
        values = self.trackerInfo.values()
        for value in values:
            textKeys = []
            for entry in value:
                textKey = entry[0]
                textKeys.append(textKey)
        for key in textKeys:
            self.UIElementsButtons[key] = cmds.text(l=key)
            cmds.separator( height=5, style='in' )
        
        """ Field for entering a new bug """    
        self.UIElements['textField'] = cmds.textField(tx='Enter bugs here', w=180, h=60)
        cmds.button( label='Submit', width=buttonWidth , height=22, vis=True)
            
        cmds.showWindow(self.UIElements["window"])
     
    def csvToArrays(self, *args):
        titleRow = []
        characterInfo = []
        characterKeys = []
        
        """ Declare the character tracker file """
        file = '//corp-nas01/DC/dc_art/character/GEPPETTO/CharacterTracker.csv'
        
        """ Open the file for reading """
        reader = csv.reader(open(file, 'rb'), delimiter=',', quotechar='"')
        
        """ Get the row that holds all the labels and append to titleRow """
        for row in reader:
            print row
            if row[0] == 'Character':
                titleRow.append (row)
            else:
                """ All the other rows go to characterInfo """
                characterInfo.append(row)
        
        """ Combine the label and value into a list.  Store the list in a dictionary """
        characterNames = []
        print titleRow
        titles = titleRow[0]
        for each in characterInfo:
            characterName = each[0]
            characterNames.append(characterName)
            statusList = []

            for index in range(len(each)):
                statusList.append([titles[index], each[index]])
                
            self.trackerInfo[characterName] = (statusList)
             
        self.characterNames['characterKeys'] = characterNames
            
    def charInfoToUIText(self, *args):  
        character = []
        character = cmds.textScrollList(self.UIElements['characterName'] , q=True, si=True)
        
        key = character[0]
        characterInfo = self.trackerInfo[key]
        for info in characterInfo:
            keyLabel = info[0]
            value = info[1]
            finalValue = (keyLabel + '_______' + value)
        
            cmds.text(self.UIElementsButtons[keyLabel], edit=True, l=finalValue)

    
    def readCsv(self, *args):
        titleRow = []
        characterInfo = []
        characterKeys = []

        """ Open the file for reading """
        reader = csv.reader(open(file, 'rb'), delimiter=',', quotechar='"')
        
        """ Get the row that holds all the labels and append to titleRow """
        for row in reader:
            if row[0] == 'Character':
                titleRow.append (row)
            else:
                """ All the other rows go to characterInfo """
                characterInfo.append(row)
                
        print         
                
    def updateVersionNumber(self, *args):  
        """ Declare the character tracker file """
        file = '//corp-nas01/DC/dc_art/character/GEPPETTO/CharacterTracker.csv'
        
        character = []
        character = cmds.textScrollList(self.UIElements['characterName'] , q=True, si=True)
        
        key = character[0]
        characterInfo = self.trackerInfo[key]
        versionNumber = characterInfo[2][1]
        
        index = 0
        """ Open the file for reading """
        with open(file, 'rb') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                newIndex = index+1
                index = newIndex
                if row[0] == character[0]:
                    numLine = index
                    versionNumber = int(row[2])
                    newVersion = versionNumber + 1
                    
                    row[2] = newVersion
                    print row
                    
    
        
        line_to_override = {numLine:[row]}            

        """ Open the csv in maya for writing """
        writer = csv.writer(open(file, 'wb'), delimiter=',')

        data = line_to_override.get(numLine, row)
        writer.writerow(data)
        
        #writer.writerow(version)
        
        
        
        
        
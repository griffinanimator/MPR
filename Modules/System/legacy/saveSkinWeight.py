    
    def saveSkinWeights():
        ''' This next block is used to define the path where the weights will be saved.
        I plan on putting this in the __init__ once I am done testing '''
        annie = annie.animation()
        
        character = cmds.ls(sl=True)
        rootPath =  turbineUtils.getCharacterInfo()[1]
        outFileSuffix = '_skinWeight.csv'
        outFile = (character + outFileSuffix )
        finalPath = ('Z:\\art\Product_Art\\Characters\\character_01\\XML\\character_01_skinWeight.csv')
        
        
        # Select the character here, then use GetValidSkinWeights to grab vert info.
        for char in annie.GetValidSkinWeights():
            vert = char[0]
        
            jointInfo = char[1]
            for each in jointInfo:
                joint = each[0]
                weight = each[1]
                
                value = (vert, joint, weight)
                
                writer = csv.writer(open(finalPath, "a"))
                writer.writerow(value)

        # Close the file
        finalPathfinalPath.close()
        
        
    def loadSkinWeights():
        import maya.mel as mel
        annie = annie.animation()
        
        allCV = []
        reader = csv.reader(open(finalPath, 'rb'), delimiter=' ', quotechar='|')
        
        # Find the skin cluster
        selection= cmds.ls(sl=True,fl=True)
        mel.eval("$selectionList = `ls -sl`")
        skCl = mel.eval('findRelatedSkinCluster $selectionList[0]')
    
        for row in reader:
            if row not in allCV:
                allCV.append(row)
                
        for cv in allCV:
            splitString1 = cv[0].partition(",")
            vert =  splitString1[0]
            splitString2 = splitString1[2].partition(",")
            joint = splitString2[0]
            value = float(splitString2[2])
            
            cmds.skinPercent( skCl, vert, transformValue=[(joint, value)])
    def exportGameAssets(self, *args): 
        self.exportSetup()
                       
        self.removeNamespaces()
        
        self.exportRig()

        
    def exportSetup(self):
        # Remove the setup_grp and geometry group from it's container.
        cmds.lockNode(self.exportContainer, l=False, lu=False)
        
        cmds.container(self.exportContainer, edit=True, removeNode="Setup_grp", ihb=True)
        if cmds.objExists("Geometry"):
            cmds.container(self.exportContainer, edit=True, removeNode="Geometry", ihb=True)
            
        cmds.select(cl=True)
            
        
        cmds.select("Geometry")
        cmds.select("Setup_grp", tgl=True)
        
        rigPath =(self.dirExt.paths['rigPath']  + '/setup/' + self.characterName)
        cmds.file(rigPath, exportSelected=True, con=False, type="mayaAscii") 
        
        cmds.container(self.exportContainer, edit=True, addNode="Setup_grp", ihb=True)
        
        cmds.lockNode(self.exportContainer, l=True, lu=True)
        
        
        
    def exportRig(self):
        #cmds.lockNode(self.characterContainer, l=False, lu=False)
        cmds.select(cl=True)
        
        cmds.select('character_container', cc=True)
        
        rigPath =(self.dirExt.paths['rigPath'] + self.characterName)
        
        cmds.file(rigPath, exportSelected=True, con=False, type="mayaAscii")
        
        
    def createCharacterNameAttr(self, *args):

        """ Unlock character_container """
        cmds.lockNode(self.characterContainer, l=False, lu=False)
        cmds.addAttr(self.characterContainer, shortName='charName', dt='string')
        
        cmds.setAttr(self.characterPrefix + ':character_container.charName',  self.characterPrefix, type='string')
        
        """ lock character_container """
        cmds.lockNode(self.characterContainer, l=True, lu=True)
        
    def removeNamespaces(self, *args):
        cmds.namespace(set=':')
        """ Move objects out of the character namespace """
        cmds.namespace(mv=(self.characterPrefix, ':'), f=True)
        cmds.namespace(rm=self.characterPrefix)
        
        cmds.namespace(mv=(self.exportPrefix, ':'), f=True)
        cmds.namespace(rm=self.exportPrefix)
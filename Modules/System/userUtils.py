import maya.cmds as cmds
import os
import getpass
import smtplib
import pymel.core as pm





def getUser():
    """ returns the user name of the currently logged in user. """
    userName = getpass.getuser()
    stuUsers = {"cmoore":"Chad", "cuth":"Chonny", "bbateman":"Brandon", "jwoodard":"Justin", "rgriffin":"Ryan", "shuxter":"Sean", "mtrujillo":"Manny", "rtighe":"Rob", "jlindemuth":"John"}
    if userName in stuUsers:
        niceName = stuUsers[userName]
    else:
        niceName = userName
    return userName, niceName

    
def containerSettings():
    pm.setContainerAtTop(val=True, **kwargs)
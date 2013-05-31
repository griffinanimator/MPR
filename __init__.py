STATUS = 'ON'
BUTTON_LABEL = 'Geppetto'
ENV_ROOT = 'GEPPETTO'

def toolCommand(*args):
    import os, sys

    try:
        riggingToolRoot = os.environ["GEPPETTO"]
    except:
        print "GEPPETTO environment variable not correctly configured"
    else: 
        print riggingToolRoot
        path = riggingToolRoot + "/Modules"
    
        if not path in sys.path:
            sys.path.append(path)
    
        import System.geppetto_UI as geppetto_UI
        reload (geppetto_UI)
    
        
        UI = geppetto_UI.Geppetto_UI()
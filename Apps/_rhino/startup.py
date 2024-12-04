__title__ = "EnneadTab_Startup"
__doc__ = "Automatically run on every new rhino start session if bind to Rhino setting."
import os
import sys
import traceback
_app_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_lib_path = os.path.join(_app_folder, "lib" )
sys.path.append(_lib_path)

# print ("\n".join(sys.path))
from EnneadTab import ERROR_HANDLE, NOTIFICATION, ENVIRONMENT, VERSION_CONTROL, USER, EXE
from EnneadTab.RHINO import RHINO_ALIAS


import rhinoscriptsyntax as rs
import Rhino # pyright: ignore
rs.AddSearchPath(_lib_path)

sys.path.append(ENVIRONMENT.RHINO_FOLDER + "\\Ennead+.menu\\get_latest.button")
import get_latest_left # pyright: ignore


@ERROR_HANDLE.try_catch_error(is_silent=True)
def main():

    
    get_latest_left.get_latest(is_silient = True)
    RHINO_ALIAS.register_alias_set()
    add_hook()

    NOTIFICATION.messenger(main_text = "Startup Script Completed")

    
@ERROR_HANDLE.try_catch_error(is_silent=True, is_pass=True)
def add_hook(): 
    # first record current file
    action_update_timesheet(Rhino.RhinoDoc.ActiveDoc)
   
        
    # then add hook for future file in this session
    Rhino.RhinoDoc.BeginOpenDocument += event_func_timesheet
    Rhino.RhinoDoc.CloseDocument += event_func_timesheet


    Rhino.RhinoDoc.BeginSaveDocument += event_func_update_EA_dist

    
    Rhino.RhinoApp.Closing += event_func_update_r8_rui
###################################################
def action_update_timesheet(doc):
    if doc.Path:
        try:
            from EnneadTab import TIMESHEET
            TIMESHEET.update_timesheet(doc.Path)
        except:
            print ("Error updating timesheet")
            if USER.IS_DEVELOPER:
                print (traceback.format_exc())


##################################################
def event_func_timesheet(sender, e):
    action_update_timesheet(e.Document)

def event_func_update_EA_dist(sender, e):
    VERSION_CONTROL.update_EA_dist()

def event_func_update_r8_rui():
    EXE.try_open_app("Rhino8RuiUpdater", safe_open=True)


if __name__ == "__main__":
    main()
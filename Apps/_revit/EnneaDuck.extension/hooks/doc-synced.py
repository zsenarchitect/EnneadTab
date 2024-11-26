import os
import random
from pyrevit import EXEC_PARAMS
from Autodesk.Revit import DB # pyright: ignore
from pyrevit.coreutils import envvars
DOC = EXEC_PARAMS.event_args.Document


import proDUCKtion # pyright: ignore 
proDUCKtion.validify()
from EnneadTab import ERROR_HANDLE, FOLDER, SOUND, LOG, NOTIFICATION, SPEAK, MODULE_HELPER, ENVIRONMENT, EMAIL, USER, DATA_FILE, IMAGE, SPEAK
from EnneadTab.REVIT import REVIT_SYNC, REVIT_FORMS, REVIT_EVENT, REVIT_SPATIAL_ELEMENT
__title__ = "Doc Synced Hook"


REGISTERED_AUTO_PROJS = ["1643_lhh bod-a_new",
                         "1643_lhh_bod-a_existing",
                        "2151_a_ea_nyuli_cup_ext",
                        "2151_a_ea_nyuli_hospital_ext",
                        "2151_A_EAEC_NYULI_Hospital_INT",
                        "2151_a_ea_nyuli_parking east",
                        "2151_a_ea_nyuli_parking west",
                        "2151_a_ea_nyuli_site",
                        "Facade System"]

REGISTERED_AUTO_PROJS = [x.lower() for x in REGISTERED_AUTO_PROJS]

def warn_non_enclosed_area(doc):
    areas = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Areas).ToElements()
    non_closed, non_placed = REVIT_SPATIAL_ELEMENT.filter_bad_elements(areas)
    note = ""
    if len(non_closed) > 0:
        note += "There are {} non-enclosed areas in need of attention.\n".format(len(non_closed))
    if len(non_placed) > 0:
        note += "There are {} non-placed areas in need of attention.".format(len(non_placed))
    if note:
        NOTIFICATION.messenger(note)


def warn_non_enclosed_room(doc):
    rooms = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Rooms).ToElements()
    non_closed, non_placed = REVIT_SPATIAL_ELEMENT.filter_bad_elements(rooms)
    note = ""
    if len(non_closed) > 0:
        note += "There are {} non-enclosed rooms in need of attention.\n".format(len(non_closed))
    if len(non_placed) > 0:
        note += "There are {} non-placed rooms in need of attention.".format(len(non_placed))
    if note:
        NOTIFICATION.messenger(note)



def update_project_2151(doc):

    if not doc.Title.lower().startswith("2151_"):
        return
    


    folder = "Ennead Tailor.tab\\Proj. 2151.panel\\LI_NYU.pulldown"
    func_name = "update_parking_data"
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False, is_from_sync_hook = True)


    return
    
    if USER.USER_NAME not in ["sha.li", "szhang"]:
        return
    
    folder = "Ennead Tailor.tab\\Proj. 2151.panel\\LI_NYU.pulldown"
    func_name = "color_pills"
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False)
    
    
    
    folder = "Ennead Tailor.tab\\Proj. 2151.panel\\LI_NYU.pulldown"
    func_name = "all_in_one_checker"
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False)



    folder = "Ennead Tailor.tab\\Proj. 2151.panel\\LI_NYU.pulldown"
    func_name = "confirm_RGB"
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False)




def update_project_2314(doc):

    if "2314_a-455 1st ave" not in doc.Title.lower():
        return
    
    folder = "Ennead Tailor.tab\\Proj. 2314.panel\\First Ave.pulldown"
    func_name = "all_in_one_checker"
    

    
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False)
    
    return


def update_project_1643(doc):
    update_new(doc)
    update_existing(doc)


def update_new(doc):
    if "1643_lhh bod-a_new" not in doc.Title.lower():
        return


    folder = "Ennead Tailor.tab\\Proj. Lenox Hill.panel\\Lenox Hill.pulldown"
    func_name = "update_level_relative_value"
    MODULE_HELPER.run_revit_script(folder, func_name, doc)

    
    folder = "Ennead Tailor.tab\\Proj. Lenox Hill.panel\\Lenox Hill.pulldown"
    func_name = "update_keyplan"
    MODULE_HELPER.run_revit_script(folder, func_name, doc)


    

def update_existing(doc):
    if "1643_lhh bod-a_existing" not in doc.Title.lower():
        return


    folder = "Ennead Tailor.tab\\Proj. Lenox Hill.panel\\Lenox Hill.pulldown"
    func_name = "update_grid_bldgId"
    MODULE_HELPER.run_revit_script(folder, func_name, doc)

    folder = "Ennead Tailor.tab\\Proj. Lenox Hill.panel\\Lenox Hill.pulldown"
    func_name = "update_level_relative_value"
    MODULE_HELPER.run_revit_script(folder, func_name, doc)

    folder = "Ennead Tailor.tab\\Proj. Lenox Hill.panel\\Lenox Hill.pulldown"
    func_name = "update_keyplan"
    MODULE_HELPER.run_revit_script(folder, func_name, doc)

    
def update_with_generic_healthcare_tool(doc):
    if not USER.IS_DEVELOPER:
        return
    health_care_projects = ["2151_a_ea_nyuli_hospital_ext"]
    
    if doc.Title.lower() not in health_care_projects:
        return
    
    folder = "Ennead.tab\\Tools.panel"
    func_name = "generic_healthcare_tool"
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False)


    
def update_DOB_numbering(doc):
    folder = "Ennead.tab\\ACE.panel"
    func_name = "update_DOB_page"
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False)


def update_sheet_name(doc):

    try:
        doc.Title
    except Exception as e:
        if USER.USER_NAME == "szhang":
            print (str(e))
        return


    if doc.Title.lower() not in REGISTERED_AUTO_PROJS:
        return

    script = "Ennead.tab\\Tools.panel\\general_renamer.pushbutton\\general_renamer_script.py"
    func_name = "rename_views"
    sheets = DB.FilteredElementCollector(doc).OfClass(DB.ViewSheet).WhereElementIsNotElementType().ToElements()
    is_default_format = True
    show_log = False
    MODULE_HELPER.run_revit_script(script, func_name, doc, sheets, is_default_format, show_log)

    
def update_working_view_name(doc):
    try:
        doc.Title
    except:
        return

    if doc.Title.lower() not in REGISTERED_AUTO_PROJS:
        return

    script = "Ennead.tab\\Manage.panel\\working_view_cleanup.pushbutton\\manage_working_view_script.py"
    func_name = "modify_creator_in_view_name"

    fullpath = "{}\\{}".format(ENVIRONMENT.REVIT_PRIMARY_EXTENSION, script)
    import imp
    ref_module = imp.load_source("manage_working_view_script", fullpath)



    views = DB.FilteredElementCollector(doc).OfClass(DB.View).WhereElementIsNotElementType().ToElements()
    no_sheet_views = filter(ref_module.is_no_sheet, views)
    is_adding_creator = True
    MODULE_HELPER.run_revit_script(script, func_name, no_sheet_views, is_adding_creator)

    

def update_project_2306(doc):
    if "universal hydrogen" not in doc.Title.lower():
        return
    # if not USER.is_SZ():
    #     return

    folder = "Ennead Tailor.tab\\Proj. 2306.panel\\Universal Hydro.pulldown"
    func_name = "factory_internal_check"
    MODULE_HELPER.run_revit_script(folder, func_name, doc, show_log = False)
 
    
    

def update_sync_queue(doc):

    # dont need to do anything if pre-sycn chech was cancelled,
    if REVIT_EVENT.is_sync_cancelled():
        return


    log_file = FOLDER.get_shared_dump_folder_file("SYNC_QUEUE_{}.sexyDuck". format(doc.Title))
  

    if not os.path.exists(log_file):
        with open(log_file, "w"): # if not existing then create
            pass

    queue = DATA_FILE.get_list(log_file)

    
    OUT = []


    for item in queue:
        if USER.USER_NAME in item:
            #this step remove current user name from any place in wait list, either beginging or last
            continue
        OUT.append(item)
        
        

    if not DATA_FILE.set_list(OUT, log_file):
        NOTIFICATION.messenger ("Your account have no access to write in DB folder.")
        return

    if REVIT_EVENT.is_sync_queue_disabled():
        # when  gloabl sync queue disabled, dont want to see dialogue, but still want to clear name from log file
        return

    if len(OUT) == 0:
        return
    try:
        next_user = OUT[0].split("]")[-1]
        # next user found!! if this step can pass
    except Exception as e:
        return


    EMAIL.email(receiver_email_list="{}@ennead.com".format(next_user),
                            subject="Your Turn To Sync!",
                            body="Hi there, it is your turn to sync <{}>!".format(doc.Title),
                            body_image_link_list=[IMAGE.get_image_path_by_name("meme_you_sync_first.jpg")])

    REVIT_FORMS.notification(main_text = "[{}]\nshould sync next.".format(next_user), sub_text = "Expect slight network lag between SH/NY server to transfer waitlist file.", window_width = 500, window_height = 400, self_destruct = 15)




def play_success_sound():
    file = 'sound_effect_mario_1up.wav'
    SOUND.play_sound(file)

@LOG.log(__file__, __title__)
@ERROR_HANDLE.try_catch_error(is_silent=True)
def doc_synced(doc):

    play_success_sound()
    REVIT_SYNC.update_last_sync_data_file(doc)


    update_sync_queue(doc)
    

    if random.random() < 0.1:
        warn_non_enclosed_area(doc)
    if random.random() < 0.1:
        warn_non_enclosed_room(doc)

    if REVIT_EVENT.is_all_sync_closing():
        return
        
    update_DOB_numbering(doc)
    update_sheet_name(doc)
    update_working_view_name(doc)
    update_with_generic_healthcare_tool(doc)


    
    update_project_2151(doc)

    if USER.IS_DEVELOPER:
        SPEAK.speak("Document {} has finished syncing.".format(doc.Title))
        NOTIFICATION.messenger("Document {} has finished syncing.".format(doc.Title))
    return


    update_project_2314(doc)
    update_project_2306(doc)
    update_project_1643(doc)






    ENNEAD_LOG.warn_revit_session_too_long(non_interuptive = False)





    if ENNEAD_LOG.is_money_negative():
        print ("Your Current balance is {}".format(ENNEAD_LOG.get_current_money()))

    ENNEAD_LOG.update_local_warning(doc)



    
    
    envvars.set_pyrevit_env_var("IS_DOC_CHANGE_HOOK_ENABLED", True)
    



#################################################################
if __name__ == "__main__":
    doc_synced(DOC)


import os
import ENVIRONMENT
import NOTIFICATION

def try_open_app(exe_name):
    """extension optional"""
    exe_name = exe_name.replace(".exe", "")
    
    exe = ENVIRONMENT.EXE_PRODUCT_FOLDER + "\\{}.exe".format(exe_name)
    if os.path.exists(exe):
        os.startfile(exe)
        return True
    foldered_exe = ENVIRONMENT.EXE_PRODUCT_FOLDER + "\\{0}\\{0}.exe".format(exe_name)
    if os.path.exists(foldered_exe):
        os.startfile(foldered_exe)
        return True
    

        
    if os.environ["USERPROFILE"].split("\\")[-1] == "szhang":
        print ("[SZ only log]No exe found in the location.")
        print (exe)
        print (foldered_exe)
        NOTIFICATION.messenger("No exe found!!!\n{}".format(exe_name))
    return False



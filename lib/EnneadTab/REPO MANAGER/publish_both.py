import publish_revit
import publish_rhino
import sync_core_module
import time
import VERSION_CONTROL

def publish_both():
    start = time.time()
    sync_core_module.sync_core()
    publish_revit.publish_revit()
    publish_rhino.publish_rhino()
    VERSION_CONTROL.copy_to_dist_folder()

    end_time = time.time()
    print ("\n\n\nFinish in {}s".format(end_time - start))


if __name__ == "__main__":
    publish_both()
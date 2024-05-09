#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Update the life safety information data"
__title__ = "Update Life Safety Info"

# from pyrevit import forms #
from pyrevit import script #

import ENNEAD_LOG
from EnneadTab import ERROR_HANDLE
from EnneadTab.REVIT import REVIT_APPLICATION, REVIT_LIFE_SAFETY
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
# uidoc = EnneadTab.REVIT.REVIT_APPLICATION.get_uidoc()
doc = REVIT_APPLICATION.get_doc()

@ERROR_HANDLE.try_catch_error
def update_life_safety(doc):
    data_source = REVIT_LIFE_SAFETY.SpatialDataSource(
                source = "Area",
                area_scheme_name = "Life Safety",
                 para_name_load_per_area = "Rooms_$LS_Occupancy AreaPer",
                 para_name_load_manual = "Rooms_$LS_Occupancy Load_Manual",
                 para_name_target = "Rooms_$LS_Occupancy Load_Target",
                 para_name_egress_id = "Door_$LS_Exit Name",
                 para_name_door_width = "Door_$LS_Clear Width"
                 )
    REVIT_LIFE_SAFETY.update_life_safety(doc, data_source)


################## main code below #####################


if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    update_life_safety(doc)
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)







#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Pick a family or system cateogry, pick to copy instance parameter data from A to B."
__title__ = "Transfer\nParameter Data"

# from pyrevit import forms #
from pyrevit import script #

import ENNEAD_LOG
import EnneadTab
from Autodesk.Revit import DB # fastest DB
# from Autodesk.Revit import UI
doc = __revit__.ActiveUIDocument.Document

def get_element_by_condition():
    print "ASK SZ for update"
    pass


################## main code below #####################
output = script.get_output()
output.close_others()


if __name__ == "__main__":
    get_element_by_condition()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)










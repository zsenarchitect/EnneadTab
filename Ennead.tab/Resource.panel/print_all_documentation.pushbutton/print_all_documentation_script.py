#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Quickly print all the [Did you know] documentations."
__title__ = "Documentation\nHint"
__tip__ = True
# from pyrevit import forms #
from pyrevit import script #

import ENNEAD_LOG

from EnneadTab.REVIT import REVIT_APPLICATION
from EnneadTab import DOCUMENTATION, ERROR_HANDLE
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
# uidoc = REVIT_APPLICATION.get_uidoc()
doc = REVIT_APPLICATION.get_doc()
            
@ERROR_HANDLE.try_catch_error
def print_all_documentation():
    DOCUMENTATION.print_documentation_book_for_review_revit()

################## main code below #####################


if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    print_all_documentation()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)











#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "NOT IN USE"
__title__ = "46B_move elements\nsouth 4500 thru move(NOT IN USE)"

# from pyrevit import forms #
from pyrevit import script #
# from pyrevit import revit #
import EA_UTILITY
import EnneadTab
from Autodesk.Revit import DB # fastest DB
# from Autodesk.Revit import UI
doc = __revit__.ActiveUIDocument.Document


################## main code below #####################
output = script.get_output()
output.close_others()
#ideas:
uidoc = __revit__.ActiveUIDocument
selection_ids = uidoc.Selection.GetElementIds ()
#print selection_ids
t = DB.Transaction(doc, "move south 4500")
t.Start()
DB.ElementTransformUtils.MoveElements(doc, selection_ids, DB.XYZ(0,-EA_UTILITY.mm_to_internal(4500),0))
t.Commit()

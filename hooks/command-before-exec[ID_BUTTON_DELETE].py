
from pyrevit import  EXEC_PARAMS, script

import EnneadTab
from Autodesk.Revit import DB
from Autodesk.Revit import UI
args = EXEC_PARAMS.event_args
doc = args.ActiveDocument 
uidoc = UI.UIDocument(doc)
uiapp = UI.UIApplication(doc.Application)
# uiapp.PostCommand(args.CommandId)

@EnneadTab.ERROR_HANDLE.try_catch_error_silently
def main():
    should_cancel_1 = check_depedent_views()
    should_cancel_2 = check_rvt_link()

    if should_cancel_1 or should_cancel_2:
        args.Cancel = True
    else:
        args.Cancel = False

def check_rvt_link():
    selection_ids = uidoc.Selection.GetElementIds()
    selection = [doc.GetElement(x) for x in selection_ids]
   
    def is_rvt_link(x):
        if not hasattr(x, 'MoveBasePointToHostBasePoint'):
            return False
        return True
    

    links = filter(is_rvt_link, selection)
   
    
    if len(links) == 0: 
        return
    
    options = ["Oops! Do not delete selected link(s).",
               "Just DELETE selected link(s)."]
    
    note = "Are you sure you want to delete revit link?"
    for link in links:
        note +=  "\n  + <" + link.GetLinkDocument ().Title + ">"

    note += "\n\nYou might want to consider 'Unload for your machine only' if you do not want to see them."
        
    res = EnneadTab.REVIT.REVIT_FORMS.dialogue(main_text = "There are revit links in current selection.",
                                                sub_text = note,
                                                options = options)
    if res == options[0]:
        is_cancel = True
    if res == options[1]:
        is_cancel = False
    else:
        is_cancel = True

    return is_cancel


        
def check_depedent_views():
    selection_ids = uidoc.Selection.GetElementIds()
    selection = [doc.GetElement(x) for x in selection_ids]
    # for x in EnneadTab.REVIT.REVIT_SELECTION.get_selection():
    #     print (x )
    #     print (type(x))
    # selected_views = [x for x in EnneadTab.REVIT.REVIT_SELECTION.get_selection() if hasattr(x, "GetDependentViewIds")]
    # parent_views = [x for x in selected_views if len(x.GetDependentViewIds ()) != 0]
    
    def is_primary_view(x):
        if not hasattr(x, 'GetDependentViewIds'):
            return False
        try:
            return x.LookupParameter("Dependency").AsString() == "Primary"
        except:
            return False
    
    # not using CORE module method becasue it is not ideal during hook scope space.
    parent_views = filter(is_primary_view, selection)
    # print (parent_views)
    
    if len(parent_views) == 0: 
        return
    
    options = ["Oops! Do not delete selected view(s).",
               "Just DELETE selected view(s)."]
    
    note = "Those view(s) have dependent views under."
    for view in parent_views:
        note +=  "\n  + " + view.Name
        for child in view.GetDependentViewIds():
            note += "\n       - " + doc.GetElement(child).Name
    res = EnneadTab.REVIT.REVIT_FORMS.dialogue(main_text = "One or more views you are trying to delete has depedent views. Deleting parent will also delete the children.",
                                                sub_text = note,
                                                options = options)
    if res == options[0]:
        is_cancel = True
    if res == options[1]:
        is_cancel = False
    else:
        is_cancel = True

    return is_cancel
############################
output = script.get_output()
output.close_others()


if __name__ == '__main__':
    main()
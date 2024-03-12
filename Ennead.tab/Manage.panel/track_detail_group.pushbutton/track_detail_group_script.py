#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Sen Zhang has not writed documentation for this tool, but he should!"
__title__ = "Track\nDetail Group"



from pyrevit import forms 
from pyrevit import script

import ENNEAD_LOG
import EnneadTab
from Autodesk.Revit import DB

# from Autodesk.Revit import UI
# uidoc = EnneadTab.REVIT.REVIT_APPLICATION.get_uidoc()
doc = EnneadTab.REVIT.REVIT_APPLICATION.get_doc()

from EnneadTab.REVIT import REVIT_FORMS

  
@EnneadTab.ERROR_HANDLE.try_catch_error
def track_detail_group():
    opts = ["Find detail groups by view",
            "Find views by detail group"]

    res = REVIT_FORMS.dialogue(options=opts, main_text="What do you want to do?")
    if not res:
        return

    if res == opts[0]:
        find_detail_groups_by_view()
    else:
        find_views_by_detail_group()

def find_detail_groups_by_view():
    views = forms.select_views()

    if not views:
        return

    for view in views:
        print ("\n\nChecking view: [{}]".format(view.Name))
        all_detail_groups = DB.FilteredElementCollector(doc, view.Id).OfCategory(DB.BuiltInCategory.OST_IOSDetailGroups).WhereElementIsNotElementType().ToElements()
        all_detail_groups = sorted(all_detail_groups, key=lambda x: x.GroupType.LookupParameter("Type Name").AsString())
        for i,group in enumerate(all_detail_groups):
            print (" - {}/{}: {}".format(i+1, len(all_detail_groups), output.linkify(group.Id, title = group.GroupType.LookupParameter("Type Name").AsString())))
    

def find_views_by_detail_group():
    all_group_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_IOSDetailGroups).WhereElementIsElementType().ToElements()
    
    class MyOption(forms.TemplateListItem):
        @property
        def name(self):
            return "{}".format(self.item.LookupParameter("Type Name").AsString())


    res = forms.SelectFromList.show(sorted([MyOption(x) for x in all_group_types], key = lambda x: x.name),
                                    multiselect=True,
                                    button_name='Select Group')
    if not res:
        return

    for group_type in res:
        print ("\n\nChecking detail group type: [{}]".format(group_type.LookupParameter("Type Name").AsString()))
        group_instances = list(group_type.Groups)
        view_ids_used = list(set([x.OwnerViewId for x in group_instances]))
        views_used = [doc.GetElement(x) for x in view_ids_used]
        views_used.sort(key = lambda x: x.Name)
        for i, view in enumerate(views_used):
            print (" - {}/{}: {} on sheet: {}:{}".format(i+1, len(views_used), 
                                                         output.linkify(view.Id, title = view.Name),
                                                        view.LookupParameter("Sheet Number").AsString(),
                                                        view.LookupParameter("Sheet Name").AsString()))

################## main code below #####################


if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    track_detail_group()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)







#!/usr/bin/python
# -*- coding: utf-8 -*-



__doc__ = "Sen Zhang has not writed documentation for this tool, but he should!"
__title__ = "Excel2Diagram"

# from pyrevit import forms #
from weakref import ref
from pyrevit import script #

import ENNEAD_LOG
from EnneadTab import ERROR_HANDLE, EXCEL, FOLDER
from EnneadTab.REVIT import REVIT_APPLICATION, REVIT_FAMILY, REVIT_VIEW, REVIT_SELECTION
from Autodesk.Revit import DB 
# from Autodesk.Revit import UI
# uidoc = EnneadTab.REVIT.REVIT_APPLICATION.get_uidoc()
doc = REVIT_APPLICATION.get_doc()



EXCEL_FILE = "J:\\1643\\2_Master File\\B-70_Programming\\01_Program & Analysis\\EA 2024-03-21 EA Program Responsibilities.xlsx"
FAMILY_NAME = "AreaShader"
WORKING_VIEW = "Program Shading_from(szhangXNLCX)"


@ERROR_HANDLE.try_catch_error
def excel_to_diagram():
    REVIT_VIEW.set_active_view_by_name(WORKING_VIEW)
    solid_id = REVIT_SELECTION.get_solid_fill_pattern_id(doc)

    
    t = DB.Transaction(doc, __title__)
    t.Start()
    
    temp = FOLDER.copy_file_to_local_dump_folder(EXCEL_FILE, "temp.xls")
    data = EXCEL.read_data_from_excel(temp, worksheet="LHH_Public Program")

    data = data[6:] # remove header roows
    color = -1,-1,-1

    for line in data:

        
        line = line[6:] # remove bad columns from left
        
        if line[0] == line[1] == line[2] == "":
            #empty line
            continue

        
        print ("\n\n")
        print (line)

        if line[0] != "":
            ref_num = line[0]
            title = line[1]
        else:
            ref_num = line[1]
            title = line[2]
            
        #round to 2 digit
        if isinstance(ref_num, float):
            ref_num = round(float(ref_num), 3)
            ref_num = str(ref_num)


        count = line[3] if line[3] != "" else 1
        unit_area = line[4] if line[4] != "" else -1

        if unit_area > 0:
            program_area = unit_area * count
        else:
            program_area = line[5] if line[5] != "" else line[6]
            

        note = str(line[7])

        if line[14] != "":
            color = line[14].split("-")
            color = [int(x) for x in color]
        
        
        

        print ("ref num = " + ref_num)
        print ("title = " + title)
        print ("count = " + str(count))
        print ("unit area = " + str(unit_area))
        print ("program area = " + str(program_area))
        print ("note = " + note)
        print ("color = " + str(color))

        
        graphic_override = DB.OverrideGraphicSettings ()
        graphic_override.SetSurfaceForegroundPatternColor (DB.Color(*color))
        graphic_override.SetSurfaceForegroundPatternId  (solid_id)
        process_line(ref_num, title, count, unit_area, program_area, note, graphic_override)



    t.Commit()


def process_line(ref_num, title, count, unit_area, program_area, note, graphic_override):
    pass

    # try find instance with ref_num, if not exist, create one
    type_name = "{}_{}".format(ref_num, title)

    family_type = REVIT_FAMILY.get_family_type_by_name(FAMILY_NAME, type_name, create_if_not_exist=True)

    instances = REVIT_FAMILY.get_family_instances_by_family_name_and_type_name(FAMILY_NAME, type_name)
    if len(instances) == 0:
        instance = doc.Create.NewFamilyInstance(DB.XYZ(0, 0, 0), family_type, doc.ActiveView)
    elif len(instances) == 1:
        instance = instances[0]
        
    elif len(instances) > 1:
        print ("more than one, badddddddd!")


    print (family_type)
    # update the data to instance
    family_type.LookupParameter("Count").Set(count)
    family_type.LookupParameter("UnitArea").Set(unit_area)
    family_type.LookupParameter("ProgramArea").Set(program_area)
    family_type.LookupParameter("Note").Set(note)
    family_type.LookupParameter("RefNum").Set(ref_num)
    family_type.LookupParameter("Title").Set(title)


    
    doc.ActiveView.SetElementOverrides (instance.Id, graphic_override)





################## main code below #####################


if __name__ == "__main__":
    output = script.get_output()
    output.close_others()
    excel_to_diagram()
    ENNEAD_LOG.use_enneadtab(coin_change = 20, tool_used = __title__.replace("\n", " "), show_toast = True)







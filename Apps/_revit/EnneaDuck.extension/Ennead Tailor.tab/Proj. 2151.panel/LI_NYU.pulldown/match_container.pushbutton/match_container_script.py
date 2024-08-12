#!/usr/bin/python
# -*- coding: utf-8 -*-

__doc__ = "Use container file as base to compare BIM data to other major NYULI docs for comsistensy"
__title__ = "Match Container"

import proDUCKtion # pyright: ignore 
proDUCKtion.validify()

from pyrevit import script

from EnneadTab import ERROR_HANDLE, LOG, NOTIFICATION, OUTPUT
from EnneadTab.REVIT import REVIT_APPLICATION
from Autodesk.Revit import DB # pyright: ignore 

# UIDOC = REVIT_APPLICATION.get_uidoc()
# DOC = REVIT_APPLICATION.get_doc()
import file_getter as FG
import system_family_checker as SFC

from collections import OrderedDict
EMOJI_DICT = OrderedDict({
    "Exist": ":ballot_box_with_check:",
    "NotExist":":question_mark:",
    "NoMatchType":":question_mark:",
    "NoMatchPara":":double_exclamation_mark:",
    "NoSame":":face_with_raised_eyebrow:",
    "Same":":thumbs_up:"
})



@LOG.log(__file__, __title__)
@ERROR_HANDLE.try_catch_error()
def match_container():

    container_file_title = "EAEC_NYU-Langone Health_Container File"
    if REVIT_APPLICATION.get_doc().Title == container_file_title:
        NOTIFICATION.messenger("Your active doc is the container file. Nothing to compare.")
        return None
    container_doc = FG.get_NYU_doc(doc_title = container_file_title)
    if not container_doc:
        return

    output.print_md("## Objective:")
    print (__doc__)
    output.print_md("## Icon Legend:")
    for key in EMOJI_DICT.keys():
        emoji = EMOJI_DICT[key]
        output.print_md("{}: {}".format(key, emoji))

    print ("\n\n")


        
    NYULI_list = [
        "2151_A_EA_NYULI_Hospital_EXT",
        "2151_A_EAEC_NYULI_Hospital_INT",
        "2151_A_EA_NYULI_Site",
        "2151_A_EA_NYULI_Parking East",
        "2151_A_EA_NYULI_Parking West",
        "2151_A_EA_NYULI_CUP_EXT"
    ]
    working_docs = [FG.get_NYU_doc(doc_title = x) for x in NYULI_list]
    working_docs = [x for x in working_docs if x is not None]
    SFC.process_system_family("Walls", container_doc, working_docs)
    SFC.process_system_family("Floors", container_doc, working_docs)
    SFC.process_system_family("Roofs", container_doc, working_docs)

    OUTPUT.display_output_on_browser()





################## main code below #####################
if __name__ == "__main__":
    output = script.get_output()
    match_container()







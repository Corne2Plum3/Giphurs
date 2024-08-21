"""
Add anchors points on accented glyphs, as long they're built using components (aka references to
other glyphs). The list of glyphs where to do this information must be manually specified, and
it's on a text file called ACCENTED_GLYPHS_LIST (see below in the code)

It modify the .glif file of those glyphs, overwriting all existing anchors on them.
"""

ACCENTED_GLYPHS_LIST = "sources/accented_glyphs_list.txt"

import sys
from ufo_get_glif_from_name import get_glif_from_name
import xml.etree.ElementTree as ET

# Returns a dict with all anchor points of a glyph, and for each anchor the coordinates in the format (x, y) (as int)
def get_anchor_points(glyph_name, ufo_dir):
    tree = ET.parse(get_glif_from_name(glyph_name, ufo_dir))
    xml_anchor_list = tree.getroot().findall("anchor")
    anchor_dict = {}
    for anchor in xml_anchor_list:
        anchor_dict[anchor.attrib["name"]] = (int(anchor.attrib["x"]), int(anchor.attrib["y"]))
    return anchor_dict

# Place the anchor points on an accented glyph
def set_anchor_points_on_accented_glyph(glyph_name, ufo_dir):
    # remove "/" at the end of the ufo_dir if here
    if ufo_dir[-1] == "/" or ufo_dir[-1] == "\\":
        ufo_dir = ufo_dir[:-1]

    # load file to edit
    tree = ET.parse(get_glif_from_name(glyph_name, ufo_dir))
    root = tree.getroot()
    xml_component_list = root.find("outline").findall("component")

    # remove the existing anchors
    xml_anchor_list = root.findall("anchor")
    for element in xml_anchor_list:
        root.remove(element)
    
    # read the anchors from each component
    anchors_full_list = []  # each anchor is a dict with the keys "name", "source", "component_order", "x", "y"
    component_order = 0
    component_count = len(xml_component_list)
    for component in xml_component_list:
        component_order += 1
        x_offset = 0
        y_offset = 0
        if "xOffset" in component.attrib:
            x_offset = int(component.attrib["xOffset"])
        if "yOffset" in component.attrib:
            y_offset = int(component.attrib["yOffset"])
        component_anchors_dict = get_anchor_points(component.attrib["base"], ufo_dir)
        for anchor in component_anchors_dict:
            new_anchor_entry = {}
            new_anchor_entry["name"] = anchor
            new_anchor_entry["source"] = component.attrib["base"]
            new_anchor_entry["component_order"] = component_order
            new_anchor_entry["x"] = component_anchors_dict[anchor][0] + x_offset
            new_anchor_entry["y"] = component_anchors_dict[anchor][1] + y_offset
            anchors_full_list.append(new_anchor_entry)

    # separate the base and mark anchors into 2 lists
    anchors_base_list = []  # [{"name": str, "component_order": str, "x": int, "y": int}]
    anchors_mark_list = []  # [{"name": str, "component_order": str, "x": int, "y": int}]
    for anchor in anchors_full_list:
        if anchor["name"][0] == "_":
            anchors_mark_list.append(anchor)
        else:
            anchors_base_list.append(anchor)
    
    # remove 2 anchors at the same place used to place components
    for anchor_mark in anchors_mark_list:
        i = 0
        while i < len(anchors_base_list):
            anchor_base = anchors_base_list[i]
            if anchor_mark["name"][1:] == anchor_base["name"] and anchor_mark["source"] != anchor_base["source"]:
                anchors_base_list.pop(i)
            i += 1

    # remove anchors starting with "mark_" of components between 2 components (result in anchors_base_list)
    i = 0
    while i < len(anchors_base_list):
        anchor = anchors_base_list[i] 
        if "mark_" in anchor["name"] and anchor["component_order"] != 1 and anchor["component_order"] != component_count:  # for example with 3 components, remove the "mark_" anchors for the component 2
            anchors_base_list.pop(i)
        else:
            i += 1

    # remove duplicate base anchors (result in anchors_final_list)
    anchors_final_list = []  # [{"name": str, "component_order": str, "x": int, "y": int}]
    anchors_final_names = {}  # {"name": <pos_in_anchors_final_list>}
    for anchor in anchors_base_list:
        if anchor["name"] in anchors_final_names:  # anchor already here
            already_existing_anchor_index = anchors_final_names[anchor["name"]]
            already_existing_anchor = anchors_final_list[already_existing_anchor_index]
            if anchor["component_order"] < already_existing_anchor["component_order"]:  # keep the one wirth the lowest component_order value
                anchors_final_list.pop(already_existing_anchor_index)
                anchors_final_list.append(anchor)
                anchors_final_names[anchor["name"]] = len(anchors_final_list) - 1
        else:
            anchors_final_list.append(anchor)
            anchors_final_names[anchor["name"]] = len(anchors_final_list) - 1

    # add the anchor to the xml tree (the mark signs are all ignored)
    for anchor in anchors_final_list:
        new_element_attribs = {
            "x": str(anchor["x"]),
            "y": str(anchor["y"]),
            "name": anchor["name"]
        }
        ET.SubElement(root, "anchor", new_element_attribs)
    
    # save
    tree.write(get_glif_from_name(glyph_name, ufo_dir), encoding='utf-8', xml_declaration=True)

def main():
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory>")
    else:
        print(f"{sys.argv[0]}: Working on {sys.argv[1]}")
        glyphs_counter = 0
        with open(ACCENTED_GLYPHS_LIST, "r") as file:
            for glyph in file:
                glyph_name_cleaned = glyph.strip().replace(" ", "")
                if glyph_name_cleaned != "":
                    if get_glif_from_name(glyph_name_cleaned, sys.argv[1]) == "":
                        pass  # get_glif_from_name already prints a warning
                    else:
                        set_anchor_points_on_accented_glyph(glyph_name_cleaned, sys.argv[1])
                        glyphs_counter += 1
        print(f"Done ({glyphs_counter} glyphs affected).")

if __name__ == "__main__":
    main()

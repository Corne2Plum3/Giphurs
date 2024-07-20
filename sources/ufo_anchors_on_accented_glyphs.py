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
    anchors_list_names = []
    anchors_list_pos = []
    anchors_mark_list_names = []

    # remove the existing anchors
    xml_anchor_list = root.findall("anchor")
    for element in xml_anchor_list:
        root.remove(element)
    
    # read the anchors from each component
    for component in xml_component_list:
        x_offset = 0
        y_offset = 0
        if "xOffset" in component.attrib:
            x_offset = int(component.attrib["xOffset"])
        if "yOffset" in component.attrib:
            y_offset = int(component.attrib["yOffset"])
        component_anchors_dict = get_anchor_points(component.attrib["base"], ufo_dir)
        for anchor in component_anchors_dict:  # anchor already here from another components -> we remove the anchor completly later and don't add the new one
            if anchor[0] == "_":  # add without the _ (they will get removed)
                anchors_mark_list_names.append(anchor[1:])
            else:
                anchors_list_names.append(anchor)
                anchors_list_pos.append((component_anchors_dict[anchor][0] + x_offset, component_anchors_dict[anchor][1] + y_offset))

    # remove the duplicate anchor
    for anchor in anchors_mark_list_names:
        if anchor in anchors_list_names:
            index = anchors_list_names.index(anchor)
            anchors_list_names.pop(index)
            anchors_list_pos.pop(index)

    # add the anchor sto the xml tree
    for anchor_index in range(len(anchors_list_names)):
        new_element_attribs = {
            "x": str(anchors_list_pos[anchor_index][0]),
            "y": str(anchors_list_pos[anchor_index][1]),
            "name": anchors_list_names[anchor_index]
        }
        ET.SubElement(root, "anchor", new_element_attribs)
    
    # save
    tree.write(get_glif_from_name(glyph_name, ufo_dir))

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
                        pass  # get_glif_from_name already print a warning
                    else:
                        set_anchor_points_on_accented_glyph(glyph_name_cleaned, sys.argv[1])
                        glyphs_counter += 1
        print(f"Done ({glyphs_counter} glyphs affected).")

if __name__ == "__main__":
    main()

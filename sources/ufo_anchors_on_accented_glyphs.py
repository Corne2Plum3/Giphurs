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
    #print(f"### {glyph_name} ###")

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
    
    # Read the anchors from each component
    # Each anchor will be a dict with the keys "name", "source", "x", "y"
    glyph_anchor_list = []  # List of the list of anchors of each component
    # Order: (mark_2), mark_1, base_glyph (order is important)
    # Example [ [{<anchor_1}, {<anchor_2}] , [{<_anchor_1}] ]
    component_count = len(xml_component_list)
    for component in xml_component_list:
        #print(component.attrib["base"])
        component_anchor_list = []
        # apply offset if the components isn't at (0,0)
        x_offset = 0
        y_offset = 0
        if "xOffset" in component.attrib:
            x_offset = int(component.attrib["xOffset"])
        if "yOffset" in component.attrib:
            y_offset = int(component.attrib["yOffset"])
        # Read each anchor
        component_anchors_dict = get_anchor_points(component.attrib["base"], ufo_dir)
        for anchor in component_anchors_dict:
            new_anchor_entry = {}
            new_anchor_entry["name"] = anchor
            new_anchor_entry["source"] = component.attrib["base"]
            new_anchor_entry["x"] = component_anchors_dict[anchor][0] + x_offset
            new_anchor_entry["y"] = component_anchors_dict[anchor][1] + y_offset
            component_anchor_list.append(new_anchor_entry)
        # Add the component's list to the glyph list
        glyph_anchor_list.append(component_anchor_list)
    #print(glyph_anchor_list)

    # Remove the achors used to attach 2 glyphs
    for i in range(0, component_count-1, 1):
        # mark_anchor_list = glyph_anchor_list[i]
        # base_anchor_list = glyph_anchor_list[i+1]
        im = 0  # index of the base component inside the mark's anchor list
        while im < len(glyph_anchor_list[i]):
            ib = 0  # index of the base component inside the glyphs's anchor list
            while im < len(glyph_anchor_list[i]) and ib < len(glyph_anchor_list[i+1]):
                #print(f"{glyph_anchor_list[i][im]["name"]} and {glyph_anchor_list[i+1][ib]["name"]}")
                if glyph_anchor_list[i][im]["name"][0] == "_" and glyph_anchor_list[i][im]["name"][1:] == glyph_anchor_list[i+1][ib]["name"]:  # attached anchors
                    glyph_anchor_list[i].pop(im)
                    glyph_anchor_list[i+1].pop(ib)
                    #print(f"Removing {glyph_anchor_list[i].pop(im)} and {glyph_anchor_list[i+1].pop(ib)}")
                    ib = 0
                else:
                    ib += 1
            im += 1

    # Remove the anchors of intermediate components
    while len(glyph_anchor_list) > 2:
        glyph_anchor_list.pop(1)
    #print(glyph_anchor_list)

    # Merge into a single list with the anchors we're going to keep
    glyph_anchor_list_merged = []
    for component in glyph_anchor_list:
        for anchor in component:
            glyph_anchor_list_merged.append(anchor)

    # Convert the 'mkmk' anchors into 'mark' (base to mark) anchors
    mkmk_convert = {
        "mkmk_top_center": "top_center"
    }
    for anchor in glyph_anchor_list_merged:
        if anchor["name"] in mkmk_convert.keys():
            #print(f"Renaming {anchor["name"]} -> {mkmk_convert[anchor["name"]]}")
            anchor["name"] = mkmk_convert[anchor["name"]]

    # Remove duplicates and remaining mark glyphs
    glyph_anchor_list_merged_names = []
    i = 0
    while i < len(glyph_anchor_list_merged):
        if glyph_anchor_list_merged[i]["name"] in glyph_anchor_list_merged_names:  # duplicate found, remove
            glyph_anchor_list_merged.pop(i)
            #print(f"Removing {glyph_anchor_list_merged.pop(i)}")
        elif glyph_anchor_list_merged[i]["name"][0] == "_":  # delete mark anchor
            glyph_anchor_list_merged.pop(i)
            #print(f"Removing {glyph_anchor_list_merged.pop(i)}")
        else:
            glyph_anchor_list_merged_names.append(glyph_anchor_list_merged[i]["name"])
            i += 1
    #print(glyph_anchor_list_merged)

    # add the anchor to the xml tree (the mark signs are all ignored)
    for anchor in glyph_anchor_list_merged:
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

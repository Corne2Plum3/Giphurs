"""
Build an accented glyph by palcing components (the list of components for each affected glyph on 
COMPONENTS_LIST).

Replace the outline and the anchors of the associated .glif file (if found)

Has an optional parameter to specify 1 glyph. If it's not here, will act on all glyphs on the 
COMPONENTS_LIST.

Fields on COMPONENTS_LIST:
glyph_name, allow_left_overflow, allow_right_overflow, base, component_1, component_2, ...
"""

import sys
from ufo_utils import *
import xml.etree.ElementTree as ET

# CSV with the format glyph_name ; component 1 ; component 2 ; ...
# WARNING: First line is ignored
COMPONENTS_LIST = "scripts/custom_components.csv"
COMPONENTS_LIST_DELIM = ";"
MKMK_ANCHORS_REPLACE = {
    "mkmk_top_center": "top_center",
    "mkmk_bottom_center": "bottom_center",
    "mkmk_greek_top_center": "top_center"  # under special conditions replaces mkmk_top_center
}

def get_glyph_component_list(glyph_name):
    """
    Reads the list of components of glyph_name from COMPONENTS_LIST.
    
    Returns `None` if the glyph is not found.
    """
    global COMPONENTS_LIST, COMPONENTS_LIST_DELIM
    with open(COMPONENTS_LIST, "r") as csv_file:
        csv_lines = csv_file.readlines()
        i = 1
        components_list = []

        while i < len(csv_lines) and csv_lines[i].split(COMPONENTS_LIST_DELIM)[0] != glyph_name:  # find the glyph on the list
            i += 1
            
        if csv_lines[i].split(COMPONENTS_LIST_DELIM)[0] == glyph_name:  # if found
            csv_entry = csv_lines[i].split(COMPONENTS_LIST_DELIM)
            j = 1
            while j < len(csv_entry):
                component = csv_lines[i].split(COMPONENTS_LIST_DELIM)[j].strip()
                if component != "":
                    components_list.append(component)
                j += 1
            
            #print(f"Found {len(components_list)} components for {glyph_name} at line {i+1}: {components_list}")
            return components_list
        
        # We're here if the glyph hasn't been found
        return None

def build_accented_glyph(glyph_name, ufo_dir):
    """
    Edit a .glif file and change generate the components.

    Returns nothing.
    """
    global COMPONENTS_LIST, COMPONENTS_LIST_DELIM, MKMK_ANCHORS_REPLACE

    # Load file to edit
    xml_tree = ET.parse(get_glif_from_name(glyph_name, ufo_dir))
    xml_root = xml_tree.getroot()

    # Find the glyph and its components
    components_list = []
    with open(COMPONENTS_LIST, "r") as csv_file:
        csv_lines = csv_file.readlines()
        i = 1  # ignore 1st line
        while i < len(csv_lines) and csv_lines[i].split(COMPONENTS_LIST_DELIM)[0] != glyph_name:  # find the glyph on the list
            i += 1
        if i == len(csv_lines):  # not found
            print(f"ERROR: Glyph {glyph_name} not found on {COMPONENTS_LIST} (line {i})")
            return
        csv_entry = csv_lines[i].split(COMPONENTS_LIST_DELIM)
        if len(csv_entry) < 4:
            print(f"ERROR: No components found for glyph {glyph_name} (line {i})")
            return
        j = 3
        while j < len(csv_entry):
            component = csv_lines[i].split(COMPONENTS_LIST_DELIM)[j].strip()
            if component != "":
                components_list.append(component)
            j += 1
        if glyph_name in components_list:  # avoid infinite recursion
            print(f"ERROR: Glyph {glyph_name} contains itself as component (line {i})")
            return
    
    # Retrieve parameters
    allow_left_overflow = bool(int(csv_lines[i].split(COMPONENTS_LIST_DELIM)[1].strip()))
    allow_right_overflow = bool(int(csv_lines[i].split(COMPONENTS_LIST_DELIM)[2].strip()))

    # Place components and anchors and get metrics of the base (when recalculate kerning)
    glyph_component = {}  # {"component": (xOffset, yOffset)}
    glyph_anchors = {}  # {"anchor_name": (x, y)}
    base_metrics = {}  # set by get_glyph_metrics()
    for i in range(len(components_list)):
        # Load anchor points
        new_component_anchors = get_glyph_anchor_points(components_list[i], ufo_dir)

        # Place component
        x_offset = 0
        y_offset = 0
        if i == 0:  # find the offset of the new component (ignore the step below for the base)
            glyph_component[components_list[i]] = (0, 0)
            base_metrics = get_glyph_metrics(components_list[i], ufo_dir)
        else:
            # Find a matching anchor
            placed_component = False
            glyph_anchors_keys = list(glyph_anchors.keys())  # have a list of all keys of the dicts
            new_component_anchors_keys = list(new_component_anchors.keys())
            ib = 0
            while placed_component == False and ib < len(glyph_anchors_keys):  # from the glyph we are building
                base_anchor = glyph_anchors_keys[ib]
                im = 0
                while placed_component == False and im < len(new_component_anchors_keys):  # from the component we're adding
                    mark_anchor = new_component_anchors_keys[im]
                    if placed_component == False and ("_" + base_anchor) == mark_anchor:  # found matching base/mark
                        x_offset = glyph_anchors[base_anchor][0] - new_component_anchors[mark_anchor][0]
                        y_offset = glyph_anchors[base_anchor][1] - new_component_anchors[mark_anchor][1]
                        glyph_component[components_list[i]] = (x_offset, y_offset)
                        glyph_anchors.pop(base_anchor)  # remove the 2 anchors from the anchor list
                        new_component_anchors.pop(mark_anchor)
                        glyph_anchors_keys = list(glyph_anchors.keys())  # update these too
                        new_component_anchors_keys = list(new_component_anchors.keys())
                        placed_component = True
                    else:
                        im += 1
                ib += 1
            if not placed_component:  # Anchor not found: apply no offset (shouldn't happen)
                print(f"WARNING: Couldn't find where to attach {components_list[i]} on {glyph_name}")
                glyph_component[components_list[i]] = (0, 0)

        # Save anchor on the dict glyph_anchors
        for new_anchor in new_component_anchors:
            x = new_component_anchors[new_anchor][0] + x_offset
            y = new_component_anchors[new_anchor][1] + y_offset
            glyph_anchors[new_anchor] = (x, y)  # replace if already here

    # Create a list with the name of all anchors
    glyph_anchors_keys = list(glyph_anchors.keys())

    # greek_* anchors : either we keep all of them or remove them all (greek_kt, greek_t, greek_k, greek_v)
    greek_anchors_count = 0
    for anchor in glyph_anchors_keys:  # This loop just counts them
        if anchor[0:6] == "greek_":
            greek_anchors_count += 1

    # Keep only mkmk_greek_top_center on lowercase and top_center on uppercase if both are here (detected by the x-coordinates of these 2 anchors if they are here) for U+1Fxx glyphs
    if "mkmk_greek_top_center" in glyph_anchors_keys and "top_center" in glyph_anchors_keys:
        if abs(glyph_anchors["mkmk_greek_top_center"][0] - glyph_anchors["top_center"][0]) < 5:  # lowercase
            del glyph_anchors["top_center"]
            glyph_anchors_keys.pop(glyph_anchors_keys.index("top_center")) 
        else:  # uppercase
            del glyph_anchors["mkmk_greek_top_center"]
            glyph_anchors_keys.pop(glyph_anchors_keys.index("mkmk_greek_top_center")) 

    # Clean the anchors (delete/replace)
    i = 0
    while i < len(glyph_anchors_keys):
        anchor = glyph_anchors_keys[i]
        if anchor[0] == "_":  # get rid of mark anchors
            glyph_anchors.pop(anchor)
            glyph_anchors_keys = list(glyph_anchors.keys())  # we have to update this to keep track of the list of used anchors
        elif anchor in MKMK_ANCHORS_REPLACE:  # replace mkmk anchor
            glyph_anchors[MKMK_ANCHORS_REPLACE[anchor]] = glyph_anchors[anchor]
            glyph_anchors.pop(anchor)
            glyph_anchors_keys = list(glyph_anchors.keys())
        elif anchor[0:6] == "greek_" and greek_anchors_count > 0 and greek_anchors_count < 4:  # delete greek accents (see above)
            glyph_anchors.pop(anchor)
            glyph_anchors_keys = list(glyph_anchors.keys())
        else:
            i += 1

    # Set the anchors on the XML
    xml_anchor_list = xml_root.findall("anchor")
    for element in xml_anchor_list:  # delete the already existing ones
        xml_root.remove(element)
    for anchor in glyph_anchors:  # place the one we just calculated
        ET.SubElement(xml_root, "anchor", {"x": str(glyph_anchors[anchor][0]), "y": str(glyph_anchors[anchor][1]), "name": anchor})
    
    # Set the components (the outline) on the XML
    xml_root.remove(xml_root.find("outline"))  # empty the componenets inside <outline>
    xml_outline = ET.SubElement(xml_root, "outline")
    for component in glyph_component:
        if glyph_component[component][0] == 0 and glyph_component[component][1] == 0:
            ET.SubElement(xml_outline, "component", {"base": component})
        else:
            ET.SubElement(xml_outline, "component", {"base": component, "xOffset": str(glyph_component[component][0]), "yOffset": str(glyph_component[component][1])})

    # Save the file
    xml_tree.write(get_glif_from_name(glyph_name, ufo_dir), encoding='utf-8', xml_declaration=True)

    # Update kern if needed
    current_glyph_metrics = get_glyph_metrics(glyph_name, ufo_dir)
    if (not allow_right_overflow) and current_glyph_metrics["x_max"] > base_metrics["glyph_width"]: 
        move_glyph(glyph_name, ufo_dir, current_glyph_metrics["x_max"] - base_metrics["glyph_width"], 0, False, False, True)
    if (not allow_left_overflow) and current_glyph_metrics["x_min"] < 0:
        move_glyph(glyph_name, ufo_dir, abs(current_glyph_metrics["x_min"]), 0, True, True, False)

    #print(f"Done with {glyph_name} ({len(glyph_component)} components, {len(glyph_anchors)} anchors)")
    return

def main():
    if len(sys.argv) < 2:
        print(f"ERROR: {sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory> [<glyph_name>]")
    else:
        if len(sys.argv) == 2:  # no specific glyph -> do all
            # get the list of what to do
            glyphs_list = []
            with open(COMPONENTS_LIST, "r") as csv_file:
                first_line_seen = False
                for csv_line in csv_file:
                    if not first_line_seen:  # then this is the first line (-> skip)
                        first_line_seen = True
                    else:
                        glyphs_list.append(csv_line.split(";")[0].strip())
            # act on each glyph
            print("Starting...")
            nb_glyphs = len(glyphs_list)
            for index, glyph in enumerate(glyphs_list):
                sys.stdout.write('\033[2K\033[1G')
                print(f"[{index}/{nb_glyphs} ({int((index-1)/nb_glyphs*100)}%)] Working on {glyph}...", end="\r")
                build_accented_glyph(glyph, sys.argv[1])
            print(f"Done with {sys.argv[1]} ({len(glyphs_list)} files changed)")
        else:
            build_accented_glyph(sys.argv[2], sys.argv[1])
        
if __name__ == "__main__":
    main()

"""
Build an accented glyph by palcing components (the list of components for each affected glyph on 
COMPONENTS_LIST).

Replace the outline and the anchors of the associated .glif file (if found)

Has an optional parameter to specify 1 glyph. If it's not here, will act on all glyphs on the 
COMPONENTS_LIST.

Fields on COMPONENTS_LIST:
glyph_name, allow_left_overflow, allow_right_overflow, base, component_1, component_2, ...
"""

from multiprocessing import Process
import sys
from ufo_utils import *
import xml.etree.ElementTree as ET

# CSV with the format glyph_name ; component 1 ; component 2 ; ...
# WARNING: First line is ignored
COMPONENTS_LIST = "scripts/accented_glyphs.csv"
COMPONENTS_LIST_DELIM = ";"
MKMK_ANCHORS_REPLACE = {
    "mkmk_top_center": "top_center",
    "mkmk_bottom_center": "bottom_center",
    "mkmk_greek_top_center": "top_center"  # under special conditions replaces mkmk_top_center
}

# Performances settings
USE_MULTITHREADING = True


def build_accented_glyph(glyph_name, ufo_dir, style, allow_left_overflow, allow_right_overflow, components_list):
    """
    Edit a .glif file and change generate the components.

    For 'style' argument: 1 = non-italic, 2 = italic.

    Returns 0 if success, non-zero if it fails.
    """
    global COMPONENTS_LIST, COMPONENTS_LIST_DELIM, MKMK_ANCHORS_REPLACE

    # Load file to edit
    glif_filename = get_glif_from_name(glyph_name, ufo_dir)
    xml_tree = ET.parse(glif_filename)
    xml_root = xml_tree.getroot()

    # Place components and anchors and get metrics of the base (when recalculate kerning)
    glyph_component = {}  # {"component": (xOffset, yOffset)}
    glyph_anchors = {}  # {"anchor_name": (x, y)}
    base_metrics = {}  # set by get_glyph_metrics()
    for i in range(len(components_list)):
        # Load anchor points
        new_component_anchors = get_glyph_anchor_points(components_list[i], ufo_dir)

        # Place component (and update glyph width on base)
        x_offset = 0
        y_offset = 0
        if i == 0:  # find the offset of the new component (ignore the step below for the base)
            glyph_component[components_list[i]] = (0, 0)
            base_metrics = get_glyph_metrics(components_list[i], ufo_dir)
            xml_tree.getroot().find("advance").attrib["width"] = str(base_metrics["glyph_width"])
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
    xml_tree.write(glif_filename, encoding='utf-8', xml_declaration=True)

    # Update kern if needed
    current_glyph_metrics = get_glyph_metrics(glyph_name, ufo_dir)
    if (not allow_right_overflow) and current_glyph_metrics["x_max"] > base_metrics["glyph_width"]:
        xml_root = move_glyph(glyph_name, ufo_dir, current_glyph_metrics["x_max"] - base_metrics["glyph_width"], 0, False, False, True)
    if (not allow_left_overflow) and current_glyph_metrics["x_min"] < 0:
        xml_root = move_glyph(glyph_name, ufo_dir, abs(current_glyph_metrics["x_min"]), 0, True, True, not allow_right_overflow)

    #print(f"Done with {glyph_name} ({len(glyph_component)} components, {len(glyph_anchors)} anchors)")
    return 0

def check_csv_entry(csv_line, glyph_name=None, style=None):
    """
    Read a line of COMPOSITE_GLYPHS_LIST given as a string.
    It is possible to check if it corresponds to a specific glyph name and/or a style
    If the line is valid and applies to the style given, then returns 0,
    otherwise returns a non-zero value, depending on the issue.
    """
    csv_data = csv_line.strip().split(COMPONENTS_LIST_DELIM)
    for i in range(len(csv_data)):  # remove whitespaces
        csv_data[i] = csv_data[i].strip()

    # Number of columns check:
    if len(csv_data) < 5:
        return 1  # Not enough parameters
    
    # Style entry check
    csv_style_value = None
    try:
        csv_style_value = int(csv_data[1])
    except:
        return 2  # Style field is not an integer

    # Self reference check (to avoid infinite recursion)
    if csv_data[0] in csv_data[4:]:
        return 3  # Glyph refers itself as component

    # Glyph name matching check
    if not glyph_name is None:
        if glyph_name != csv_data[0]:
            return 4  # Glyph name is not matching

    # Style support check
    if not style is None:
        line_non_italic_support = bool(int(csv_style_value) & 1)
        line_italic_support = bool(int(csv_style_value) & 2)
        if not((style == 1 and line_non_italic_support) or (style == 2 and line_italic_support)):
            return 5  # Unsupported style
    
    # All good :)
    return 0

def main():

    # Read parameters
    if len(sys.argv) < 3:
        print(f"ERROR: {sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory> <style> [<glyph_name>]")
        print("* style: 1 = non-italic ; 2 = italic")
        print("If a glyph name isn't provided, all accented glyphs from the font will be built")
        return

    ufo_dir = sys.argv[1]
    style = int(sys.argv[2])
    glyph_name = None if len(sys.argv) == 3 else sys.argv[3]

    # Get the list of glyphs to do. Result is in 'glyphs_list', a 2d matrix, with each rows looking like the CSV file:
    # [0] Glyph Name (str)
    # [1] Supported styles (int)
    # [2] Allow left overflow (bool)
    # [3] Allow right overflow (bool)
    # [4+] Components (str)
    glyphs_list_data = []
    with open(COMPONENTS_LIST, "r") as csv_file:
        csv_lines = csv_file.readlines()
        first_line_seen = False
        for line_number, csv_line in enumerate(csv_lines, start=1):
            if not first_line_seen:  # then this is the first line (-> skip)
                first_line_seen = True
            else:
                csv_line_check = check_csv_entry(csv_line, glyph_name, style)
                # -- Valid line
                if csv_line_check == 0:
                    csv_line_splitted = csv_line.strip().split(COMPONENTS_LIST_DELIM)  # all elements are strings!
                    new_entry = []
                    for i in range(len(csv_line_splitted)):  # remove whitespaces
                        if not csv_line_splitted[i] == "":
                            if i == 1:  # Styles -> int
                                csv_line_splitted[i] = int(csv_line_splitted[i])
                            elif i == 2 or i == 3:  # Allow left/right overflow -> bool
                                csv_line_splitted[i] = not csv_line_splitted[i].lower() in ["", "0", "no"]
                            new_entry.append(csv_line_splitted[i])
                    glyphs_list_data.append(new_entry)
                # -- Errors on the line
                elif csv_line_check == 1:
                    print(f"WARNING: Not enough parameters at line {line_number}, skipping.")
                elif csv_line_check == 2:
                    print(f"WARNING: 'Style' field isn't an integer at line {line_number}, skipping.")
                elif csv_line_check == 3:
                    print(f"WARNING: The glyph at line {line_number} contains itself as component, skipping.")
                # -- The style and eventually the glyph name don't match
                # do nothing
    
    # Check the possible errors before build and correct them if possible
    # -- The glyph specified doesn't exists [FATAL]
    if not glyph_name is None and len(glyphs_list_data) == 0:
        print(f"ERROR: Don't know how to build {glyph_name} for style={style}")
        exit(1)
    # -- A specified glyph appears twice (NOT checked if building all glyphs)
    if not glyph_name is None and len(glyphs_list_data) > 1:
        print(f"WARNING: More than 1 recipe found for {glyph_name} for style={style}: only the first one will be used")
        glyphs_list_data = [glyphs_list_data[0]]
    # -- 0 glyphs to build [FATAL]
    if len(glyphs_list_data) == 0:
        print(f"ERROR: No glyph to build for style={style}")
        exit(2)
    
    # Build the accented glyphs
    print("Starting...")
    nb_glyphs = len(glyphs_list_data)
    if USE_MULTITHREADING:
        processes = [Process(target=build_single_glyph, args=(glyphs_list_data[i], ufo_dir, style, i, nb_glyphs)) for i in range(nb_glyphs)]
        # start all processes
        for process in processes:
            process.start()
        # wait for all processes to complete
        for process in processes:
            process.join()
    else:  # single thread (recommended for debug)
        for i in range(nb_glyphs):
            build_single_glyph(glyphs_list_data[i], ufo_dir, style, i, nb_glyphs)

    # End message
    if glyph_name is None:
        print(f"Done with {sys.argv[1]} ({nb_glyphs} files changed)", flush=True)
    else:
        print(f"Done building {glyph_name} in {sys.argv[1]} ({nb_glyphs} files changed)", flush=True)


def build_single_glyph(glyph_data, ufo_dir, style, index, nb_glyphs):
    """
    Sub-process of main() supposed to work in parallel which read a line of glyph_list.
    Ne retourne rien.
    """

    current_glyph_name = glyph_data[0]
    current_glyph_left_overflow = glyph_data[2]
    current_glyph_right_overflow = glyph_data[3]
    current_glyph_components = glyph_data[4:]

    sys.stdout.write('\033[2K\033[1G')
    print(f"[{index+1}/{nb_glyphs} ({int((index+1)/nb_glyphs*100)}%)] Working on {current_glyph_name}...", end="\r")

    build_accented_glyph(current_glyph_name, ufo_dir, style, current_glyph_left_overflow, current_glyph_right_overflow, current_glyph_components)


if __name__ == "__main__":
    main()

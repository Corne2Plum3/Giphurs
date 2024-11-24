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
from ufo_get_glif_from_name import get_glif_from_name
import xml.etree.ElementTree as ET

# CSV with the format glyph_name ; component 1 ; component 2 ; ...
# WARNING: First line is ignored
COMPONENTS_LIST = "sources/custom_components.csv"
COMPONENTS_LIST_DELIM = ";"
MKMK_ANCHORS_REPLACE = {
    "mkmk_top_center": "top_center",
    "mkmk_bottom_center": "bottom_center"
}

def get_glyph_anchor_points(glyph_name, ufo_dir):
    """
    Find the anchors points from a .glif file.
    
    Returns a dict with all anchor points of a glyph, and for each anchor the coordinates (`int`):
    `{"anchor_name_1": (x1, y1), "anchor_name_2": (x2, y2), ...}`
    """
    xml_tree = ET.parse(get_glif_from_name(glyph_name, ufo_dir))
    xml_anchor_list = xml_tree.getroot().findall("anchor")
    anchor_dict = {}
    for anchor in xml_anchor_list:
        anchor_dict[anchor.attrib["name"]] = (int(anchor.attrib["x"]), int(anchor.attrib["y"]))
    return anchor_dict

def get_glyph_component_list(glyph_name):
    """
    Reads the list of components of glyph_name from COMPONENTS_LIST
    
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

def get_glyph_metrics(glyph_name, ufo_dir):
    """
    Returns a dict with some informations about the metrics of the glyph:

    `{"glyph_width": int, "left_kern": int, "right_kern": int, "x_min": int, "x_max": int", 
    "y_min": int, "y_max": int}`
    """
    glyph_width = get_glyph_width(glyph_name, ufo_dir)
    points_list = get_glyph_points_coordinates(glyph_name, ufo_dir)
    if len(points_list) == 0:  # no points...
        return {
            "glyph_width": glyph_width,
            "left_kern": 0,
            "right_kern": glyph_width,
            "x_min": 0,
            "x_max": 0,
            "y_min": 0,
            "y_max": 0
        }
    else:
        x_points = [ p[0] for p in points_list ]
        y_points = [ p[1] for p in points_list ]
        return {
            "glyph_width": glyph_width,
            "left_kern": min(x_points),
            "right_kern": glyph_width - max(x_points),
            "x_min": min(x_points),
            "x_max": max(x_points),
            "y_min": min(y_points),
            "y_max": max(y_points)
        }

def get_glyph_points_coordinates(glyph_name, ufo_dir):
    """
    Returns a list of couple (int, int) with the coordinate of all points (from all contours):
    `[(x1, y1), (x2, y2), ...]`

    If the glyphs include components, it also include their points, applying the correct offset.
    """
    xml_tree = ET.parse(get_glif_from_name(glyph_name, ufo_dir))
    xml_outline = xml_tree.getroot().find("outline")
    points_list = []
    for element in xml_outline:
        if element.tag == "contour":
            for point in element.findall("point"):
                points_list.append((int(point.attrib["x"]), int(point.attrib["y"])))
        elif element.tag == "component":
            components_points_list = get_glyph_points_coordinates(element.attrib["base"], ufo_dir)
            x_offset = 0
            if "xOffset" in element.attrib:
                x_offset = int(element.attrib["xOffset"])
            y_offset = 0
            if "yOffset" in element.attrib:
                y_offset = int(element.attrib["yOffset"])
            for point in components_points_list:
                points_list.append((point[0] + x_offset, point[1] + y_offset))
    return points_list

def get_glyph_width(glyph_name, ufo_dir):
    """
    Returns the glyph width (`int`) by reading the <advance> tag from its .glif file of the glyph specified.
    """
    xml_tree = ET.parse(get_glif_from_name(glyph_name, ufo_dir))
    return int(xml_tree.getroot().find("advance").attrib["width"])

def move_glyph(glyph_name, ufo_dir, x, y, move_points=True, move_anchors=True, move_width=False):
    """
    Translate all elements of the glyphs by (x, y). The parameter `move_width`, if set to True,
    also moves change the glyph's width by x.

    Returns nothing.
    """
    filename = get_glif_from_name(glyph_name, ufo_dir)
    xml_tree = ET.parse(filename)
    xml_root = xml_tree.getroot()
    for element in xml_root.findall("./*"):
        if element.tag == "advance" and move_width:
            element.attrib["width"] = str(int(element.attrib["width"]) + x)
        elif element.tag == "anchor" and move_anchors:
            element.attrib["x"] = str(int(element.attrib["x"]) + x)
            element.attrib["y"] = str(int(element.attrib["y"]) + y)
        elif element.tag == "outline" and move_points:
            for outline_element in element.findall("./*"):
                if outline_element.tag == "contour":
                    for contour_element in outline_element.findall("./*"):
                        if contour_element.tag == "point":
                            contour_element.attrib["x"] = str(int(contour_element.attrib["x"]) + x)
                            contour_element.attrib["y"] = str(int(contour_element.attrib["y"]) + y)
                elif outline_element.tag == "component":
                    if "xOffset" in outline_element.attrib:
                        outline_element.attrib["xOffset"] = str(int(outline_element.attrib["xOffset"]) + x)
                    else:
                        outline_element.attrib["xOffset"] = str(x)
                    if "yOffset" in outline_element.attrib:
                        outline_element.attrib["yOffset"] = str(int(outline_element.attrib["yOffset"]) + y)
                    else:
                        outline_element.attrib["yOffset"] = str(y)
        # ignore other type of elements, keeping them as is
    xml_tree.write(filename, encoding="UTF-8", xml_declaration=True)
    return

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
            print(f"ERROR: Glyph {glyph_name} not found on {COMPONENTS_LIST}")
            return
        csv_entry = csv_lines[i].split(COMPONENTS_LIST_DELIM)
        if len(csv_entry) < 4:
            print(f"ERROR: No components found for glyph {glyph_name} at line {i}")
            return
        j = 3
        while j < len(csv_entry):
            component = csv_lines[i].split(COMPONENTS_LIST_DELIM)[j].strip()
            if component != "":
                components_list.append(component)
            j += 1
    
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

    # Clean the anchors (delete/replace)
    i = 0
    glyph_anchors_keys = list(glyph_anchors.keys())
    while i < len(glyph_anchors_keys):
        anchor = glyph_anchors_keys[i]
        if anchor[0] == "_":  # get rid of mark anchors
            glyph_anchors.pop(anchor)
            glyph_anchors_keys = list(glyph_anchors.keys())
        elif anchor in MKMK_ANCHORS_REPLACE:  # replace mkmk anchor
            glyph_anchors[MKMK_ANCHORS_REPLACE[anchor]] = glyph_anchors[anchor]
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

    print(f"Done with {glyph_name} ({len(glyph_component)} components, {len(glyph_anchors)} anchors)")
    return

def main():
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: Not enough parameters.")
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
            for glyph in glyphs_list:
                build_accented_glyph(glyph, sys.argv[1])
            print(f"Done with {sys.argv[1]} ({len(glyphs_list)} files changed)")
        else:
            build_accented_glyph(sys.argv[2], sys.argv[1])
        
if __name__ == "__main__":
    main()

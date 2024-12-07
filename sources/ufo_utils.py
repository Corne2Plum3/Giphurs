"""
Various useful functions to interact with ufo directories, and more especially the glyphs inside.

Note: All glyphs must be located to a folder called "glyphs" to work correctly.   
"""

import sys
import xml.etree.ElementTree as ET

def get_glif_from_name(glyph_name, ufo_dir):
    """
    Reads the glyphs/contents.plist and retrive the path of the .glif file associated with the glyph
    with the name specified.

    Usage: get_glif_from_name(glyph_name, ufo_dir)
    * glyph_name: The name of the glyph
    * ufo_dir: The ufo directory.
    """
    # remove "/" at the end of the ufo_dir if here
    if ufo_dir[-1] == "/" or ufo_dir[-1] == "\\":
        ufo_dir = ufo_dir[:-1]

    # open contents.plist
    tree = ET.parse(f"{ufo_dir}/glyphs/contents.plist")
    glyphs_dict = tree.getroot().find("dict")

    # find glyph_name
    key_list = glyphs_dict.findall("key")
    string_list = glyphs_dict.findall("string")
    index = 0
    glyph_found = False
    while glyph_found == False and index < len(key_list):
        if key_list[index].text == glyph_name:
            glyph_found = True
        else:
            index += 1

    # return
    if glyph_found:
        return f"{ufo_dir}/glyphs/{string_list[index].text}"
    else:
        print(f"{sys.argv[0]}: WARNING: Glyph not found: {glyph_name}")
        return ""

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

    Changes UFO file.

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

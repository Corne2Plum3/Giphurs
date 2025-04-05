"""
This python script builds composite glyphs i.e. glyphs made of 1 or more characters (for example,
"IJ", made of a I and J, or Alpha, which is just the letter A).

It replies on a CSV file, `COMPOSITE_GLYPHS_LIST`, in the following format, telling the components
of glyphs, and if anchors should be kept (should be 0 if there are several compoents).

Replace the outline and the anchors of the associated .glif file (if found). If no glyph is
specified, it will act on all glyphs listed by `COMPOSITE_GLYPHS_LIST`

Usage: python3 PATH_TO_THIS_SCRIPT <ufo_directory> [<glyph_name>]
"""

import sys
from ufo_utils import *
import xml.etree.ElementTree as ET

# CSV with the format Glyph Name ; Copy anchors ; Glyph 1 ; Glyph 2 ; Glyph 3 ; Glyph 4 ; ...
# Copy anchors contains a number (0 or 1)
# WARNING: First line is ignored
COMPOSITE_GLYPHS_LIST = "scripts/composite_glyphs.csv"
COMPOSITE_GLYPHS_LIST_DELIM = ";"

def build_composite_glyph(glyph_name, ufo_dir, style, copy_anchors, components_list):
    """
    Build the composite glyph `glyph_name` using its components listed from `COMPOSITE_GLYPHS_LIST`.
    
    Changes UFO .glif file of destination glyph.

    For 'style' argument: 1 = non-italic, 2 = italic.

    Return `0` if sucess, non-zero integer if it fails.
    """

    # Place components
    x_cursor = 0
    for component_number in range(0, len(components_list), 1):
        component_name = components_list[component_number]
        copy_single_glyph(component_name, glyph_name, ufo_dir, copy_anchors, component_number==0, x_cursor, 0)
        x_cursor += get_glyph_metrics(component_name, ufo_dir)["glyph_width"]
        if (component_number + 1) < len(components_list):  # apply kern with the next element
            x_cursor += get_kerning(components_list[component_number], components_list[component_number+1], ufo_dir)
    
    # Update the advance value
    filename = get_glif_from_name(glyph_name, ufo_dir)
    xml_tree = ET.parse(filename)
    xml_tree.getroot().find("advance").attrib["width"] = str(x_cursor)
    xml_tree.write(filename, encoding="UTF-8", xml_declaration=True)
    
    return 0

def copy_single_glyph(glyph_src, glyph_dst, ufo_dir, copy_anchors=True, replace_all=True, x_offset=0, y_offset=0):
    """
    Copy `glyph_src` into `glyph_dst`, without changing its name not Unicode value.
    Can also copy anchors with `copy_anchors` set to `True`.

    Changes UFO .glif file of destination glyph.

    Returns nothing
    """
    # get source anchors and outline
    src_xml_tree = ET.parse(get_glif_from_name(glyph_src, ufo_dir))
    src_xml_root = src_xml_tree.getroot()
    src_anchor_list = src_xml_root.findall("anchor") if copy_anchors else []

    # Parse destination glyph XML
    dst_xml_tree = ET.parse(get_glif_from_name(glyph_dst, ufo_dir))
    dst_xml_root = dst_xml_tree.getroot()

    # Clear old anchors and outline if replace_all
    if replace_all:
        xml_anchor_list = dst_xml_root.findall("anchor")
        for element in xml_anchor_list:  # delete the already existing ones
            dst_xml_root.remove(element)
        xml_outline_list = dst_xml_root.findall("outline")
        for element in xml_outline_list:  # delete the already existing ones
            dst_xml_root.remove(element)
        ET.SubElement(dst_xml_root, "outline")

    # Copy the anchors
    if copy_anchors:
        for src_anchor in src_anchor_list:
            dst_anchor_attribs = {
                "x": str(int(src_anchor.attrib["x"]) + x_offset),
                "y": str(int(src_anchor.attrib["y"]) + y_offset),
                "name": src_anchor.attrib["name"]
            }
            ET.SubElement(dst_xml_root, "anchor", dst_anchor_attribs)
    
    # Copy the outline
    new_component_attrib = {
        "base": glyph_src,
        "xOffset": str(x_offset),
        "yOffset": str(y_offset)
    }
    ET.SubElement(dst_xml_root.find("outline"), "component", new_component_attrib)

    # Save
    dst_xml_tree.write(get_glif_from_name(glyph_dst, ufo_dir), encoding='utf-8', xml_declaration=True)
    return

def check_csv_entry(csv_line, glyph_name=None, style=None):
    """
    Read a line of COMPOSITE_GLYPHS_LIST given as a string.
    It is possible to check if it corresponds to a specific glyph name and/or a style
    If the line is valid and applies to the style given, then returns 0,
    otherwise returns a non-zero value, depending on the issue.
    """
    csv_data = csv_line.split(COMPOSITE_GLYPHS_LIST_DELIM)
    for i in range(len(csv_data)):  # remove whitespaces
        csv_data[i] = csv_data[i].strip()

    # Number of columns check:
    if len(csv_data) < 4:
        return 1  # Not enough parameters
    
    # Style entry check
    csv_style_value = None
    try:
        csv_style_value = int(csv_data[1])
    except:
        return 2  # Style field is not an integer

    # Self reference check (to avoid infinite recursion)
    if csv_data[0] in csv_data[3:]:
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
        print("If a glyph name isn't provided, all composite glyphs from the font will be built.")
        return
    
    ufo_dir = sys.argv[1]
    style = int(sys.argv[2])
    glyph_name = None if len(sys.argv) == 3 else sys.argv[3]

    # Get the list of glyphs to do. Result is in 'glyphs_list', a 2d matrix, with each rows looking like the CSV file:
    # [0] Glyph Name (str)
    # [1] Supported style (int)
    # [2] Copy Anchors (bool)
    # [3+] Components (str)
    glyphs_list_data = []
    with open(COMPOSITE_GLYPHS_LIST, "r") as csv_file:
        csv_lines = csv_file.readlines()
        first_line_seen = False
        for line_number, csv_line in enumerate(csv_lines, start=1):
            if not first_line_seen:  # then this is the first line (-> skip)
                first_line_seen = True
            else:
                csv_line_check = check_csv_entry(csv_line, glyph_name, style)
                # -- Valid line
                if csv_line_check == 0:
                    csv_line_splitted = csv_line.strip().split(COMPOSITE_GLYPHS_LIST_DELIM)  # all elements are strings!
                    new_entry = []
                    for i in range(len(csv_line_splitted)):  # remove whitespaces
                        if not csv_line_splitted[i] == "":
                            if i == 1:  # Styles -> int
                                csv_line_splitted[i] = int(csv_line_splitted[i])
                            elif i == 2:  # Copy anchors -> bool
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
    
    # Build the composite glyphs
    print("Starting...")
    nb_glyphs = len(glyphs_list_data)
    sucess_count = 0
    for index, glyph_data in enumerate(glyphs_list_data, start=0):
        current_glyph_name = glyph_data[0]
        current_glyph_copy_anchors = glyph_data[2]
        current_glyph_components = glyph_data[3:]

        sys.stdout.write('\033[2K\033[1G')
        print(f"[{index}/{nb_glyphs} ({int((index-1)/nb_glyphs*100)}%)] Working on {current_glyph_name}...", end="\r")

        build_status = build_composite_glyph(current_glyph_name, ufo_dir, style, current_glyph_copy_anchors, current_glyph_components)
        if build_status == 0:
            sucess_count += 1

    # End message
    if glyph_name is None:
        print(f"Done with {sys.argv[1]} ({sucess_count}/{nb_glyphs} files changed)")
    else:
        print(f"Done building {glyph_name} in {sys.argv[1]} ({sucess_count}/{nb_glyphs} files changed)")

if __name__ == "__main__":
    main()

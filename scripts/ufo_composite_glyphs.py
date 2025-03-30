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

def build_composite_glyph(glyph_name, ufo_dir, style=1):
    """
    Build the composite glyph `glyph_name` using its components listed from `COMPOSITE_GLYPHS_LIST`.
    
    Changes UFO .glif file of destination glyph.

    Return `0` if sucess, non-zero integer if it fails.
    """
    # Get compoents
    copy_anchors = False
    with open(COMPOSITE_GLYPHS_LIST, "r") as csv_file:
        csv_lines = csv_file.readlines()
        line_number = 1
        components_list = []

        # find the glyph on the list (find its index -> line_number)
        glyph_found = False
        while line_number < len(csv_lines) and not glyph_found:  # find the glyph on the list
            line_glyph_name = csv_lines[line_number].split(COMPOSITE_GLYPHS_LIST_DELIM)[0]
            line_styles = csv_lines[line_number].split(COMPOSITE_GLYPHS_LIST_DELIM)[1]
            line_non_italic_support = bool(int(line_styles) & 1)
            line_italic_support = bool(int(line_styles) & 2)
            if line_glyph_name == glyph_name and ((style == 1 and line_non_italic_support) or (style == 2 and line_italic_support)):
                glyph_found = True
            else:
                line_number += 1

        if line_number >= len(csv_lines):  # end of file reached
            print(f"ERROR: Glyph {glyph_name} not found on {COMPOSITE_GLYPHS_LIST} for style={style}")
            return 1
        
        csv_entry = csv_lines[line_number].split(COMPOSITE_GLYPHS_LIST_DELIM)

        if len(csv_entry) < 4:  # 0 components found or missing parameters
            print(f"ERROR: Invalid entry for {glyph_name} (line {line_number+1})")
            return 2

        # Read the "Copy anchors" parameter
        copy_anchors = bool(int(csv_entry[2]))

        column_number = 3
        while column_number < len(csv_entry):
            cell_value = csv_entry[column_number].strip()
            if cell_value != "":
                components_list.append(cell_value)
            column_number += 1

        if glyph_name in components_list:  # avoid infinite recursion
            print(f"ERROR: Glyph {glyph_name} contains itself as component (line {line_number+1})")
            return 3
    
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

def main():
    if len(sys.argv) < 3:
        print(f"ERROR: {sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory> <style> [<glyph_name>]")
        print("* style: 1 = non-italic ; 2 = italic")
        print("If a glyph name isn't provided, all composite glyphs from the font will be built.")
    else:
        if len(sys.argv) == 3:  # no specific glyph -> do all
            # get the list of what to do
            glyphs_list = []
            with open(COMPOSITE_GLYPHS_LIST, "r") as csv_file:
                first_line_seen = False
                for csv_line in csv_file:
                    if not first_line_seen:  # then this is the first line (-> skip)
                        first_line_seen = True
                    else:
                        glyphs_list.append(csv_line.split(";")[0].strip())
            # act on each glyph
            print("Starting...")
            nb_glyphs = len(glyphs_list)
            sucess_count = 0
            for index, glyph in enumerate(glyphs_list, start=1):
                sys.stdout.write('\033[2K\033[1G')
                print(f"[{index}/{nb_glyphs} ({int((index-1)/nb_glyphs*100)}%)] Working on {glyph}...", end="\r")
                build_status = build_composite_glyph(glyph, sys.argv[1], int(sys.argv[2]))
                if build_status == 0:
                    sucess_count += 1
            print(f"Done with {sys.argv[1]} ({sucess_count}/{len(glyphs_list)} files changed)")
        else:  # single glyph
            build_status = build_composite_glyph(sys.argv[3], sys.argv[1], int(sys.argv[2]))
            if build_status == 0:
                print(f"Done building {sys.argv[3]}")
            else:
                print(f"Failed building {sys.argv[3]}")

if __name__ == "__main__":
    main()

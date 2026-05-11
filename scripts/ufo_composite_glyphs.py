"""
This python script builds composite glyphs i.e. glyphs made of 1 or more characters (for example,
"IJ", made of a I and J, or Alpha, which is just the letter A).

It replies on a CSV file, `COMPOSITE_GLYPHS_LIST`, in the following format, telling the components
of glyphs, and if anchors should be kept (should be 0 if there are several compoents).

Replace the outline and the anchors of the associated .glif file (if found). If no glyph is
specified, it will act on all glyphs listed by `COMPOSITE_GLYPHS_LIST`

Usage: python3 PATH_TO_THIS_SCRIPT <ufo_directory> [<glyph_name>]
"""

from multiprocessing import Process
import sys
from ufo_utils import *
import xml.etree.ElementTree as ET

# CSV with the format Glyph Name ; Copy anchors ; Glyph 1 ; Glyph 2 ; Glyph 3 ; Glyph 4 ; ...
# Copy anchors contains a number (0 or 1)
# WARNING: First line is ignored
COMPOSITE_GLYPHS_LIST = "scripts/composite_glyphs.csv"
COMPOSITE_GLYPHS_LIST_DELIM = ";"

# Performances settings
USE_MULTITHREADING = True


class Composite_Glyph():
    def __init__(self, name: str, styles: int, copy_anchor: bool, components: list[str]):
        self.name = name
        self.styles = styles
        self.copy_anchor = copy_anchor
        self.components = components


def build_composite_glyph(glyph_name: str,
                          ufo_dir: Path,
                          style: int, 
                          copy_anchors: bool, 
                          components_list: list[str]) -> None:
    """
    Build the composite glyph `glyph_name` using its components listed from `COMPOSITE_GLYPHS_LIST`.
    
    Changes UFO .glif file of destination glyph.

    For 'style' argument: 1 = non-italic, 2 = italic.

    Return `0` if sucess, non-zero integer if it fails.
    """

    # Place components
    x_cursor: int = 0
    for component_number in range(0, len(components_list), 1):
        component_name: str = components_list[component_number]
        copy_single_glyph(component_name, glyph_name, ufo_dir, copy_anchors, component_number==0, x_cursor, 0)
        x_cursor += get_glyph_metrics(component_name, ufo_dir)["glyph_width"]
        if (component_number + 1) < len(components_list):  # apply kern with the next element
            x_cursor += get_kerning(components_list[component_number], components_list[component_number+1], ufo_dir)
    
    # Update the advance value
    glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
    if glif is None:
        return
    xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif)
    xml_advance: ET.Element[str] | None = xml_tree.getroot().find("advance")
    if xml_advance is None:
        return
    xml_advance.attrib["width"] = str(x_cursor)
    xml_tree.write(glif, encoding="UTF-8", xml_declaration=True)
    return

def copy_single_glyph(glyph_src: str,
                      glyph_dst: str,
                      ufo_dir: Path,
                      copy_anchors: bool = True,
                      replace_all: bool = True,
                      x_offset: int = 0,
                      y_offset: int = 0) -> None:
    """
    Copy `glyph_src` into `glyph_dst`, without changing its name not Unicode value.
    Can also copy anchors with `copy_anchors` set to `True`.

    Changes UFO .glif file of destination glyph.

    Returns nothing
    """
    # get source anchors and outline
    src_glif: Path | None = get_glif_from_name(glyph_src, ufo_dir)
    if src_glif is None:
        return
    src_xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(src_glif)
    src_xml_root: ET.Element[str] = src_xml_tree.getroot()
    src_anchor_list: list[ET.Element[str]] = src_xml_root.findall("anchor") if copy_anchors else []

    # Parse destination glyph XML
    dst_glif: Path | None = get_glif_from_name(glyph_dst, ufo_dir)
    if dst_glif is None:
        return
    dst_xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(dst_glif)
    dst_xml_root: ET.Element[str] = dst_xml_tree.getroot()

    # Clear old anchors and outline if replace_all
    if replace_all:
        xml_anchor_list: list[ET.Element[str]] = dst_xml_root.findall("anchor")
        for element in xml_anchor_list:  # delete the already existing ones
            dst_xml_root.remove(element)
        xml_outline_list: list[ET.Element[str]] = dst_xml_root.findall("outline")
        for element in xml_outline_list:  # delete the already existing ones
            dst_xml_root.remove(element)
        ET.SubElement(dst_xml_root, "outline")

    # Copy the anchors
    if copy_anchors:
        for src_anchor in src_anchor_list:
            dst_anchor_attribs: dict[str, str] = {
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
    dst_xml_outline: ET.Element[str] | None = dst_xml_root.find("outline")
    if dst_xml_outline is None:  # This shouldn't happen
        print(f'[ERROR] Somehow couldn\'t find <outline> when copying {glyph_src} into {glyph_dst}')
        return
    ET.SubElement(dst_xml_outline, "component", new_component_attrib)

    # Save
    dst_xml_tree.write(dst_glif, encoding='utf-8', xml_declaration=True)
    return

def check_csv_entry(csv_line: str, glyph_name: str | None = None, style: int | None = None) -> int:
    """
    Read a line of COMPOSITE_GLYPHS_LIST given as a string and check if the line is valid.
    It is possible to check if it corresponds to a specific glyph name and/or a style
    If the line is valid and applies to the style given, then returns 0, otherwise returns a non-zero
    value, depending on the issue.
    Value for style : 1 = non-italic ; 2 = italic ; 3 = both
    """
    csv_data: list[str] = csv_line.split(COMPOSITE_GLYPHS_LIST_DELIM)
    for i in range(len(csv_data)):  # remove whitespaces
        csv_data[i] = csv_data[i].strip()

    # Number of columns check:
    if len(csv_data) < 4:
        return 1  # Not enough parameters
    
    # Style entry check
    csv_style_value: int
    try:
        csv_style_value = int(csv_data[1])
    except:
        return 2  # Style field is not an integer

    # Self reference check (to avoid infinite recursion)
    if csv_data[0] in csv_data[3:]:
        return 3  # Glyph refers itself as component

    # Glyph name matching check
    if glyph_name is not None:
        if glyph_name != csv_data[0]:
            return 4  # Glyph name is not matching

    # Style support check
    if style is not None:
        line_non_italic_support: bool = bool(int(csv_style_value) & 1)
        line_italic_support: bool = bool(int(csv_style_value) & 2)
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
    
    ufo_dir: Path = Path(sys.argv[1])
    style: int = int(sys.argv[2])
    glyph_name: str | None = None if len(sys.argv) == 3 else sys.argv[3]

    # Get the list of glyphs to do
    glyphs_list_data: list[Composite_Glyph] = []
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
                    csv_line_splitted: list[str] = csv_line.strip().split(COMPOSITE_GLYPHS_LIST_DELIM)
                    components: list[str] = []
                    for c in csv_line_splitted[3:]:
                        if c != '':
                            components.append(c)
                    new_entry: Composite_Glyph = Composite_Glyph(
                        name=csv_line_splitted[0],
                        styles=int(csv_line_splitted[1]),
                        copy_anchor=not csv_line_splitted[2].lower() in ["", "0", "no"],
                        components=components
                    )
                    glyphs_list_data.append(new_entry)
                # -- Errors on the line
                elif csv_line_check == 1:
                    print(f"WARNING: Not enough parameters at line {line_number}, skipping.")
                elif csv_line_check == 2:
                    print(f"WARNING: 'Style' field isn't an integer at line {line_number}, skipping.")
                elif csv_line_check == 3:
                    print(f"WARNING: The glyph at line {line_number} contains itself as component, skipping.")
                # -- The style and eventually the glyph name don't match
                # ...do nothing
    
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
    if USE_MULTITHREADING:
        processes: list[Process] = [Process(target=build_single_glyph, args=(glyphs_list_data[i], ufo_dir, style, i, nb_glyphs)) for i in range(nb_glyphs)]
        # start all processes
        for process in processes:
            process.start()
        # wait for all processes to complete
        for process in processes:
            process.join()
    else:  # single thread (recommended for debug)
        for i, composite_glyph in enumerate(glyphs_list_data):
            build_single_glyph(composite_glyph, ufo_dir, style, i, nb_glyphs)

    # End message
    if glyph_name is None:
        print(f"Done with {sys.argv[1]} ({nb_glyphs} files changed)", flush=True)
    else:
        print(f"Done building {glyph_name} in {sys.argv[1]} ({nb_glyphs} files changed)", flush=True)
        
def build_single_glyph(glyph_data: Composite_Glyph, ufo_dir: Path, style: int, index: int, nb_glyphs: int) -> None:
    """
    Sub-process of main() supposed to work in parallel which read a line of glyph_list.
    Returns nothing.
    """

    sys.stdout.write('\033[2K\033[1G')
    print(f"[{index+1}/{nb_glyphs} ({int((index+1)/nb_glyphs*100)}%)] Working on {glyph_data.name}...", end="\r")
    
    build_composite_glyph(
        glyph_name=glyph_data.name,
        ufo_dir=ufo_dir,
        style=glyph_data.styles,
        copy_anchors=glyph_data.copy_anchor,
        components_list=glyph_data.components
    )

if __name__ == "__main__":
    main()

"""
Various useful functions to interact with ufo directories, and more especially the glyphs inside.

Note: All glyphs must be located to a folder called "glyphs" to work correctly.   
"""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

def get_glif_from_name(glyph_name: str, ufo_dir: Path) -> Path | None:
    """
    Reads the glyphs/contents.plist and retrive the path of the .glif file associated with the glyph
    with the name specified.
    Args:
        glyph_name: The name of the glyph
        ufo_dir: The ufo directory the glyph is from
    Returns:
        The name of the glyph, as str. Returns None if not found.
    """
    # open contents.plist
    tree: ET.ElementTree[ET.Element[str]] = ET.parse(ufo_dir / 'glyphs' / 'contents.plist')
    glyphs_dict: ET.Element[str] | None = tree.getroot().find("dict")
    if glyphs_dict is None:
        print('[WARNING] Couldn\' find <dict> in contents.plist')
        return None

    # find glyph_name
    key_list: list[ET.Element[str]] = glyphs_dict.findall("key")
    string_list: list[ET.Element[str]] = glyphs_dict.findall("string")
    index: int = 0
    glyph_found: bool = False
    while glyph_found == False and index < len(key_list):
        if key_list[index].text == glyph_name:
            glyph_found = True
        else:
            index += 1

    # return
    if glyph_found:
        return ufo_dir / 'glyphs' / str(string_list[index].text)
    else:
        print(f"{sys.argv[0]}: WARNING: Glyph not found: {glyph_name}")
        return None

def get_glyph_anchor_points(glyph_name: str, ufo_dir: Path) -> dict[str, tuple[int, int]]:
    """
    Find the anchors points from a .glif file. Returns an empty dict if the .glif is not found.
    Args:
        glyph_name: The name of the glyph
        ufo_dir: The ufo directory the glyph is from
    Returns:
        dict: All anchor points of a glyph, and for each anchor the coordinates (`int`) like this: `{"anchor_name_1": (x1, y1), "anchor_name_2": (x2, y2), ...}`
    """
    glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
    if glif is None:
        return {}
    xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif)
    xml_anchor_list: list[ET.Element[str]] = xml_tree.getroot().findall("anchor")
    anchor_dict: dict[str, tuple[int, int]] = {}
    for anchor in xml_anchor_list:
        anchor_dict[anchor.attrib["name"]] = (int(anchor.attrib["x"]), int(anchor.attrib["y"]))
    return anchor_dict

def get_glyph_metrics(glyph_name: str, ufo_dir: Path) -> dict[str, int]:
    """
    Returns a dict with some informations about the metrics of the glyph.
    Args:
        glyph_name: The name of the glyph
        ufo_dir: The ufo directory the glyph is from
    Returns:
        dict: A dict with the following format: `{"glyph_width": int, "left_kern": int,
        "right_kern": int, "raw_width": int, "raw_height": int, "x_min": int, "x_max": int",
        "y_min": int, "y_max": int}`
    """
    glyph_width: int = get_glyph_width(glyph_name, ufo_dir)
    points_list: list[tuple[int, int]] = get_glyph_points_coordinates(glyph_name, ufo_dir)
    if len(points_list) == 0:  # no points...
        return {
            "glyph_width": glyph_width,
            "left_kern": 0,
            "right_kern": glyph_width,
            "raw_width": 0,
            "raw_height": 0,
            "x_min": 0,
            "x_max": 0,
            "y_min": 0,
            "y_max": 0
        }
    else:
        x_points: list[int] = [ p[0] for p in points_list ]
        y_points: list[int] = [ p[1] for p in points_list ]
        return {
            "glyph_width": glyph_width,  # advance value
            "left_kern": min(x_points),
            "right_kern": glyph_width - max(x_points),
            "raw_width": abs(max(x_points) - min(x_points)),  # distance between x min and max
            "raw_height": abs(max(y_points) - min(y_points)),
            "x_min": min(x_points),
            "x_max": max(x_points),
            "y_min": min(y_points),
            "y_max": max(y_points),
        }

def get_glyph_points_coordinates(glyph_name: str, ufo_dir: Path) -> list[tuple[int, int]]:
    """
    Returns the list of all points in a glyph, rounded to `int`. If the glyphs include components, their points are also included, applying the correct offset.
    Args:
        glyph_name: The name of the glyph
        ufo_dir: The ufo directory the glyph is from
    Returns:
        list: list of tuples (int, int) with the coordinate of all points from all contours (`[(x1, y1), (x2, y2), ...]`)    
    """
    glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
    if glif is None:
        return []
    xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif)
    xml_outline: ET.Element[str] | None = xml_tree.getroot().find("outline")
    if xml_outline is None:
        print(f'[WARNING] Couldn\'t find <outline> in "{glif}"')
        return []
    points_list: list[tuple[int, int]] = []
    for element_index, element in enumerate(xml_outline):
        if element.tag == "contour":
            for point in element.findall("point"):
                if float(point.attrib["x"]) % 1 != 0.0 or float(point.attrib["y"]) % 1 != 0.0:
                    print(f'[WARNING] {glif}: non-integer coordinates at element {element_index}: ({point.attrib["x"]}, {point.attrib["y"]})')
                points_list.append((int(point.attrib["x"]), int(point.attrib["y"])))
        elif element.tag == "component":
            components_points_list: list[tuple[int, int]] = get_glyph_points_coordinates(element.attrib["base"], ufo_dir)
            x_offset: int = 0
            if "xOffset" in element.attrib:
                if float(element.attrib['xOffset']) % 1 != 0.0:
                    print(f'[WARNING] {glif}: non-integer x-offset at element {element_index}: {element.attrib['xOffset']}')
                x_offset = int(element.attrib["xOffset"])
            y_offset: int = 0
            if "yOffset" in element.attrib:
                if float(element.attrib['yOffset']) % 1 != 0.0:
                    print(f'[WARNING] {glif}: non-integer y-offset at element {element_index}: {element.attrib['yOffset']}')
                y_offset = int(element.attrib["yOffset"])
            for point in components_points_list:
                points_list.append((point[0] + x_offset, point[1] + y_offset))
    return points_list

def get_glyph_width(glyph_name: str, ufo_dir: Path) -> int:
    """
    Returns the glyph width (`int`) by reading the <advance> tag from its .glif file of the glyph specified.
    The value `0` is returned if the .glif is not found or doesn't have an <advance> tag.
    Args:
        glyph_name: The name of the glyph
        ufo_dir: The ufo directory the glyph is from
    Returns:
        int
    """
    glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
    if glif is None:
        return 0
    xml_tree = ET.parse(glif)
    xml_advance: ET.Element[str] | None = xml_tree.getroot().find("advance")
    if xml_advance is None:
        print(f'[WARNING] {glif}: <advance> tag not found.')
        return 0
    return int(xml_advance.attrib["width"])

def get_glyph_xml_points(glyph_name: str, ufo_dir: Path, x_offset: int = 0, y_offset: int = 0, x_scale: float = 1.0, y_scale: float = 1.0) -> list[list[ET.Element]]:
    """
    Returns a list of all points (as xml <point> node). If a component is found, their points is also returned, recursively.
    User shouldn't set x_offset, y_offset, x_scale and y_scale and keep them at their default values.
    Args:
        glyph_name: The name of the glyph
        ufo_dir: The ufo directory the glyph is from
        x_offset: (optional) Horizontal offset to apply on all points
        y_offset: (optional) Vertical offset to apply on all points
        x_scale: (optional) Horizontal scale to apply on all points (excluding offset)
        y_scale: (optional) Vertical scale to apply on all points (excluding offset)
    Returns:
        list: a list of all contours, and for each contours, the xml <point> nodes.
    """
    glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
    if glif is None:
        return []
    xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif)
    xml_outline: ET.Element[str] | None = xml_tree.getroot().find("outline")
    if xml_outline is None:
        print(f'[WARNING] {glif}: <outline> tag not found.')
    xml_contour_nodes: list[list[ET.Element[str]]] = []
    for element_index, element in enumerate(xml_outline if xml_outline is not None else []):
        if element.tag == "contour":
            xml_contour_points: list[ET.Element[str]] = element.findall("point")
            xml_contour_points_with_offset: list[ET.Element[str]] = []
            for point_index, point in enumerate(xml_contour_points):
                if float(point.attrib["x"]) % 1 != 0.0 or float(point.attrib["y"]) % 1 != 0.0:
                    print(f'[WARNING] {glif}: non-integer coordinates at element {element_index}, point {point_index}: ({point.attrib["x"]}, {point.attrib["y"]})')
                point.attrib["x"] = str(int(float(point.attrib["x"]) * x_scale) + x_offset)
                point.attrib["y"] = str(int(float(point.attrib["y"]) * y_scale) + y_offset)
                xml_contour_points_with_offset.append(point)
            xml_contour_nodes.append(xml_contour_points_with_offset)
        elif element.tag == "component":
            # calculate offset
            component_x_offset: int = 0
            if "xOffset" in element.attrib:
                if float(element.attrib['yOffset']) % 1 != 0.0:
                    print(f'[WARNING] {glif}: non-integer x-offset at element {element_index}: {element.attrib['xOffset']}')
                component_x_offset = int(element.attrib["xOffset"])
            component_y_offset: int = 0
            if "yOffset" in element.attrib:
                if float(element.attrib['yOffset']) % 1 != 0.0:
                    print(f'[WARNING] {glif}: non-integer y-offset at element {element_index}: {element.attrib['yOffset']}')
                component_y_offset = int(element.attrib["yOffset"])
            # Missing scale calculation?
            xml_contour_nodes += get_glyph_xml_points(element.attrib["base"], ufo_dir, component_x_offset, component_y_offset)
    return xml_contour_nodes

def get_kerning(glyph_first: str, glyph_second: str, ufo_dir: Path):
    """
    Returns the kerning between 2 glyphs by reading the `feature.fea` file.
    Requires a `kern` feature to be defined and containing a kerning lookup. Within the kerning
    lookup, the classes should be defined first (before the `pos` values).
    Args:
        glyph_first: Name of the first glyph
        glyph_second: Name of the second glyph
        ufo_dir: .ufo file to look at.
    Note: 
        Given how this is implemented right now, the script and language aren't checked, and
        thus, only the first lookup table found in the `feature kern` block is used.
    Returns:
        int
    """
    # Maybe code would look less awful if using fonttools lib?

    features_filename = ufo_dir / 'features.fea'

    # Find the table
    table_name: str | None = None
    table_found: bool = False
    with open(features_filename, "r") as features_file:
        # find the name of the kern table
        line: str = features_file.readline()
        while line:
            if "feature kern" in line:  # feature found
                while line and not("}" in line) and table_name is None:
                    line = features_file.readline()
                    if "lookup" in line:
                        table_name = line.strip().replace(";", "").split(" ")[1]
                if table_name is None:
                    print("[WARNING] No lookup table found in feature kern block")
                    return 0
            line = features_file.readline()
        if table_name is None:
            print("[WARNING] No feature kern block found")
            return 0

        # find the kern table
        features_file.seek(0)  # go back to the beginning
        line = features_file.readline()
        while line and not(table_found):
            if f"lookup {table_name}" in line:
                table_found = True
            else:
                line = features_file.readline()

        if not(table_found):
            print(f"[WARNING] Kern table '{table_name}' not found.")
            return 0

        # find the classes of the 2 glyphs and the kern
        line = features_file.readline()  # pointing "lookupflag 0;"
        line = features_file.readline()  # pointing towards the first class definition
        glyph_first_classes: list[str] = []
        glyph_second_classes: list[str] = []
        while line and not("}" in line):
            if line.strip().split(" ")[0] == "pos":  # pos value
                # example: "pos @kc82_first_1 @kc82_second_3 -70;"
                class_first: str = line.strip().split(" ")[1]
                class_second: str = line.strip().split(" ")[2]
                kern_value: int = int(line.strip().split(" ")[3].replace(";", ""))
                if (class_first in glyph_first_classes) and (class_second in glyph_second_classes):
                    return kern_value
                else:
                    line = features_file.readline()  # next line
            elif "=" in line:  # new class
                # first line
                current_class: str = line.strip().split(" ")[0]
                glyph_list: str = line.strip().split("=")[1]
                if (f"\\{glyph_first}" in glyph_list) or (f" {glyph_first}" in glyph_list) or (f"{glyph_first} " in glyph_list):
                    glyph_first_classes.append(current_class)
                if (f"\\{glyph_second}" in glyph_list) or (f" {glyph_second}" in glyph_list) or (f"{glyph_second} " in glyph_list):
                    glyph_second_classes.append(current_class)
                while not(";" in line):
                    line = features_file.readline()
                    if (f"\\{glyph_first}" in glyph_list) or (f" {glyph_first}" in glyph_list) or (f"{glyph_first} " in glyph_list):
                        glyph_first_classes.append(current_class)
                    if (f"\\{glyph_second}" in glyph_list) or (f" {glyph_second}" in glyph_list) or (f"{glyph_second} " in glyph_list):
                        glyph_second_classes.append(current_class)
                line = features_file.readline()  # next line

        return 0  # no kerning

def move_glyph(glyph_name: str, ufo_dir: Path, x: int, y: int, move_points: bool = True, move_anchors: bool = True, move_width: bool = False) -> int:
    """
    Translation transform a glyph and round all points to `int`. Edits the related .glif name from the .ufo file.
    Args:
        glyph_name: The name of the glyph where to apply the transformation
        ufo_dir: The ufo directory the glyph is from
        x: How many units to move the glyphs horizontally (positive number = to the right)
        y: How many units to move the glyphs vertically (positive number = to the top)
        move_points: (optional) Move all points from the glyph. Default value: `True`.
        move_anchors: (optional) Move the anchors points. Default value: `True`.
        move_width: (optional) Increases the glyph's width by `x`. Default value: `False`.
    Returns:
        `0` if success, non-zero otherwise.
    """
    glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
    if glif is None:
        return 1
    xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif)
    xml_root: ET.Element[str] = xml_tree.getroot()
    for element_index, element in enumerate(xml_root.findall("./*")):
        if element.tag == "advance" and move_width:
            if float(element.attrib["width"]) % 1 != 0.0:
                print(f'[WARNING] {glif}: non-integer advance value: {element.attrib["width"]})')
            element.attrib["width"] = str(int(element.attrib["width"]) + x)
        elif element.tag == "anchor" and move_anchors:
            if float(element.attrib["x"]) % 1 != 0.0 or float(element.attrib["y"]) % 1 != 0.0:
                print(f'[WARNING] {glif}: non-integer coordinates at anchor index {element_index}: ({element.attrib["x"]}, {element.attrib["y"]})')
            element.attrib["x"] = str(int(element.attrib["x"]) + x)
            element.attrib["y"] = str(int(element.attrib["y"]) + y)
        elif element.tag == "outline" and move_points:
            for outline_number, outline_element in enumerate(element.findall("./*")):
                if outline_element.tag == "contour":
                    for contour_element in outline_element.findall("./*"):
                        if contour_element.tag == "point":
                            if float(contour_element.attrib["x"]) % 1 != 0.0 or float(contour_element.attrib["y"]) % 1 != 0.0:
                                print(f'[WARNING] {glif}: non-integer coordinates at outline index {element_index} outline {outline_number} : ({contour_element.attrib["x"]}, {contour_element.attrib["y"]})')
                            contour_element.attrib["x"] = str(int(contour_element.attrib["x"]) + x)
                            contour_element.attrib["y"] = str(int(contour_element.attrib["y"]) + y)
                elif outline_element.tag == "component":
                    if "xOffset" in outline_element.attrib:
                        if float(outline_element.attrib['xOffset']) % 1 != 0.0:
                            print(f'[WARNING] {glif}: non-integer x-offset at component index {element_index}: {outline_element.attrib['xOffset']}')
                        outline_element.attrib["xOffset"] = str(int(outline_element.attrib["xOffset"]) + x)
                    else:
                        outline_element.attrib["xOffset"] = str(x)
                    if "yOffset" in outline_element.attrib:
                        if float(outline_element.attrib['yOffset']) % 1 != 0.0:
                            print(f'[WARNING] {glif}: non-integer y-offset at component index {element_index}: {outline_element.attrib['yOffset']}')
                        outline_element.attrib["yOffset"] = str(int(outline_element.attrib["yOffset"]) + y)
                    else:
                        outline_element.attrib["yOffset"] = str(y)
        # ignore other type of elements, keep them as is
    
    # Save
    try:
        xml_tree.write(glif, encoding="UTF-8", xml_declaration=True)
    except Exception as err:
        print(f'[ERROR] Failed to save {glif}: {err}')
        return 1
    return 0

def unlink_references(glyph_name: str, ufo_dir: Path) -> int:
    """
    Replaces all components of a glyph (references towards other glyphs) by points. Changes UFO file.
    Args:
        glyph_name: The name of the glyph where to apply the transformation
        ufo_dir: The ufo directory the glyph is from
    Returns:
        `0` if success, non-zero otherwise.
    """
    # Load file to edit
    glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
    if glif is None:
        return 1
    xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif)
    xml_root: ET.Element[str] = xml_tree.getroot()
    xml_outline: ET.Element[str] | None = xml_root.find("outline")
    if xml_outline is None:
        print(f'[ERROR] <outline> not found.')
        return 1

    # Find all <components> node
    components_nodes: list[ET.Element[str]] = xml_outline.findall("component")

    # Get points from components_nodes
    xml_contours_list: list[list[ET.Element[str]]] = []
    for component in components_nodes:
        x_offset: int = 0
        y_offset: int = 0
        x_scale: float = 1.0
        y_scale: float = 1.0
        if "xOffset" in component.attrib:
            x_offset = int(float(component.attrib["xOffset"]))
        if "yOffset" in component.attrib:
            y_offset = int(float(component.attrib["yOffset"]))
        if "xScale" in component.attrib:
            x_scale = float(component.attrib["xScale"])
        if "yScale" in component.attrib:
            y_scale = float(component.attrib["yScale"])
        xml_contours_list += get_glyph_xml_points(component.attrib["base"], ufo_dir, x_offset, y_offset, x_scale, y_scale)

    # Delete components nodes
    for node in xml_outline.findall("component"):
        xml_outline.remove(node)

    # Inject the new contours
    for contour in xml_contours_list:
        new_node: ET.Element[str] = ET.SubElement(xml_outline, "contour", {})
        for point in contour:
            ET.SubElement(new_node, point.tag, point.attrib)

    # Save
    try:
        xml_tree.write(glif, encoding="UTF-8", xml_declaration=True)
    except Exception as err:
        print(f'[ERROR] Failed to save {glif}: {err}')
        return 1
    return 0


from abc import abstractmethod
import argparse
from concurrent.futures import ProcessPoolExecutor
from logger import configure_logging
import os
from pathlib import Path
from ufo_utils import get_glif_from_name, get_glyph_anchor_points, get_glyph_metrics, get_kerning, move_glyph
import xml.etree.ElementTree as ET

# How many process to run at most for parallelizable tasks (excluding gftools)
PROCESSES_COUNT: int = int(os.environ.get('PROCESSES_COUNT', '1'))

logger = configure_logging()

class Composed_Glyph():
    def __init__(self, name: str, styles: int, glyphs: list[str]):
        self.name = name
        self.styles = styles
        self.glyphs = glyphs
        self.priority = 0  # set manually when building glyphs

    @abstractmethod
    def generate_glif(self, ufo_dir: Path) -> int:
        '''
            Generate the .glif file related to this object. Writes inside the given UFO.
            Args:
                ufo_dir: UFO project to write.
            Returns:
                `0` if success, non-zero if an error occured.
        '''
        pass

class Accented_Glyph(Composed_Glyph):
    
    def __init__(self, name: str, styles: int, allow_left_overflow: bool, allow_right_overflow: bool, glyphs: list[str]):
        super().__init__(name, styles, glyphs)
        self.allow_left_overflow = allow_left_overflow
        self.allow_right_overflow = allow_right_overflow

    def generate_glif(self, ufo_dir: Path) -> int:
        # under special conditions replaces mkmk_top_center
        MKMK_ANCHORS_REPLACE = {
            "mkmk_top_center": "top_center",
            "mkmk_bottom_center": "bottom_center",
            "mkmk_greek_top_center": "top_center" 
        }

        # Self reference check
        if self.name in self.glyphs:
            logger.error(f'Failed to generate "{self.name}": the glyph is composed of itself.')
            return 1

        glif_filename: Path | None = get_glif_from_name(self.name, ufo_dir)
        if glif_filename is None:
            return 1
        xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif_filename)
        xml_root: ET.Element[str] = xml_tree.getroot()
        xml_advance: ET.Element[str] | None = xml_root.find("advance")
        if xml_advance is None:
            logger.error(f'<advance> not found in "{glif_filename}"')
            return 1

        # Place components and anchors and get metrics of the base (when recalculate kerning)
        glyph_component: dict[str, tuple[int, int]] = {}  # {"component": (xOffset, yOffset)}
        glyph_anchors  : dict[str, tuple[int, int]] = {}  # {"anchor_name": (x, y)}
        base_metrics   : dict[str, int]             = {}  # set by get_glyph_metrics()
        for i in range(len(self.glyphs)):
            # Load anchor points
            new_component_anchors: dict[str, tuple[int, int]] = get_glyph_anchor_points(self.glyphs[i], ufo_dir)
            glyph_anchors_keys: list[str]  # used several times in this function

            # Place component (and update glyph width on base)
            x_offset = 0
            y_offset = 0
            if i == 0:  # find the offset of the new component (ignore the step below for the base)
                glyph_component[self.glyphs[i]] = (0, 0)
                base_metrics = get_glyph_metrics(self.glyphs[i], ufo_dir)
                xml_advance.attrib["width"] = str(base_metrics["glyph_width"])
            else:
                # Find a matching anchor
                placed_component: bool = False
                glyph_anchors_keys = list(glyph_anchors.keys())  # have a list of all keys of the dicts
                new_component_anchors_keys: list[str] = list(new_component_anchors.keys())
                ib: int = 0
                while (not placed_component) and ib < len(glyph_anchors_keys):  # from the glyph we are building
                    base_anchor = glyph_anchors_keys[ib]
                    im: int = 0
                    while (not placed_component) and im < len(new_component_anchors_keys):  # from the component we're adding
                        mark_anchor: str = new_component_anchors_keys[im]
                        if (not placed_component) and ("_" + base_anchor) == mark_anchor:  # found matching base/mark
                            x_offset: int = glyph_anchors[base_anchor][0] - new_component_anchors[mark_anchor][0]
                            y_offset: int = glyph_anchors[base_anchor][1] - new_component_anchors[mark_anchor][1]
                            glyph_component[self.glyphs[i]] = (x_offset, y_offset)
                            glyph_anchors.pop(base_anchor)  # remove the 2 anchors from the anchor list
                            new_component_anchors.pop(mark_anchor)
                            glyph_anchors_keys = list(glyph_anchors.keys())  # update these too
                            new_component_anchors_keys = list(new_component_anchors.keys())
                            placed_component = True
                        else:
                            im += 1
                    ib += 1
                if not placed_component:  # Anchor not found: apply no offset (shouldn't happen)
                    logger.warning(f'Couldn\'t find where to attach {self.glyphs[i]} on {self.name}')
                    glyph_component[self.glyphs[i]] = (0, 0)

            # Save anchor on the dict glyph_anchors
            for new_anchor in new_component_anchors:
                x: int = new_component_anchors[new_anchor][0] + x_offset
                y: int = new_component_anchors[new_anchor][1] + y_offset
                glyph_anchors[new_anchor] = (x, y)  # replace if already here

        # Create a list with the name of all anchors
        glyph_anchors_keys = list(glyph_anchors.keys())

        # greek_* anchors : either we keep all of them or remove them all (greek_kt, greek_t, greek_k, greek_v)
        greek_anchors_count: int = 0
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
        i: int = 0
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
        xml_outline: ET.Element[str] | None = xml_root.find("outline")
        if xml_outline is not None:
            xml_root.remove(xml_outline)  # empty the componenets inside <outline>
        xml_outline = ET.SubElement(xml_root, "outline")
        for component in glyph_component:
            if glyph_component[component][0] == 0 and glyph_component[component][1] == 0:
                ET.SubElement(xml_outline, "component", {"base": component})
            else:
                ET.SubElement(xml_outline, "component", {"base": component, "xOffset": str(glyph_component[component][0]), "yOffset": str(glyph_component[component][1])})

        # Save the file
        try:
            xml_tree.write(glif_filename, encoding='utf-8', xml_declaration=True)
        except Exception as err:
            logger.error(f'Failed to write into "{glif_filename}": {err}')
            return 1

        # Update kern if needed
        current_glyph_metrics: dict[str, int] = get_glyph_metrics(self.name, ufo_dir)
        if (not self.allow_right_overflow) and current_glyph_metrics["x_max"] > base_metrics["glyph_width"]:
            move_glyph(self.name, ufo_dir, current_glyph_metrics["x_max"] - base_metrics["glyph_width"], 0, False, False, True)
        if (not self.allow_left_overflow) and current_glyph_metrics["x_min"] < 0:
            move_glyph(self.name, ufo_dir, abs(current_glyph_metrics["x_min"]), 0, True, True, not self.allow_right_overflow)

        logger.debug(f"Done buliding {self.name} ({len(glyph_component)} components, {len(glyph_anchors)} anchors)")
        return 0

class Composite_Glyph(Composed_Glyph):
    def __init__(self, name: str, styles: int, copy_anchors: bool, glyphs: list[str]):
        super().__init__(name, styles, glyphs)
        self.copy_anchors = copy_anchors

    def _copy_single_glyph(self, glyph_src: str,
                                 glyph_dst: str,
                                 ufo_dir: Path,
                                 copy_anchors: bool = True,
                                 replace_all: bool = True,
                                 x_offset: int = 0,
                                 y_offset: int = 0) -> int:
        """
            Copy `glyph_src` into `glyph_dst`, without changing its name not Unicode value.
            Can also copy anchors with `copy_anchors` set to `True`.

            Changes UFO .glif file of destination glyph.

            Returns `0` if success, non-zero otherwise.
        """
        # get source anchors and outline
        src_glif: Path | None = get_glif_from_name(glyph_src, ufo_dir)
        if src_glif is None:
            return 1
        src_xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(src_glif)
        src_xml_root: ET.Element[str] = src_xml_tree.getroot()
        src_anchor_list: list[ET.Element[str]] = src_xml_root.findall("anchor") if copy_anchors else []

        # Parse destination glyph XML
        dst_glif: Path | None = get_glif_from_name(glyph_dst, ufo_dir)
        if dst_glif is None:
            return 1
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
            logger.error(f'Somehow couldn\'t find <outline> when copying {glyph_src} into {glyph_dst}')
            return 1
        ET.SubElement(dst_xml_outline, "component", new_component_attrib)

        # Save
        dst_xml_tree.write(dst_glif, encoding='utf-8', xml_declaration=True)
        return 0

    def generate_glif(self, ufo_dir: Path) -> int:
        # Self reference check
        if self.name in self.glyphs:
            logger.error(f'Failed to generate "{self.name}": the glyph is composed of itself.')
            return 1

        # Place components
        x_cursor: int = 0
        for component_number in range(0, len(self.glyphs), 1):
            component_name: str = self.glyphs[component_number]
            self._copy_single_glyph(component_name, self.name, ufo_dir, self.copy_anchors, component_number==0, x_cursor, 0)
            x_cursor += get_glyph_metrics(component_name, ufo_dir)["glyph_width"]
            if (component_number + 1) < len(self.glyphs):  # apply kern with the next element
                x_cursor += get_kerning(self.glyphs[component_number], self.glyphs[component_number+1], ufo_dir)
        
        # Update the advance value
        glif_filename: Path | None = get_glif_from_name(self.name, ufo_dir)
        if glif_filename is None:
            return 1
        xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif_filename)
        xml_advance: ET.Element[str] | None = xml_tree.getroot().find("advance")
        if xml_advance is None:
            logger.error(f'<advance> not found in "{glif_filename}"')
            return 1
        xml_advance.attrib["width"] = str(x_cursor)
        # Save the file
        try:
            xml_tree.write(glif_filename, encoding='utf-8', xml_declaration=True)
        except Exception as err:
            logger.error(f'Failed to write into "{glif_filename}": {err}')
            return 1
        logger.debug(f"Done buliding {self.name} ({len(self.glyphs)} components)")
        return 0

class Glyph_Tree():
    def __init__(self, glyph_name: str, children: list['Glyph_Tree']):
        self.glyph_name = glyph_name
        self.children = children

    def __repr__(self) -> str:
        output: str = f'(\'{self.glyph_name}\', ['
        for i, child in enumerate(self.children):
            if i > 0:
                output += ', '
            output += child.__repr__()
        output += '])'
        return output

    def __str__(self) -> str:
        return self.__repr__()

    def print(self):
        '''Show ASCII schema of the tree on the terminal.'''

        def _print_loop(node: Glyph_Tree, prefix: str = "", is_last: bool = True):
            # 1. Print the current node with its appropriate connector
            if prefix == "":
                # Root node doesn't need a connector
                print(node.glyph_name)
            else:
                connector = "└── " if is_last else "├── "
                print(f"{prefix}{connector}{node.glyph_name}")
            
            # 2. Update the prefix for the children
            # If this node is the last child of its parent, its vertical line ends here ("    ")
            # Otherwise, the vertical line continues down ("│   ")
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            # 3. Recursively print all children
            child_count = len(node.children)
            for i, child in enumerate(node.children):
                is_child_last = (i == child_count - 1)
                _print_loop(child, new_prefix, is_child_last)

        _print_loop(self)

# === INTERNAL FUNCTIONS ===

def _is_composed(name: str, cg_list: list[Composed_Glyph]) -> bool:
    '''Check if the glyph is made of other glyphs.'''
    return name in [cg.name for cg in cg_list]

def _get_children_from_name(name: str, cg_list: list[Composed_Glyph]) -> list[str]:
    '''Returns the list of glyphs to build the glyph with the given name.'''
    for cg in cg_list:
        if cg.name == name:
            return cg.glyphs
    return []

def _get_tree_parents(glyph_name: str, tree: Glyph_Tree) -> list[str]:
    '''Returns a list of parents of the glyph with the given name. Last element is the glyph itself. Returns empty list if not found.'''
    if tree.glyph_name == glyph_name:
        return [glyph_name]
    
    for child in tree.children:
        child_path = _get_tree_parents(glyph_name, child)
        if child_path:
            return [tree.glyph_name] + child_path
            
    return []

def _get_subtree(name: str, tree: Glyph_Tree) -> Glyph_Tree | None:
    if name == tree.glyph_name:
        return tree
    for child in tree.children:
        subtree = _get_subtree(name, child)
        if subtree is not None:
            return subtree
    return None

def _build_tree_from_glyph(name: str, cg_list: list[Composed_Glyph], path: list[str] = []) -> Glyph_Tree | None:
    '''Build glyph tree for a single glyph. Returns None if an error was detected.'''
    if name in _get_children_from_name(name, cg_list):  # Self-reference check
        logger.error(f'Failed to get dependencies of "{name}": the glyph is composed of itself.')
        return None

    if name in path:  # Circular reference check using the current path trace
        # Extract the loop portion from the path for the error message
        cycle_start_idx = path.index(name)
        cycle_path = path[cycle_start_idx:] + [name]

        error_msg = f'Failed to get dependencies of "{name}" circular reference '
        error_msg += " -> ".join(f'"{p}"' for p in cycle_path)
        logger.error(error_msg)
        return None

    if not _is_composed(name, cg_list):  # Leaf node (base case)
        return Glyph_Tree(name, [])

    # Recursive step
    name_tree = Glyph_Tree(name, [])
    extended_path = path + [name]   # Add current node to the path before diving into children
    for child in _get_children_from_name(name, cg_list):
        # Pass the extended path down to children
        subtree = _build_tree_from_glyph(child, cg_list, extended_path)
        if subtree is None:  
            return None  # Propagate failure upwards
        name_tree.children.append(subtree)

    return name_tree

def _build_tree_from_list(cg_list: list[Composed_Glyph]) -> Glyph_Tree | None:
    """
    Takes a list of Composed_Glyph objects and structures them into a Glyph_Tree.
    Ensures every Composed_Glyph definition is instantiated exactly once as a parent node.
    """
    # 1. Map each composed glyph name to its object for quick lookup
    cg_map: dict[str, Composed_Glyph] = {cg.name: cg for cg in cg_list}
    
    # 2. Track which composed glyphs have already been processed into the tree
    processed_composed: set[str] = set()

    def build_node(name: str, path: list[str]) -> Glyph_Tree | None:
        # Check self-reference
        if name in _get_children_from_name(name, cg_list):
            logger.error(f'Failed to get dependencies of "{name}": the glyph is composed of itself.')
            return None

        # Check circular dependency using the path trace
        if name in path:
            cycle_start_idx = path.index(name)
            cycle_path = path[cycle_start_idx:] + [name]
            error_msg = f'Failed to get dependencies of "{name}" circular reference '
            error_msg += " -> ".join(f'"{p}"' for p in cycle_path)
            logger.error(error_msg)
            return None

        # Base case: If it's a leaf node (not a composed glyph definition)
        if name not in cg_map:
            return Glyph_Tree(name, [])

        # If it is a composed glyph but we already generated its definitive structural node,
        # treat it as a leaf reference here to avoid duplicating the sub-graph elements.
        if name in processed_composed:
            return Glyph_Tree(name, [])

        # Mark this composed glyph as processed
        processed_composed.add(name)

        # Recursive step for new structural nodes
        node = Glyph_Tree(name, [])
        extended_path = path + [name]
        
        for child_name in cg_map[name].glyphs:
            subtree = build_node(child_name, extended_path)
            if subtree is None:
                return None  # Propagate error upward
            node.children.append(subtree)

        return node

    # Create the top-level master root container
    root_tree: Glyph_Tree = Glyph_Tree("", [])

    # 3. First pass: Find natural root nodes (glyphs not used as components inside any other glyph)
    all_components: set[str] = set(child for cg in cg_list for child in cg.glyphs)
    natural_roots: list[str] = [cg.name for cg in cg_list if cg.name not in all_components]

    # Process natural roots first
    for root_name in natural_roots:
        subtree = build_node(root_name, [])
        if subtree:
            root_tree.children.append(subtree)

    # 4. Second pass: Pick up any orphaned loops or disconnected components 
    # ensuring every Composed_Glyph in cg_list appears exactly once in the tree structure.
    for cg in cg_list:
        if cg.name not in processed_composed:
            subtree = build_node(cg.name, [])
            if subtree:
                root_tree.children.append(subtree)

    return root_tree

def _set_glyph_priorities_from_list(cg_list: list[Composed_Glyph]) -> list[Composed_Glyph]:
    '''
        Compute the priority attributes of a list of composed glyph by building a tree.
        Higher priority value should be built first. Lowest priority is 1.

        Every `Composed_Glyphs` should have an unique glyph name (NOTE: this function doesn't check this).
    
        Returns a NEW list if success ; returns empty list if there's an issue with the tree.
    '''

    new_cg_list: list[Composed_Glyph] = cg_list.copy()
    for i, _ in enumerate(new_cg_list):
        new_cg_list[i].priority = 0

    cg_map: dict[str, int] = {cg.name: i for i, cg in enumerate(new_cg_list)}  # name -> index in new_cg_list 

    # Get tree
    cg_tree: Glyph_Tree | None = _build_tree_from_list(new_cg_list)
    if cg_tree is None:
        return []
    
    # Set priorities attributes
    def _read_node(tree: Glyph_Tree, depth: int = 0) -> None:
        if tree.glyph_name != '' and tree.glyph_name in cg_map.keys():
            new_cg_list[cg_map[tree.glyph_name]].priority = max(new_cg_list[cg_map[tree.glyph_name]].priority, depth)
        for child in tree.children:
            _read_node(child, depth + 1)

    _read_node(cg_tree)
    
    # Sort by priority
    new_cg_list.sort(key=lambda cg: cg.priority, reverse=True)
    logger.debug(f'Build order and priority: {[(cg.name, cg.priority) for cg in new_cg_list]}')
    return new_cg_list

# === PUBLIC FUNCTIONS ===

def parse_composed_glyph_csv_line(line: str, index: int | None = None) -> Composed_Glyph | None:
    '''
        Converts a string with value separated by commas into a `Composed_Glyph` object (`Accented_Glyph` or `Composite_Glyph`).
        
        A line should look like this: `Name,Styles,Category,Param_1,Param_2,Glyph_1,Glyph_2,Glyph_3,Glyph_4,...`
        * `Name`: name of the composed glyph (`str`)
        * `Styles`: styles where this line applies. `1` = normal ; `2` = italic ; `3` = both
        * `Category`: how the glyph `Name` should be build. `A`: accented ; `C`: composite
        * `Param_x`: depends of the `Category`:
                * `A`: `Param_1` = allow left overflow ; `Param_2` = allow right overflow (if an accent would go out of `Glyph_1` limits horizontaly)
                * `C`: `Param_1` = copy anchors
        * `Glyph_x`: glyphs that compose the glyph `Name`, in order.

        Note:
            For `Category`, only the first char is read (case insensitive).
        Args:
            line: the line to read
            index: (optional) line number to show on error messages.
        Returns:
            `Accented_Glyph` or `Composite_Glyph` depending of the `Category` field.
    '''

    def log_fail(msg: str, index: int | None):
        '''Logging when returning None because of invalid value.'''
        if index is None:
            logger.warning(f'Failed to parse line "{line}": {msg}')
        else:
            logger.warning(f'Failed to parse line {index}: {msg}')

    data: list[str] = line.split(',')

    if len(data) < 6:  # Check column count
        log_fail('Not enough columns.', index)
        return None

    # Value check (params check columns 3 and 4 are done in their respective class)
    if not data[1].isnumeric():
        log_fail(f'Invalid style value: "{data[1]}" is not a number.', index)
        return None

    name: str = data[0]
    styles: int = int(data[1])
    category: str = data[2].upper()[0:]
    glyphs: list[str] = [g for g in data[5:] if len(g) >= 1]

    if category == 'A':  # Accented glyphs
        if not data[3].isnumeric():
            log_fail(f'Invalid param value at column [3]: "{data[3]}" is not a number', index)
            return None
        if not data[4].isnumeric():
            log_fail(f'Invalid param value at column [4]: "{data[4]}" is not a number', index)
            return None
        left_overflow: bool = bool(int(data[3]))
        right_overflow: bool = bool(int(data[4]))
        return Accented_Glyph(name, styles, left_overflow, right_overflow, glyphs)
    
    if category == 'C':  # Composite glyph
        if not data[3].isnumeric():
            log_fail(f'Invalid param value at column [3]: "{data[3]}" is not a number', index)
            return None
        copy_anchors: bool = bool(int(data[3]))
        return Composite_Glyph(name, styles, copy_anchors, glyphs)

    # Unknown category
    log_fail(f'Invalid category at column [2]: "{data[3]}" is not a number', index)
    return None




def parse_composed_glyph_csv(csv_file: Path, styles: int, first_line_number: int = 1) -> list[Composed_Glyph]:
    '''
        Read an entire CSV file describing composed glyphs (see `parse_composed_glyph_csv_line()`).
        This function handles logging. 

        Args:
            csv_file: path to the csv file to read
            styles: `1` = normal, `2` = italic, `3` = both
            first_line_number: first line number to read in the CSV. First line in the file is 1!
        Return:
            list[Composed_Glyph]. Invalid or duplicates lines are ignored. 
        Note:
            This function does not check circular references or duplicates.
    '''
    cg_list: list[Composed_Glyph] = []
    cg_list_names: dict[str, int] = {}  # maps glyphs with their line number in CSV
    with open(csv_file, 'r') as f:
        for line_number, line in enumerate(f.readlines(), start=1):
            if line_number >= first_line_number:
                cg: Composed_Glyph | None = parse_composed_glyph_csv_line(line.strip(), line_number + 1)
                if cg is None:  # invalid line -> parse_composed_glyph_csv_line prints warning message
                    pass 
                elif not cg.styles & styles:  # style check
                    pass  # nothing to do, skip the line
                elif cg.name in cg_list_names.keys():  # duplicate glyph check
                    logger.warning(f'"{csv_file}": line {line_number} will be ignored, "{cg.name}" is already defined at line {cg_list_names[cg.name]}')
                else:  # all good :)
                    cg_list.append(cg)
                    cg_list_names[cg.name] = line_number
    logger.debug(f'Parsed {len(cg_list)} composed glyphs from "{csv_file}".')
    return cg_list

def _build_composed_glyph_from_csv_worker(cg: Composed_Glyph, ufo_dir: Path) -> int:
    '''Subfunction of `build_composed_glyph_from_csv()`'''
    return cg.generate_glif(ufo_dir)

def build_composed_glyph_from_csv(csv_file: Path, ufo_dir: Path, styles: int, processes_count: int = 1) -> int:
    '''
        Builds composed glyphs (.glif) from a CSV definition inside an UFO directory. Overwrites existing .glif files.

        This function parses a CSV file containing composed glyph definitions, assigns priority 
        levels to the glyphs based on their tree structure, and iterates through each priority 
        level to generate individual `.glif` files within the specified output directory (`ufo_dir`).

        It supports multiprocessing (using `ProcessPoolExecutor`) when requested via `processes_count`.

        Args:
            csv_file: Path to the CSV file containing composed glyph definitions.
            ufo_dir: The base directory where the resulting `.glif` files (UFO components) will be written.
            styles: `1` = non-italic, `2` = italic
            processes_count: Number of worker processes to use for generation. If 1, sequential execution is used.

        Returns:
            int: `0` if no error, `-1` if invalid input has been detected.
            An error count representing the number of glyphs that failed to generate successfully.
    '''
    logger.info(f'Working on "{ufo_dir}"...')

    # Styles value check
    if styles <= 0:
        logger.error(f'Invalid value for "styles": {styles}')
        return -1
    
    # Read CSV
    cg_list: list[Composed_Glyph] = parse_composed_glyph_csv(csv_file, styles, 2)  # priority is 0 by default
    if len(cg_list) == 0:
        logger.info('No glyph has been generated, nothing to build.')
        return 0


    # Set priorities by building tree
    cg_list = _set_glyph_priorities_from_list(cg_list)
    total_glyphs: int = len(cg_list)
    if len(cg_list) == 0:
        logger.warning('No glyph has been generated.')
        return -1
    
    max_priority: int = cg_list[0].priority
    logger.info(f'Found {total_glyphs} glyphs inside "{csv_file}".')
    error_count: int = 0
    for priority in reversed(range(max_priority + 1)):
        cg_with_priority: list[Composed_Glyph] = [cg for cg in cg_list if cg.priority == priority]
        logger.verbose(f'Building {len(cg_with_priority)} glyphs with priority {priority}')  # pyright: ignore[reportUnknownMemberType]
        if processes_count > 1:
            logger.verbose(f'Using multiprocessing ({processes_count} processes)')  # pyright: ignore[reportUnknownMemberType]
            

            with ProcessPoolExecutor(max_workers=processes_count) as executor:
                futures = [executor.submit(_build_composed_glyph_from_csv_worker, cg, ufo_dir) for cg in cg_list]
                for future in futures:
                    error_count += future.result()
        else:
            logger.verbose('Using a single process.')  # pyright: ignore[reportUnknownMemberType]
            for cg in cg_with_priority:
                if cg.generate_glif(ufo_dir) != 0:
                    error_count += 1

    if error_count >= total_glyphs:
        logger.error(f'Failed to generate every of the {total_glyphs} glyphs.')
    else:
        logger.success(f'Sucessfully generated {total_glyphs - error_count} / {total_glyphs} glyphs into "{ufo_dir}"')  # pyright: ignore[reportUnknownMemberType]
        if error_count > 0:
            logger.warning(f'Failed to generate {error_count} glyphs.')

    logger.warning(f'PLEASE OPEN AND SAVE "{ufo_dir}" WITH FONTFORGE TO COMPLETE THE PROCESS!!!' )

    return error_count


if __name__ == '__main__':

    # Read input args
    parser = argparse.ArgumentParser(description='Generate .glif files from a CSV config.')
    parser.add_argument('csv_config', type=str, help='List of glyphs as CSV file.')
    parser.add_argument('ufo_dir', type=str, help='UFO dir to write.')
    parser.add_argument('style', type=int, help='1 = non-italic ; 2 = italic', choices=[1, 2])

    # Check args values
    try:
        args = parser.parse_args()
    except Exception as err:
        logger.error(err)
        print(parser.print_help())
        exit(1)
    if not Path(args.csv_config).exists():
        logger.error(f'CSV config not found: "{args.csv_config}"')
        exit(1)
    if not Path(args.ufo_dir).exists():
        logger.error(f'UFO not found: "{args.ufo_dir}"')
        exit(1)

    # Run
    exit_code: int = build_composed_glyph_from_csv(Path(args.csv_config), Path(args.ufo_dir), args.style, PROCESSES_COUNT)
    exit(1 if exit_code == -1 else 0)

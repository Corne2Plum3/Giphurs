from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
from pathlib import Path
import sys
from ufo_utils import get_glif_from_name, get_glyph_anchor_points, get_glyph_metrics, move_glyph
import xml.etree.ElementTree as ET

sys.path.append('..')

logger = configure_logging()

class Accented_Glyph(Composed_Glyph):
    '''Glyph with accents/diacritics.'''

    def __init__(self, name: str, weight: str | None, styles: int, allow_left_overflow: bool, allow_right_overflow: bool, glyphs: list[str]):
        super().__init__(name, weight, styles, glyphs)
        self.allow_left_overflow = allow_left_overflow
        self.allow_right_overflow = allow_right_overflow

    def generate_glif(self, weight: str, style: int, ufo_dir: Path) -> int:
        # Parameters check
        super().generate_glif(weight, style, ufo_dir)

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

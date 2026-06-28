from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
from math import pi, tan
from pathlib import Path
import sys
from ufo_utils import add_glyph_reference_to_sequence, clean_glyph, get_glif_from_name
import xml.etree.ElementTree as ET

sys.path.append('..')

logger = configure_logging()

class Composite_Glyph(Composed_Glyph):
    '''Sequence of 1 or several glyphs.'''
    
    def __init__(self, name: str, weight: str | None, styles: int, copy_anchors: bool, y_offset: int, glyphs: list[str]):
        super().__init__(name, weight, styles, glyphs)
        self.copy_anchors = copy_anchors
        self.y_offset = y_offset

    def generate_glif(self, weight: str, style: int, ufo_dir: Path) -> int:
        # Parameters check
        super().generate_glif(weight, style, ufo_dir)

        # Self reference check
        if self.name in self.glyphs:
            logger.error(f'Failed to generate "{self.name}": the glyph is composed of itself.')
            return 1

        # Get dest .glif and clean it
        dst_glif: Path | None = get_glif_from_name(self.name, ufo_dir)
        if dst_glif is None:
            return 1
        dst_glif_xml_tree: ET.ElementTree[ET.Element] = ET.parse(dst_glif)
        tmp: ET.ElementTree | None = clean_glyph(dst_glif_xml_tree)  # pyright: ignore[reportArgumentType]
        if tmp is None:
            logger.error(f'Failed to clean XML tree of dst_glif for "{self.name}".')
            return 1
        dst_glif_xml_tree = tmp  # pyright: ignore[reportAssignmentType]
        del tmp

        # Reset advance value
        dst_advance_node: ET.Element[str] | None = dst_glif_xml_tree.getroot().find('advance')
        if dst_advance_node is None:
            ET.SubElement(dst_glif_xml_tree.getroot(), 'advance', {'width': '0'})
        else:
            dst_advance_node.attrib['width'] = '0'

        # Place components
        is_italic: bool = bool(style & Composed_Glyph.STYLE_ITALIC)

        for i, glyph_name in enumerate(self.glyphs):
            new_glif: Path | None = get_glif_from_name(glyph_name, ufo_dir)
            if new_glif is None:
                return 1

            try:
                new_glif_xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(new_glif)
            except Exception as err:
                logger.error(f'Failed to get XML data from "{glyph_name}": {err}')
                return 1

            new_tree: ET.ElementTree[ET.Element[str]] | None = add_glyph_reference_to_sequence(  # pyright: ignore[reportAssignmentType]
                src_glif_xml_tree=new_glif_xml_tree,  # pyright: ignore[reportArgumentType]
                dst_glif_xml_tree=dst_glif_xml_tree,  # pyright: ignore[reportArgumentType]
                ufo_dir=ufo_dir,
                copy_anchors=self.copy_anchors,
                replace_all=(i == 0),
                x_offset=(int(self.y_offset / tan(pi/2-Composed_Glyph.ITALIC_SLANT)) if is_italic else 0),
                y_offset=self.y_offset
            )
            if new_tree is None:
                return 1
            dst_glif_xml_tree = new_tree

        # Save the file
        try:
            dst_glif_xml_tree.write(dst_glif, encoding='utf-8', xml_declaration=True)
        except Exception as err:
            logger.error(f'Failed to write into "{dst_glif}": {err}')
            return 1
        logger.debug(f"Done buliding {self.name} ({len(self.glyphs)} components)")
        return 0

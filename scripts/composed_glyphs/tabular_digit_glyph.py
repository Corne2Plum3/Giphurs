from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
from pathlib import Path
import sys
from ufo_utils import add_component, clean_glyph, get_glif_from_name, get_glyph_metrics
import xml.etree.ElementTree as ET

sys.path.append('..')

logger = configure_logging()

class Tabular_Digit_Glyph(Composed_Glyph):
    '''A single digit but with forced width.'''

    def __init__(self, name: str, weight: str | None, styles: int, size: int, glyphs: list[str]):
        super().__init__(name, weight, styles, [glyphs[0]])
        assert size in [0, 1]
        self.size = size

    def generate_glif(self, weight: str, style: int, ufo_dir: Path) -> int:
        # Get left and right kern
        WIDTH_VALUES = {  # [size]
            0: 1232,  # exponents
            1: 1232   # normal digits  
        }

        # Load base .glif metrics
        base_xml_metrics: dict[str, int] = get_glyph_metrics(self.glyphs[0], ufo_dir)

        # Load destination .glif
        dst_glif: Path | None = get_glif_from_name(self.name, ufo_dir)
        if dst_glif is None:
            return 1
        dst_xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(dst_glif)
        tmp: ET.ElementTree | None = clean_glyph(dst_xml_tree)  # pyright: ignore[reportRedeclaration, reportArgumentType]
        if tmp is None:
            return 1
        dst_xml_tree = tmp  # pyright: ignore[reportAssignmentType]

        # Update advance value
        for element in dst_xml_tree.getroot().findall('advance'):  # remove existing <advance>
            dst_xml_tree.getroot().remove(element)
        glyph_width: int = WIDTH_VALUES[self.size]
        dst_xml_tree.getroot().insert(0, ET.Element('advance', {'width': str(glyph_width)}))

        # Place component
        additional_kern: int = glyph_width - base_xml_metrics['glyph_width']
        x_offset: int = int(additional_kern / 2)
        tmp = add_component(
            dst_xml_tree,  # pyright: ignore[reportArgumentType]
            self.glyphs[0], 
            x_offset=x_offset
        )
        if tmp is None:
            return 1
        dst_xml_tree = tmp  # pyright: ignore[reportAssignmentType]

        # Save the file
        try:
            dst_xml_tree.write(dst_glif, encoding='utf-8', xml_declaration=True)
        except Exception as err:
            logger.error(f'Failed to write into "{dst_glif}": {err}')
            return 1
        logger.debug(f"Done buliding {self.name} ({len(self.glyphs)} components)")
        return 0

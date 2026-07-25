from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
from math import pi, tan
from pathlib import Path
import sys
from ufo_utils import add_component, clean_glyph, get_glif_from_name, get_glyph_metrics
import xml.etree.ElementTree as ET

sys.path.append('..')

logger = configure_logging()


class Proportional_Digit_Glyph(Composed_Glyph):
    '''A single digit but with proportional width'''
    
    def __init__(self, name: str, weight: str | None, styles: int, size: int, digit_value: int, glyphs: list[str]):
        super().__init__(name, weight, styles, [glyphs[0]])
        assert size in [0, 1]
        self.size = size
        self.digit_value = digit_value
    
    def generate_glif(self, weight: str, style: int, ufo_dir: Path) -> int:
        # Parameters check
        super().generate_glif(weight, style, ufo_dir)

        # Get left and right kern
        KERN_VALUES = {  # [size][weight][digit_value]
            0: {  # exponents
                '100' : {'1': (100,200), 'other': (100,100)},
                '400' : {'1': (60,120), 'other': (60,60)},
                '1000': {'1': (50,100) , 'other': (50,50)},
                'other': {'other': (0, 0)}
            },
            1: {  # normal digits
                '100' : {'1': (140,280) , 'other': (140,140)},
                '400' : {'1': (100,200), 'other': (100,100)},
                '1000': {'1': (50,100) , 'other': (50,50)},
                'other': {'other': (0, 0)}
            }
        }
        kern_value_size_weight = KERN_VALUES[self.size][weight] if weight in KERN_VALUES[self.size] else KERN_VALUES[self.size]['other']
        left_kern: int = kern_value_size_weight[str(self.digit_value)][0] if str(self.digit_value) in kern_value_size_weight else kern_value_size_weight['other'][0]
        right_kern: int = kern_value_size_weight[str(self.digit_value)][1] if str(self.digit_value) in kern_value_size_weight else kern_value_size_weight['other'][1]

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
        is_italic: int = bool(style & Composed_Glyph.STYLE_ITALIC)
        for element in dst_xml_tree.getroot().findall('advance'):  # remove existing <advance>
            dst_xml_tree.getroot().remove(element)
        glyph_width: int = left_kern + right_kern
        if is_italic:
            glyph_width += int(base_xml_metrics['raw_width'] - base_xml_metrics['raw_height'] / tan(pi/2 - Composed_Glyph.ITALIC_SLANT))  # non-italic raw width
        else:
            glyph_width += base_xml_metrics['raw_width']
        dst_xml_tree.getroot().insert(0, ET.Element('advance', {'width': str(glyph_width)}))

        # Place component
        x_offset: int = left_kern
        if is_italic:
            x_offset -= int(base_xml_metrics['left_kern'] - base_xml_metrics['raw_height'] / (2 * tan(pi/2 - Composed_Glyph.ITALIC_SLANT)))
        else:
            x_offset -= base_xml_metrics['left_kern']
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

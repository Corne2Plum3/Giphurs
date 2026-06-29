from math import pi, tan

from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from ufo_utils import clean_glyph, get_glif_from_name, add_component, get_glyph_metrics, unlink_references

sys.path.append('..')

logger = configure_logging()

class Circled_Number_Glyph(Composed_Glyph):
    '''Number in a circle. First glyph defines the circles, glyph 2 (and 3) for digits, from left to right.'''

    def __init__(self, name: str, weight: str | None, styles: int, unlink_references: bool, glyphs: list[str]):
        super().__init__(name, weight, styles, glyphs)
        self.unlink_references = unlink_references
    
    def generate_glif(self, weight: str, style: int, ufo_dir: Path) -> int:
        # Parameters check
        super().generate_glif(weight, style, ufo_dir)
        if len(self.glyphs) == 0:
            logger.warning(f'No glyph for "{self.name}"')
            return 0

        # Constants
        TWO_DIGITS_WIDTH_COEF: dict[str, float] = {
            '100' : 4/5,
            '400' : 3/4,
            '1000': 2/3
        }  # xScale of digits in glyphs with 2 digits numbers
        TWO_DIGITS_OVERLAP: dict[str, int] = {
            '100' : 140,
            '400' : 120,
            '1000': 40
        }
        
        # Open XML file and clean it
        glif_filename: Path | None = get_glif_from_name(self.name, ufo_dir)
        if glif_filename is None:
            return 1
        xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif_filename)
        xml_root: ET.Element[str] = xml_tree.getroot()
        if xml_root.find('advance') is None:
            xml_root.append(ET.Element('advance'))
        xml_advance: ET.Element[str] = xml_root.find('advance')  # pyright: ignore[reportAssignmentType]
        xml_tree = clean_glyph(xml_tree)  # pyright: ignore[reportAssignmentType, reportArgumentType]

        # Read glyphs
        base: str = self.glyphs[0]
        digits_count = len(self.glyphs) - 1
        dt: str | None = None  # tens
        du: str | None = None  # units
        if digits_count == 0:
            pass
        elif digits_count == 1:
            du = self.glyphs[1]
        else:
            dt = self.glyphs[1]
            du = self.glyphs[2]

        # Get metrics
        base_circle_metrics: dict[str, int] = get_glyph_metrics(base, ufo_dir)
        dt_glyph_metrics: dict[str, int] = get_glyph_metrics(dt, ufo_dir) if dt is not None else {}
        du_glyph_metrics: dict[str, int] = get_glyph_metrics(du, ufo_dir) if du is not None else {}

        # Set advance
        xml_advance.attrib['width'] = str(base_circle_metrics['glyph_width'])

        # Place the base
        xml_tree = add_component(xml_tree, base)  # pyright: ignore[reportArgumentType, reportAssignmentType]

        # Place the digits
        if du is not None:  # pyright: ignore[reportUnnecessaryComparison]
            y_offset: int = -499
            middle: float = base_circle_metrics["left_kern"] + base_circle_metrics["raw_width"] / 2
            xt: float
            xu: float
            if dt is None:  # one digit : du
                xu = middle - du_glyph_metrics["glyph_width"] / 2
                if style & Composed_Glyph.STYLE_ITALIC:  # if is italic
                    xu -= abs(y_offset) / tan(pi/2-Composed_Glyph.ITALIC_SLANT)
                xml_tree = add_component(xml_tree, du, x_offset=xu, y_offset=y_offset)  # pyright: ignore[reportAssignmentType, reportArgumentType]
            else:  # two digits : tens = digit_1 and units = digit_2 (!)
                both_digits_length = (dt_glyph_metrics["glyph_width"] + du_glyph_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
                xt = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] * (Composed_Glyph.SUPS_HEIGHT / Composed_Glyph.DIGITS_HEIGHT) 
                xu = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] * (Composed_Glyph.SUPS_HEIGHT / Composed_Glyph.DIGITS_HEIGHT) - du_glyph_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
                if style & Composed_Glyph.STYLE_ITALIC:  # if is italic
                    xt -= abs(y_offset) / tan(pi/2-Composed_Glyph.ITALIC_SLANT) * TWO_DIGITS_WIDTH_COEF[weight]
                    xu -= abs(y_offset) / tan(pi/2-Composed_Glyph.ITALIC_SLANT) * TWO_DIGITS_WIDTH_COEF[weight]
                xml_tree = add_component(xml_tree, dt, x_offset=xt, y_offset=y_offset, x_scale=TWO_DIGITS_WIDTH_COEF[weight])  # pyright: ignore[reportAssignmentType, reportArgumentType]
                xml_tree = add_component(xml_tree, du, x_offset=xu, y_offset=y_offset, x_scale=TWO_DIGITS_WIDTH_COEF[weight])  # pyright: ignore[reportAssignmentType, reportArgumentType]

        # Save the file
        try:
            xml_tree.write(glif_filename, encoding='utf-8', xml_declaration=True)
        except Exception as err:
            logger.error(f'Failed to write into "{glif_filename}": {err}')
            return 1

        # Unlink reference (another save I know...)
        if self.unlink_references:
            unlink_references(self.name, ufo_dir)

        return 0

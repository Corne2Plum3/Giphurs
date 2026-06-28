from math import pi, tan

from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from ufo_utils import clean_glyph, get_glif_from_name, add_component, get_glyph_metrics, set_glyph_width

sys.path.append('..')

logger = configure_logging()

class Parenthesis_Number_Glyph(Composed_Glyph):
    '''Nuber (1 or 2 digits) between 2 glyphs.'''

    def __init__(self, name: str, weight: str | None, styles: int, glyphs: list[str]):
        super().__init__(name, weight, styles, glyphs)
    
    def generate_glif(self, weight: str, style: int, ufo_dir: Path) -> int:
        # Parameters check
        super().generate_glif(weight, style, ufo_dir)
        if len(self.glyphs) < 2:
            logger.error(f'"{self.name}": at least 2 glyphs must be provided.')
            return 1

        # Constants
        DEFAULT_KERN: dict[str, int] = {
            '100' : 140,
            '400' : 100,
            '1000': 50
        }
        TWO_DIGITS_OVERLAP: dict[str, int] = {
            '100' : 140,
            '400' : 120,
            '1000': 40
        }
        TWO_DIGITS_WIDTH_COEF: dict[str, float] = {
            '100' : 4/5,
            '400' : 3/4,
            '1000': 2/3
        }

        # Glyphs
        left_glyph: str = self.glyphs[0]
        right_glyph: str = self.glyphs[-1]
        middle_glyphs: list[str] = self.glyphs[1:-1]
        dt: str | None = None  # tens
        du: str | None = None  # units
        if len(middle_glyphs) == 0:
            pass
        elif len(middle_glyphs) == 1:
            du = middle_glyphs[0]
        else:
            dt, du = middle_glyphs[0], middle_glyphs[1]

        # Open XML file and clean it
        glif_filename: Path | None = get_glif_from_name(self.name, ufo_dir)
        if glif_filename is None:
            return 1
        xml_tree: ET.ElementTree[ET.Element[str]] = ET.parse(glif_filename)
        xml_root: ET.Element[str] = xml_tree.getroot()
        if xml_root.find('advance') is None:
            xml_root.append(ET.Element('advance'))
        xml_tree = clean_glyph(xml_tree)  # pyright: ignore[reportAssignmentType, reportArgumentType]

        # Get the metrics of the glyphs at the left and right
        left_glyph_metrics: dict[str, int] = get_glyph_metrics(left_glyph, ufo_dir)
        right_glyph_metrics: dict[str, int] = get_glyph_metrics(right_glyph, ufo_dir)
        dt_glyph_metrics: dict[str, int] = get_glyph_metrics(dt, ufo_dir) if dt is not None else {'glyph_width': 0}
        du_glyph_metrics: dict[str, int] = get_glyph_metrics(du, ufo_dir) if du is not None else {'glyph_width': 0}

        # Set advance value
        both_digits_length: float
        if dt is None:
            both_digits_length = 2 * du_glyph_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
        else:
            both_digits_length = (dt_glyph_metrics["glyph_width"] + du_glyph_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
        new_glyph_width: float = (left_glyph_metrics["raw_width"] + right_glyph_metrics["raw_width"]) * TWO_DIGITS_WIDTH_COEF[weight] + both_digits_length - TWO_DIGITS_OVERLAP[weight]
        if style & Composed_Glyph.STYLE_ITALIC:  # is italic
            new_glyph_width -= Composed_Glyph.DIGITS_HEIGHT / tan(pi/2 - Composed_Glyph.ITALIC_SLANT)
        xml_tree = set_glyph_width(xml_tree, int(new_glyph_width))  # pyright: ignore[reportAssignmentType, reportArgumentType]

        # Place the components
        xl: float = DEFAULT_KERN[weight] - left_glyph_metrics['left_kern'] * TWO_DIGITS_WIDTH_COEF[weight]
        xr: float = new_glyph_width - right_glyph_metrics['glyph_width'] * TWO_DIGITS_WIDTH_COEF[weight]
        xml_tree = add_component(xml_tree, left_glyph, x_offset=int(xl), x_scale=TWO_DIGITS_WIDTH_COEF[weight], y_offset=0)  # pyright: ignore[reportAssignmentType, reportArgumentType]
        xml_tree = add_component(xml_tree, right_glyph, x_offset=int(xr), x_scale=TWO_DIGITS_WIDTH_COEF[weight], y_offset=0)  # pyright: ignore[reportAssignmentType, reportArgumentType]
        if du is not None:
            middle: float = new_glyph_width / 2
            if dt is None:
                xu = middle - du_glyph_metrics['glyph_width'] / 2
                xml_tree = add_component(xml_tree, du, x_offset=int(xu), y_offset=0)  # pyright: ignore[reportAssignmentType, reportArgumentType]
            else:
                xt = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2
                xu = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2 - du_glyph_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
                xml_tree = add_component(xml_tree, dt, x_offset=int(xt), x_scale=TWO_DIGITS_WIDTH_COEF[weight], y_offset=0)  # pyright: ignore[reportAssignmentType, reportArgumentType]
                xml_tree = add_component(xml_tree, du, x_offset=int(xu), x_scale=TWO_DIGITS_WIDTH_COEF[weight], y_offset=0)  # pyright: ignore[reportAssignmentType, reportArgumentType]

        # Save the file
        try:
            xml_tree.write(glif_filename, encoding='utf-8', xml_declaration=True)
        except Exception as err:
            logger.error(f'Failed to write into "{glif_filename}": {err}')
            return 1

        return 0

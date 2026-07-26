from composed_glyphs.composed_glyph import Composed_Glyph
from logger import configure_logging
from math import pi, tan
from pathlib import Path
import sys
from ufo_utils import add_component, clean_glyph, get_glif_from_name, get_glyph_metrics, get_glyph_points_coordinates
import xml.etree.ElementTree as ET

sys.path.append('..')

logger = configure_logging()

class Point():
    '''Internal class representing a point.'''
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

def tuple_to_point(t: tuple[int | float, int | float]) -> Point:
    '''Converts a tuple into a Point object.'''
    return Point(t[0], t[1])

def get_box_points(points_list: list[Point]) -> dict[str, Point]:
    '''Returns a dict with a point at the `left`, `right`, `bottom` `top` of a rectangle containing all of the points.'''
    if len(points_list) < 1:
        return {'left': Point(0, 0), 'right': Point(0, 0), 'bottom': Point(0, 0), 'top': Point(0, 0)}
    left: Point = points_list[0]
    right: Point = points_list[0]
    bottom: Point = points_list[0]
    top: Point = points_list[0]
    if len(points_list) > 1:
        for p in points_list[1:]:
            if p.x < left.x:
                left = p
            if p.x > right.x:
                right = p
            if p.y < bottom.y:
                bottom = p
            if p.y > top.y:
                top = p
    return {'left': left, 'right': right, 'bottom': bottom, 'top': top}
            
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

        # Load base .glif metrics
        base_xml_metrics: dict[str, int] = get_glyph_metrics(self.glyphs[0], ufo_dir)
        is_italic: int = bool(style & Composed_Glyph.STYLE_ITALIC)
        
        # Get custom left and right kern
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
        if 'ss06' in self.name:  # bottom bar on digit 1 -> center the glyph
            right_kern = left_kern

        if is_italic:
            # Get the points at the most left, right, bottom and top
            box_points: dict[str, Point] = get_box_points([tuple_to_point(p) for p in get_glyph_points_coordinates(self.glyphs[0], ufo_dir)])
            l: Point = box_points['left']
            r: Point = box_points['right']
            b: Point = box_points['bottom']
            t: Point = box_points['top']

            # Get the bottom left and top right of the box (rectangle containing all points of the glyph)
            bl = Point(l.x - (l.y - b.y) * tan(Composed_Glyph.ITALIC_SLANT), b.y)
            tr = Point(r.x + (t.y - r.y) * tan(Composed_Glyph.ITALIC_SLANT), t.y)

            # Compute non-italic width (w)
            wi: int | float = tr.x - bl.x
            hi: int | float = tr.y - bl.y
            w: int | float = wi - hi / tan(pi/2 - Composed_Glyph.ITALIC_SLANT)

            # Kerning (idk what I'm doing but it works I guess?)
            ki_left: int = base_xml_metrics['left_kern']
            ki_right: int = base_xml_metrics['right_kern']
            left_kern = int(ki_left * w / wi)
            right_kern = int(ki_right * w / wi)
            if self.digit_value == 1 and 'ss06' not in self.name:  # <- I know it's dirty and that this is actually poorly made
                right_kern -= 70

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
        glyph_width: int = left_kern + base_xml_metrics['raw_width'] + right_kern
        dst_xml_tree.getroot().insert(0, ET.Element('advance', {'width': str(glyph_width)}))

        # Place component
        x_offset: int = left_kern - base_xml_metrics['left_kern']
        tmp = add_component(dst_xml_tree, self.glyphs[0], x_offset=x_offset)  # pyright: ignore[reportArgumentType]
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

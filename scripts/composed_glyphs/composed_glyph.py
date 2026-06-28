
from abc import abstractmethod
from math import pi
from logger import configure_logging
from pathlib import Path
import sys

sys.path.append('..')

logger = configure_logging()

class Composed_Glyph():
    '''
        Represent a glyph that can be build from other glyphs.

        Attributes:
            name: name of the glyph representated
            supported_weight: supported weight. If `None`, supports all weights
            supported_styles: supported styles (`Composed_Glyph.STYLE_NORMAL` and or `Composed_GlyphSTYLE_ITALIC`). They can be added.
            glyphs: list of components of glyph `name`.
    '''

    # Constants
    STYLE_NORMAL: int = 1
    STYLE_ITALIC: int = 2
    ITALIC_SLANT: float = 10 * pi / 180  # slant to the RIGHT in radians (the "*pi/180" converts degrees to radians)
    SUPS_HEIGHT: int = 858
    DIGITS_HEIGHT: int = 1480

    def __init__(self, name: str, supported_weight: str | None, supported_styles: int, glyphs: list[str]):
        self.name = name
        self.supported_weight = supported_weight  # None = All
        self.supported_styles = supported_styles
        self.glyphs = glyphs
        self.priority = 0  # set manually when building glyphs

    @abstractmethod
    def generate_glif(self, weight: str, style: int, ufo_dir: Path) -> int:
        '''
            Generate the .glif file related to this object. Writes inside the given UFO.

            Args:
                weight: weight of the glyph to build
                style: `Composed_Glyph.STYLE_NORMAL` or `Composed_Glyph.STYLE_ITALIC`
                ufo_dir: UFO project to write.

            Returns:
                `0` if success, non-zero if an error occured.
        '''
        # "super().generate_glif(weight, style, ufo_dir)"" should be the first line of child methods
        if self.supported_weight is not None and self.supported_weight != weight:
            logger.warning(f'Attempting to generate glyph with invalid weight "{weight}": {self.name}, w={self.supported_weight}, s={self.supported_styles}')
        if not self.supported_styles & style:
            logger.warning(f'Attempting to generate glyph with invalid style {style}: {self.name}, w={self.supported_weight}, s={self.supported_styles}')

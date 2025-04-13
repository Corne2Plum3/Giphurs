"""
This Python script generate .glif file of some glyphs that are based on digits, and with all of
their alternatives form (cv01-20, ss06-07, zero), by using components.

The components are the following:
* All digits 0-9, including cv01-20, ss06-07, zero
* Superior (sups) versions of all digits above
* Parenthesis (U+0028 and U+0029)
* White circle (U+25EF)
* Black circle (U+25CF)
* Double circle (currently on U+E02D)
* Fraction bar (U+2044)

And thus are built:
* Fractions
* Superior numbers with pnum and tnum
* subscript, numerators and denominators (+ pnum and tnum versions)
* U+2460-U+24FF and U+2776-U+277F as long they have numbers

The program takes 2 parameters: the weight value (100, 400, 1000) and the ufo directory location.
The weight value can take an additional "i" at the end (for example "400i") for italics, which can
be used to apply an offset on glyphs.
"""

from math import pi, tan
from multiprocessing import Process
import sys
from ufo_utils import *
import xml.etree.ElementTree as ET

# Performances settings
USE_MULTITHREADING = True

# Script constants

DIGITS_NAMES_ENGLISH = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

UNICODE_VALUES = {  # index = number
    "subscript": [ 0x2080 + i for i in range(10) ],
    "circle": [ 0x24EA ] + [ 0x2460 + i for i in range(20) ],
    "black_circle": [ 0x24FF ] + [ 0x2776 + i for i in range(10) ] + [ 0x24EB + i for i in range(10) ],
    "double_circle": [ -1 ] + [ 0x24F5 + i for i in range(10) ],
    "parenthezed": [ -1 ] + [ 0x2474 + i for i in range(20) ],
    "full_stop": [ -1 ] + [ 0x2488 + i for i in range(20) ],
    "frac": [  # [dnom][numr]
        #  0/     1/     2/     3/     4/     5/     6/     7/     8/     9/
        [  -1  ,0x215F,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /0 (nothing)
        [  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /1
        [  -1  ,0x00BD,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /2
        [0x2189,0x2153,0x2154,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /3
        [  -1  ,0x00BC,  -1  ,0x00BE,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /4
        [  -1  ,0x2155,0x2156,0x2157,0x2158,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /5
        [  -1  ,0x2159,  -1  ,  -1  ,  -1  ,0x215A,  -1  ,  -1  ,  -1  ,  -1  ],  # /6
        [  -1  ,0x2150,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /7
        [  -1  ,0x215B,  -1  ,0x215C,  -1  ,0x215D,  -1  ,0x215E,  -1  ,  -1  ],  # /8
        [  -1  ,0x2151,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ],  # /9
        [  -1  ,0x2152,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ,  -1  ]   # /10
        #  0/     1/     2/     3/     4/     5/     6/     7/     8/     9/
    ]
}

# {"number_0-9": list_of_available_cv}
# CAUTION: must start by 
DIGITS_CV_LIST = {
    "0": [".cv10", ".cv20"],
    "1": [".cv01", ".cv11"],
    "2": [".cv02", ".cv12"],
    "3": [".cv03", ".cv13"],
    "4": [".cv04", ".cv14"],
    "5": [".cv05", ".cv15"],
    "6": [".cv06", ".cv16"],
    "7": [".cv07", ".cv17"],
    "8": [".cv08", ".cv18"],
    "9": [".cv09", ".cv19"],
}

# {"number_0-9": list_of_available_ss}
# CAUTION: first character must be a period
DIGITS_SS_LIST = {
    "1": [".ss06"],
    "7": [".ss07"],
    "0": [".zero"],
}

# index = number
SUPERIOR_UNICODE = [0x2070, 0x00B9, 0x00B2, 0x00B3] + [ 0x2070 + i for i in range(4, 10, 1) ]  # 0-9
SUBSCRIPT_UNICODE = [ 0x2080 + i for i in range(10) ]  # 0-9
CIRCLED_UNICODE = [ 0x24EA ] + [ 0x2460 + i for i in range(20) ]  # 0-20
PARENTHESIZED_UNICODE = [None] + [ 0x2474 + i for i in range(20) ]  # 1-20
FULL_STOP_UNICODE = [None] + [ 0x2488 + i for i in range(20) ]  # 1-20
BLACK_CIRCLE_UNICODE = [ 0x24FF ] + [ 0x2776 + i for i in range(10) ] + [ 0x24EB + i for i in range(10) ]  # 0-20
DOUBLE_CIRCLE_UNICODE = [None] + [ 0x24F5 + i for i in range(10) ]  # 1-10

# {"glyph_name": unicode_value (int)}
FRACTIONS_UNICODE = {
    "onequarter": 0x00BC,
    "onehalf": 0x00BD,
    "threequarters": 0x00BE,
    "uni2150": 0x2150,
    "uni2151": 0x2151,
    "uni2152": 0x2152,
    "onethird": 0x2153,
    "twothirds": 0x2154,
    "uni2155": 0x2155,
    "uni2156": 0x2156,
    "uni2157": 0x2157,
    "uni2158": 0x2158,
    "uni2159": 0x2159,
    "uni215A": 0x215A,
    "oneeighth": 0x215B,
    "threeeighths": 0x215C,
    "fiveeighths": 0x215D,
    "seveneighths": 0x215E,
    "uni215F": 0x215F,
    "uni2189": 0x2189
}

# {"glyph name": (numr, dnom)}
FRACTIONS_DIGITS = {
    "onequarter": (1, 4),
    "onehalf": (1, 2),
    "threequarters": (3, 4),
    "uni2150": (1, 7),
    "uni2151": (1, 9),
    "uni2152": (1, 10),
    "onethird": (1, 3),
    "twothirds": (2, 3),
    "uni2155": (1, 5),
    "uni2156": (2, 5),
    "uni2157": (3, 5),
    "uni2158": (4, 5),
    "uni2159": (1, 6),
    "uni215A": (5, 6),
    "oneeighth": (1, 8),
    "threeeighths": (3, 8),
    "fiveeighths": (5, 8),
    "seveneighths": (7, 8),
    "uni215F": (1, None),
    "uni2189": (0, 3)
}

FRAC_NAMES = {  # using the bottom as reference
    "1/4": "onequarter",
    "1/2": "onehalf",
    "3/4": "threequarters",
    "1/3": "onethird",
    "2/3": "twothirds",
    "1/8": "oneeighth",
    "3/8": "threeeighths",
    "5/8": "fiveeighths",
    "7/8": "seveneighths"
}

# font constants
SUPS_Y = 810
SUBS_Y = -188
NUMR_Y = 622
DNOM_Y = 0
CENTER_Y = 311
DEFAULT_KERN = {
    "100": 140,
    "400": 100,
    "1000": 50
}
PNUM_SUPS_KERN = {  # "other" must be used for one.ss06!!!
    "100": {
        "1": (84,140),
        "other": (140,140)
    },
    "400": {
        "1": (50,120),
        "other": (60,60)
    },
    "1000": {
        "1": (60,84),
        "other": (50,50)
    }
}
TNUM_WIDTH = {
    "100": 1232,
    "400": 1232,
    "1000": 1232
}
TWO_DIGITS_WIDTH_COEF = {
    "100": 4/5,
    "400": 3/4,
    "1000": 2/3
}
TWO_DIGITS_OVERLAP = {  # for NORMAL size without TWO_DIGITS_WIDTH_COEF applied
    "100": 140,
    "400": 120,
    "1000": 40
}
FRAC_BAR_OVERLAP = 315  # kern between numr/dnom and the fraction bar (U+2044)
DIGITS_HEIGHT = 1480
SUPS_HEIGHT = 858
ITALIC_SLANT = 10*pi/180  # slant to the RIGHT in radians (the "*pi/180" converts degrees to radians)
ITALIC_X_OFFSET = -130  # move to the right some italic glyphs

 
def build_circled_number(glyph_name: str, weight: int, is_italic: bool, ufo_dir: str, circle_type: str):
    """
    circle_type: one of the following: "circle", "black_circle", "double_circle"
    """
    assert circle_type in ["circle", "black_circle", "double_circle"]

    # Get the number and the digits to draw
    n = None
    if circle_type == "circle":
        n = CIRCLED_UNICODE.index(int(glyph_name.split(".")[0][3:], 16))  # all glyph names starts with "uniXXXX"
    elif circle_type == "black_circle":
        n = BLACK_CIRCLE_UNICODE.index(int(glyph_name.split(".")[0][3:], 16))
    elif circle_type == "double_circle":
        n = DOUBLE_CIRCLE_UNICODE.index(int(glyph_name.split(".")[0][3:], 16))
    d1 = n // 10  # tens digit
    d2 = n % 10  # units digit

    # Get the base (the circle) and its metrics
    base_circle = None
    if circle_type == "circle":
        base_circle = "uni25EF"
    elif circle_type == "black_circle":
        base_circle = "H18533"
    elif circle_type == "double_circle":
        base_circle = "double_circle_empty"
    base_circle_metrics = get_glyph_metrics(base_circle, ufo_dir)

    # Get the digits glyphs and their metrics
    d1_glyph = DIGITS_NAMES_ENGLISH[d1]
    d2_glyph = DIGITS_NAMES_ENGLISH[d2]
    cv_list = find_cv_from_name(glyph_name)
    for cv in cv_list:
        if d1 != 0 and (str(d1) in DIGITS_CV_LIST) and (cv in DIGITS_CV_LIST[str(d1)]):
            d1_glyph = d1_glyph + cv
        if (str(d2) in DIGITS_CV_LIST) and (cv in DIGITS_CV_LIST[str(d2)]):
            d2_glyph = d2_glyph + cv
    ss_list = find_ss_from_name(glyph_name)   
    for ss in ss_list:
        if d1 != 0 and (str(d1) in DIGITS_SS_LIST) and (ss in DIGITS_SS_LIST[str(d1)]):
            d1_glyph = d1_glyph + ss
        if (str(d2) in DIGITS_SS_LIST) and (ss in DIGITS_SS_LIST[str(d2)]):
            d2_glyph = d2_glyph + ss
    d1_glyph += ".superior"
    d2_glyph += ".superior"
    d1_glyph_metrics = get_glyph_metrics(d1_glyph, ufo_dir)
    d2_glyph_metrics = get_glyph_metrics(d2_glyph, ufo_dir)

    # Start to build the xml (output)
    xml_root = ET.Element("glyph", {"name": glyph_name, "format": "2"})
    ET.SubElement(xml_root, "advance", {"width": str(base_circle_metrics["glyph_width"])})  # glyph width
    if len(cv_list) == 0 and len(ss_list) == 0:  # unicode value (if any)
        unicode_value = None
        if circle_type == "circle":
            unicode_value = CIRCLED_UNICODE[n]
        elif circle_type == "black_circle":
            unicode_value = BLACK_CIRCLE_UNICODE[n]
        elif circle_type == "double_circle":
            unicode_value = DOUBLE_CIRCLE_UNICODE[n]
        ET.SubElement(xml_root, "unicode", {"hex": hex(unicode_value).upper()[2:]})

    # Place the components
    xml_outline = ET.SubElement(xml_root, "outline")
    ET.SubElement(xml_outline, "component", {"base": base_circle})
    y_offset = CENTER_Y - SUPS_Y
    middle = base_circle_metrics["left_kern"] + base_circle_metrics["raw_width"] / 2
    if d1 == 0:  # one digit : d2
        x2 = middle - d2_glyph_metrics["glyph_width"] / 2
        if is_italic:
            x2 -= abs(y_offset) / tan(pi/2-ITALIC_SLANT)
        ET.SubElement(xml_outline, "component", {"base": d2_glyph, "xOffset": str(int(x2)), "yOffset": str(int(y_offset))})
    else:  # two digits : dozens = digit_1 and units = digit_2 (!)
        both_digits_length = (d1_glyph_metrics["glyph_width"] + d2_glyph_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
        x1 = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] * (SUPS_HEIGHT / DIGITS_HEIGHT) 
        x2 = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] * (SUPS_HEIGHT / DIGITS_HEIGHT) - d2_glyph_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
        if is_italic:
            x1 -= abs(y_offset) / tan(pi/2-ITALIC_SLANT) * TWO_DIGITS_WIDTH_COEF[weight]
            x2 -= abs(y_offset) / tan(pi/2-ITALIC_SLANT) * TWO_DIGITS_WIDTH_COEF[weight]
        ET.SubElement(xml_outline, "component", {"base": d1_glyph, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x1)), "yOffset": str(int(y_offset))})
        ET.SubElement(xml_outline, "component", {"base": d2_glyph, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x2)), "yOffset": str(int(y_offset))})

    # Save
    tree = ET.ElementTree(xml_root)
    tree.write(get_glif_from_name(glyph_name, ufo_dir), encoding="UTF-8", xml_declaration=True)

    # Unlink reference for black circles
    if circle_type == "black_circle":
        unlink_references(glyph_name, ufo_dir)
    
    return

def build_fraction(glyph_name: str, weight: int, is_italic: bool, ufo_dir: str):

    base_glyph_name = glyph_name.split(".")[0]

    # Get the numr and dnom values and the digits to draw
    numr_value = FRACTIONS_DIGITS[base_glyph_name][0]
    dnom_value = FRACTIONS_DIGITS[base_glyph_name][1]

    # Get the fraction bar and its metrics
    base_frac = "fraction"
    base_frac_metrics = get_glyph_metrics(base_frac, ufo_dir)

    n0 = numr_value % 10  # unit digit for the numerator
    d0 = dnom_value % 10 if dnom_value is not None else None  # unit digit for denominator
    d1 = dnom_value // 10 if dnom_value is not None else None  # tens digit for denominator
    n0_glyph = DIGITS_NAMES_ENGLISH[n0]
    d0_glyph = DIGITS_NAMES_ENGLISH[d0] if d0 is not None else None 
    d1_glyph = DIGITS_NAMES_ENGLISH[d1] if (d1 is not None and d1 >= 1) else None 
    cv_list = find_cv_from_name(glyph_name)
    for cv in cv_list:
        if cv in DIGITS_CV_LIST[str(n0)]:
            n0_glyph = n0_glyph + cv
        if d0_glyph is not None and cv in DIGITS_CV_LIST[str(d0)]:
            d0_glyph = d0_glyph + cv
        if d1_glyph is not None and cv in DIGITS_CV_LIST[str(d1)]:
            d1_glyph = d1_glyph + cv
    ss_list = find_ss_from_name(glyph_name)   
    for ss in ss_list:
        if str(n0) in DIGITS_SS_LIST and ss in DIGITS_SS_LIST[str(n0)]:
            n0_glyph = n0_glyph + ss
        if d0_glyph is not None and str(d0) in DIGITS_SS_LIST and ss in DIGITS_SS_LIST[str(d0)]:
            d0_glyph = d0_glyph + ss
        if d1_glyph is not None and str(d1) in DIGITS_SS_LIST and ss in DIGITS_SS_LIST[str(d1)]:
            d1_glyph = d1_glyph + ss
    n0_glyph += ".superior"
    if d0_glyph is not None:
        d0_glyph += ".superior"
    if d1_glyph is not None:
        d1_glyph += ".superior"
    n0_glyph_metrics = get_glyph_metrics(n0_glyph, ufo_dir)
    d0_glyph_metrics = get_glyph_metrics(d0_glyph, ufo_dir) if d0_glyph is not None else None
    d1_glyph_metrics = get_glyph_metrics(d1_glyph, ufo_dir) if d1_glyph is not None else None

    # Begin the XML file
    xml_root = ET.Element("glyph", {"name": glyph_name, "format": "2"})

    # Advance value calculation (entire glyph width)
    advance = n0_glyph_metrics["glyph_width"] + base_frac_metrics["glyph_width"] - FRAC_BAR_OVERLAP  # numr + bar
    if d0_glyph is not None:  # dnom (hide if 0)
        if dnom_value >= 10:  # 1/10
            advance += d1_glyph_metrics["left_kern"] + d1_glyph_metrics["raw_width"] - FRAC_BAR_OVERLAP + d0_glyph_metrics["glyph_width"]
            if is_italic:
                advance -= d1_glyph_metrics["right_kern"] + d0_glyph_metrics["left_kern"]
            if not ".ss06" in d1_glyph:  # add extra kern if there isn't a bar under the digit 1
                advance += d0_glyph_metrics["left_kern"]
        else:
            advance += d0_glyph_metrics["glyph_width"] - FRAC_BAR_OVERLAP
    ET.SubElement(xml_root, "advance", {"width": str(int(advance))})
    
    # Unicode value calculation
    if len(cv_list) == 0 and len(ss_list) == 0:
        ET.SubElement(xml_root, "unicode", {"hex": hex(FRACTIONS_UNICODE[base_glyph_name]).upper()[2:]})

    # Place the numerator (for now only 1 digit supported)
    xml_outline = ET.SubElement(xml_root, "outline")
    xn0 = 0
    yn0 = NUMR_Y - SUPS_Y
    if is_italic:
        xn0 -= abs(yn0) / tan(pi/2-ITALIC_SLANT)
    ET.SubElement(xml_outline, "component", {"base": n0_glyph, "xOffset": str(int(xn0)), "yOffset": str(int(yn0))})

    # Place the fraction bar
    xf = n0_glyph_metrics["glyph_width"] - FRAC_BAR_OVERLAP
    ET.SubElement(xml_outline, "component", {"base": base_frac, "xOffset": str(int(xf)), "yOffset": "0"})

    # Place the denominator$
    if d0_glyph is not None:  # no denominator for "1/0"
        yd =  DNOM_Y - SUPS_Y
        if d1_glyph is not None:
            xd1 = xf + base_frac_metrics["glyph_width"] - FRAC_BAR_OVERLAP
            xd0 = xd1 + d1_glyph_metrics["left_kern"] + d1_glyph_metrics["raw_width"]
            if not "ss06" in d1_glyph:  # add extra kern if there isn't a bar under the digit 1
                xd0 += d0_glyph_metrics["left_kern"]
            if is_italic:
                xd1 -= abs(yd) / tan(pi/2-ITALIC_SLANT)
                xd0 -= abs(yd) / tan(pi/2-ITALIC_SLANT)
                xd0 -= d1_glyph_metrics["right_kern"] + d0_glyph_metrics["left_kern"]
            ET.SubElement(xml_outline, "component", {"base": d1_glyph, "xOffset": str(int(xd1)), "yOffset": str(int(yd))})
            ET.SubElement(xml_outline, "component", {"base": d0_glyph, "xOffset": str(int(xd0)), "yOffset": str(int(yd))})
        else:
            xd0 = xf + base_frac_metrics["glyph_width"] - FRAC_BAR_OVERLAP
            if is_italic:
                xd0 -= abs(yd) / tan(pi/2-ITALIC_SLANT)
            ET.SubElement(xml_outline, "component", {"base": d0_glyph, "xOffset": str(int(xd0)), "yOffset": str(int(yd))})
    
    # Save
    tree = ET.ElementTree(xml_root)
    tree.write(get_glif_from_name(glyph_name, ufo_dir), encoding="UTF-8", xml_declaration=True)
    return

def build_full_stop_number(glyph_name: str, weight: int, is_italic: bool, ufo_dir: str):
    # Get the number and the digits to draw
    n = FULL_STOP_UNICODE.index(int(glyph_name.split(".")[0][3:], 16))  # all glyph names starts with "uniXXXX"
    d1 = n // 10  # tens digit
    d2 = n % 10  # units digit

    # Get the base . and its metrics
    base_period = "period"
    base_period_metrics = get_glyph_metrics(base_period, ufo_dir)

    # Get the digits glyphs and their metrics
    d1_glyph = DIGITS_NAMES_ENGLISH[d1]
    d2_glyph = DIGITS_NAMES_ENGLISH[d2]
    cv_list = find_cv_from_name(glyph_name)
    for cv in cv_list:
        if d1 != 0 and (str(d1) in DIGITS_CV_LIST) and (cv in DIGITS_CV_LIST[str(d1)]):
            d1_glyph = d1_glyph + cv
        if (str(d2) in DIGITS_CV_LIST) and (cv in DIGITS_CV_LIST[str(d2)]):
            d2_glyph = d2_glyph + cv
    ss_list = find_ss_from_name(glyph_name)   
    for ss in ss_list:
        if d1 != 0 and (str(d1) in DIGITS_SS_LIST) and (ss in DIGITS_SS_LIST[str(d1)]):
            d1_glyph = d1_glyph + ss
        if (str(d2) in DIGITS_SS_LIST) and (ss in DIGITS_SS_LIST[str(d2)]):
            d2_glyph = d2_glyph + ss
    d1_glyph_metrics = get_glyph_metrics(d1_glyph, ufo_dir)
    d2_glyph_metrics = get_glyph_metrics(d2_glyph, ufo_dir)

    # Start to build the xml (output)
    xml_root = ET.Element("glyph", {"name": glyph_name, "format": "2"})
    both_digits_length = (d1_glyph_metrics["glyph_width"] + d2_glyph_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
    new_glyph_width = DEFAULT_KERN[weight] / 2 + both_digits_length + base_period_metrics["raw_width"] + DEFAULT_KERN[weight] - TWO_DIGITS_OVERLAP[weight]
    ET.SubElement(xml_root, "advance", {"width": str(new_glyph_width)})  # glyph width
    if len(cv_list) == 0 and len(ss_list) == 0:  # unicode value (if any)
        unicode_value = FULL_STOP_UNICODE[n]
        ET.SubElement(xml_root, "unicode", {"hex": hex(unicode_value).upper()[2:]})
    
    # Place the components
    xml_outline = ET.SubElement(xml_root, "outline")
    xp = new_glyph_width - base_period_metrics["left_kern"] - base_period_metrics["raw_width"] - DEFAULT_KERN[weight]
    ET.SubElement(xml_outline, "component", {"base": base_period, "xOffset": str(int(xp)), "yOffset": "0"})
    middle = (new_glyph_width - base_period_metrics["glyph_width"]) / 2 + DEFAULT_KERN[weight]
    if d1 == 0:
        x2 = middle - d2_glyph_metrics["glyph_width"] / 2 + DEFAULT_KERN[weight]
        ET.SubElement(xml_outline, "component", {"base": d2_glyph, "xOffset": str(int(x2)), "yOffset": "0"})
    else:
        x1 = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2
        x2 = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2 - d2_glyph_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
        ET.SubElement(xml_outline, "component", {"base": d1_glyph, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x1)), "yOffset": "0"})
        ET.SubElement(xml_outline, "component", {"base": d2_glyph, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x2)), "yOffset": "0"})

    tree = ET.ElementTree(xml_root)
    tree.write(get_glif_from_name(glyph_name, ufo_dir), encoding="UTF-8", xml_declaration=True)
    return

def build_parenthesized_number(glyph_name: str, weight: int, is_italic: bool, ufo_dir: str):
    # Get the number and the digits to draw
    n = PARENTHESIZED_UNICODE.index(int(glyph_name.split(".")[0][3:], 16))  # all glyph names starts with "uniXXXX"
    d1 = n // 10  # tens digit
    d2 = n % 10  # units digit

    # Get the base () and its metrics
    base_pl = "parenleft"
    base_pr = "parenright"
    base_pl_metrics = get_glyph_metrics(base_pl, ufo_dir)
    base_pr_metrics = get_glyph_metrics(base_pr, ufo_dir)

    # Get the digits glyphs and their metrics
    d1_glyph = DIGITS_NAMES_ENGLISH[d1]
    d2_glyph = DIGITS_NAMES_ENGLISH[d2]
    cv_list = find_cv_from_name(glyph_name)
    for cv in cv_list:
        if d1 != 0 and (str(d1) in DIGITS_CV_LIST) and (cv in DIGITS_CV_LIST[str(d1)]):
            d1_glyph = d1_glyph + cv
        if (str(d2) in DIGITS_CV_LIST) and (cv in DIGITS_CV_LIST[str(d2)]):
            d2_glyph = d2_glyph + cv
    ss_list = find_ss_from_name(glyph_name)   
    for ss in ss_list:
        if d1 != 0 and (str(d1) in DIGITS_SS_LIST) and (ss in DIGITS_SS_LIST[str(d1)]):
            d1_glyph = d1_glyph + ss
        if (str(d2) in DIGITS_SS_LIST) and (ss in DIGITS_SS_LIST[str(d2)]):
            d2_glyph = d2_glyph + ss
    d1_glyph_metrics = get_glyph_metrics(d1_glyph, ufo_dir)
    d2_glyph_metrics = get_glyph_metrics(d2_glyph, ufo_dir)

    # Start to build the xml (output)
    xml_root = ET.Element("glyph", {"name": glyph_name, "format": "2"})
    both_digits_length = (d1_glyph_metrics["glyph_width"] + d2_glyph_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
    new_glyph_width = (base_pl_metrics["raw_width"] + base_pr_metrics["raw_width"]) * TWO_DIGITS_WIDTH_COEF[weight] + both_digits_length - TWO_DIGITS_OVERLAP[weight]
    ET.SubElement(xml_root, "advance", {"width": str(new_glyph_width)})  # glyph width
    if len(cv_list) == 0 and len(ss_list) == 0:  # unicode value (if any)
        unicode_value = PARENTHESIZED_UNICODE[n]
        ET.SubElement(xml_root, "unicode", {"hex": hex(unicode_value).upper()[2:]})

    # Place the components
    xml_outline = ET.SubElement(xml_root, "outline")
    xl = DEFAULT_KERN[weight] - base_pl_metrics["left_kern"] * TWO_DIGITS_WIDTH_COEF[weight]
    xr = new_glyph_width - DEFAULT_KERN[weight] - (base_pr_metrics["left_kern"] + base_pr_metrics["raw_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
    ET.SubElement(xml_outline, "component", {"base": base_pl, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(xl)), "yOffset": "0"})
    ET.SubElement(xml_outline, "component", {"base": base_pr, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(xr)), "yOffset": "0"})
    if d1 == 0:
        x2 = DEFAULT_KERN[weight] + ((new_glyph_width - 2*DEFAULT_KERN[weight]) - d2_glyph_metrics["glyph_width"]) * 0.5
        ET.SubElement(xml_outline, "component", {"base": d2_glyph, "xOffset": str(int(x2)), "yOffset": "0"})
    else:
        middle = new_glyph_width / 2
        x1 = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2
        x2 = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2 - d2_glyph_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
        ET.SubElement(xml_outline, "component", {"base": d1_glyph, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x1)), "yOffset": "0"})
        ET.SubElement(xml_outline, "component", {"base": d2_glyph, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x2)), "yOffset": "0"})

    # Save
    tree = ET.ElementTree(xml_root)
    tree.write(get_glif_from_name(glyph_name, ufo_dir), encoding="UTF-8", xml_declaration=True)
    return

def build_small_digit(glyph_name: str, weight: int, is_italic: bool, ufo_dir: str, type: str):
    """
    type: one of the following : "superior", "subscript", "numr", "dnom"
    """
    assert type in ["superior", "subscript", "numr", "dnom"]
    
    # Read parameters
    is_pnum = ".pnum" in glyph_name
    is_tnum = ".tnum" in glyph_name

    # Find the glyph to draw and its metrics
    base_glyph = glyph_name.split(".")[0]
    cv_list = find_cv_from_name(glyph_name)
    if len(cv_list) >= 1:
        base_glyph += cv_list[0]
    ss_list = find_ss_from_name(glyph_name)
    if len(ss_list) >= 1:
        base_glyph += ss_list[0]
    base_glyph += ".superior"
    base_metrics = get_glyph_metrics(base_glyph, ufo_dir)

    # Start to build the xml (output)
    xml_root = ET.Element("glyph", {"name": glyph_name, "format": "2"})

    # Calculate x offset and width
    x_offset = 0
    width = 0
    if is_pnum:
        if "one" in base_glyph:
            x_offset = PNUM_SUPS_KERN[weight]["1"][0] - base_metrics["left_kern"]
            width = PNUM_SUPS_KERN[weight]["1"][0] + base_metrics["raw_width"] + PNUM_SUPS_KERN[weight]["1"][1]
        else:
            x_offset = PNUM_SUPS_KERN[weight]["other"][0] - base_metrics["left_kern"]
            width = PNUM_SUPS_KERN[weight]["other"][0] + base_metrics["raw_width"] + PNUM_SUPS_KERN[weight]["other"][1]
        if is_italic:
            x_offset += tan(ITALIC_SLANT) * SUPS_HEIGHT / 2
            width -= tan(ITALIC_SLANT) * SUPS_HEIGHT / 2
    elif is_tnum:
        width = TNUM_WIDTH[weight]
        additional_kern = width - base_metrics["glyph_width"]
        x_offset = int(base_metrics["left_kern"] + additional_kern / 2 + ITALIC_X_OFFSET)
    else:    
        x_offset = 0
        width = base_metrics["glyph_width"]

    # Add more x offset if italic (none if superior) as we move the glyph only below
    if is_italic:
        if type == "subscript":
            x_offset -= abs(SUPS_Y - SUBS_Y) / tan(pi/2-ITALIC_SLANT)
        elif type == "numr":
            x_offset -= abs(SUPS_Y - NUMR_Y) / tan(pi/2-ITALIC_SLANT)
        elif type == "dnom":
            x_offset -= abs(SUPS_Y - DNOM_Y) / tan(pi/2-ITALIC_SLANT)

    # Calculate the y position
    y_offset = 0  # value for superior
    if type == "subscript":
        y_offset = SUBS_Y - SUPS_Y
    elif type == "numr":
        y_offset = NUMR_Y - SUPS_Y
    elif type == "dnom":
        y_offset = DNOM_Y - SUPS_Y
    
    # Build the xml and place components
    ET.SubElement(xml_root, "advance", {"width": str(width)})
    if type == "superior" and len(cv_list) == 0 and len(ss_list) == 0 and not is_pnum and not is_tnum:  # add unicode if any
        ET.SubElement(xml_root, "unicode", {"hex": hex(SUPERIOR_UNICODE[DIGITS_NAMES_ENGLISH.index(glyph_name.split(".")[0])]).upper()[2:]})
    elif type == "subscript" and len(cv_list) == 0 and len(ss_list) == 0 and not is_pnum and not is_tnum:
        ET.SubElement(xml_root, "unicode", {"hex": hex(SUBSCRIPT_UNICODE[DIGITS_NAMES_ENGLISH.index(glyph_name.split(".")[0])]).upper()[2:]})
    xml_outline = ET.SubElement(xml_root, "outline")
    ET.SubElement(xml_outline, "component", {"base": base_glyph, "xOffset": str(int(x_offset)), "yOffset": str(int(y_offset))})

    # Save
    tree = ET.ElementTree(xml_root)
    tree.write(get_glif_from_name(glyph_name, ufo_dir), encoding="UTF-8", xml_declaration=True)
    return

def find_cv_from_name(glyph_name: str):
    """
    Returns cv styles used in the glyph (from the name)
    """
    # Get the list of all available character variants
    all_cv_list = []
    for digit in DIGITS_CV_LIST:
        all_cv_list += DIGITS_CV_LIST[digit]

    glyph_cv_list = []
    for e in glyph_name.split(".")[1:]:
        if "." + e in all_cv_list:
            glyph_cv_list.append("." + e)
    
    return glyph_cv_list

def find_ss_from_name(glyph_name: str):
    """
    Returns stylistic sets used in the glyph (from the name)
    """
    # Get the list of all available character variants
    all_ss_list = []
    for digit in DIGITS_SS_LIST:
        all_ss_list += DIGITS_SS_LIST[digit]

    glyph_ss_list = []
    for e in glyph_name.split(".")[1:]:
        if "." + e in all_ss_list:
            glyph_ss_list.append("." + e)
    
    return glyph_ss_list

def get_glyph_list():
    """
    Generate the full list of glyphs to generate within this script.

    Returns an array with the name of each glyph.
    """

    glyph_list = []

    # sups/subs/numr/dnom
    for n in range(10):
        for cv in [""] + (DIGITS_CV_LIST[str(n)] if str(n) in DIGITS_CV_LIST else []):
            for ss in [""] + (DIGITS_SS_LIST[str(n)] if str(n) in DIGITS_SS_LIST else []):
                for ssnd in [".superior", ".subscript", ".numr", ".dnom"]:
                    for _pt in ["", ".pnum", ".tnum"]:
                        if not(ssnd == ".superior" and _pt == ""):
                            glyph_list.append(DIGITS_NAMES_ENGLISH[n] + cv + ss + ssnd + _pt)
            
    # 1 digit circled/parenthesized/full_stop/black_circle/double_circle (0-9 ; 11)
    for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]:
        for cv in [""] + (DIGITS_CV_LIST[str(n%10)] if str(n%10) in DIGITS_CV_LIST else []):
            for ss in [""] + (DIGITS_SS_LIST[str(n%10)] if str(n%10) in DIGITS_SS_LIST else []):
                glyph_list.append(f"uni{str(hex(CIRCLED_UNICODE[n]).upper()[2:])}" + cv + ss)
                if n >= 1:
                    glyph_list.append(f"uni{str(hex(PARENTHESIZED_UNICODE[n]).upper()[2:])}" + cv + ss)
                    glyph_list.append(f"uni{str(hex(FULL_STOP_UNICODE[n]).upper()[2:])}" + cv + ss)
                glyph_list.append(f"uni{str(hex(BLACK_CIRCLE_UNICODE[n]).upper()[2:])}" + cv + ss)
                if n >= 1 and n <= 10:
                    glyph_list.append(f"uni{str(hex(DOUBLE_CIRCLE_UNICODE[n]).upper()[2:])}" + cv + ss)

    # 2 digit circled/parenthesized/full_stop/black_circle/double_circle (10 ; 12-20)
    for n in [10, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
        d1 = n // 10
        d2 = n % 10
        for cv1 in [""] + (DIGITS_CV_LIST[str(d1)] if str(d1) in DIGITS_CV_LIST else []):
            for cv2 in [""] + (DIGITS_CV_LIST[str(d2)] if str(d2) in DIGITS_CV_LIST else []):
                cv1_temp, cv2_temp = cv1, cv2
                if cv1 != "" and cv2 != "" and int(cv1[3:]) > int(cv2[3:]):  # swap if needed because all cv must be in ascending order
                    cv1_temp, cv2_temp = cv2, cv1
                for ss1 in [""] + (DIGITS_SS_LIST[str(d1)] if str(d1) in DIGITS_SS_LIST else []):
                    for ss2 in [""] + (DIGITS_SS_LIST[str(d2)] if str(d2) in DIGITS_SS_LIST else []):
                        # ss1 and ss2 would be swapped for 71, 01 and 07 (not possible)
                        glyph_list.append(f"uni{str(hex(CIRCLED_UNICODE[n]).upper()[2:])}" + cv1_temp + cv2_temp + ss1 + ss2)
                        glyph_list.append(f"uni{str(hex(PARENTHESIZED_UNICODE[n]).upper()[2:])}" + cv1_temp + cv2_temp + ss1 + ss2)
                        glyph_list.append(f"uni{str(hex(FULL_STOP_UNICODE[n]).upper()[2:])}" + cv1_temp + cv2_temp + ss1 + ss2)
                        glyph_list.append(f"uni{str(hex(BLACK_CIRCLE_UNICODE[n]).upper()[2:])}" + cv1_temp + cv2_temp + ss1 + ss2)
                        if n == 10:
                            glyph_list.append(f"uni{str(hex(DOUBLE_CIRCLE_UNICODE[n]).upper()[2:])}" + cv1_temp + cv2_temp + ss1 + ss2)

    # Fraction 1/ (uni215F)
    for cv in [""] + (DIGITS_CV_LIST["1"] if "1" in DIGITS_CV_LIST else []):
        for ss in [""] + (DIGITS_SS_LIST["1"] if "1" in DIGITS_SS_LIST else []):
            glyph_list.append(f"uni215F" + cv + ss)
    
    # Fraction 1/10 (uni2152)
    for cv1 in [""] + (DIGITS_CV_LIST["1"] if "1" in DIGITS_CV_LIST else []):
        for cv0 in [""] + (DIGITS_CV_LIST["0"] if "0" in DIGITS_CV_LIST else []):
            cv1_temp, cv2_temp = cv1, cv0
            if cv1 != "" and cv0 != "" and int(cv1[3:]) > int(cv0[3:]):  # swap if needed because all cv must be in ascending order
                cv1_temp, cv2_temp = cv0, cv1
            for ss1 in [""] + (DIGITS_SS_LIST["1"] if "1" in DIGITS_SS_LIST else []):
                for ss0 in [""] + (DIGITS_SS_LIST["0"] if "0" in DIGITS_SS_LIST else []):
                    glyph_list.append(f"uni2152" + cv1_temp + cv2_temp + ss1 + ss0)

    # Other fractions
    for fraction_name in FRACTIONS_DIGITS:
        if not fraction_name in ["uni2152", "uni215F"]:  # ignore 1/ and 1/10 (done earlier)
            n = FRACTIONS_DIGITS[fraction_name][0]
            d = FRACTIONS_DIGITS[fraction_name][1]
            for cv1 in [""] + (DIGITS_CV_LIST[str(n)] if str(n) in DIGITS_CV_LIST else []):
                for cv2 in [""] + (DIGITS_CV_LIST[str(d)] if str(d) in DIGITS_CV_LIST else []):
                    cv1_temp, cv2_temp = cv1, cv2
                    if cv1 != "" and cv2 != "" and int(cv1[3:]) > int(cv2[3:]):  # swap if needed because all cv must be in ascending order
                        cv1_temp, cv2_temp = cv2, cv1
                    for ss1 in [""] + (DIGITS_SS_LIST[str(n)] if str(n) in DIGITS_SS_LIST else []):
                        for ss2 in [""] + (DIGITS_SS_LIST[str(d)] if str(d) in DIGITS_SS_LIST else []):
                            # ss1 and ss2 would be swapped for 7/1, 0/1 and 0/7 (not possible)
                            glyph_list.append(fraction_name + cv1_temp + cv2_temp + ss1 + ss2)

    return glyph_list

def main():
    if len(sys.argv) < 3:
        print(f"{sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <weight> <ufo_directory> [<glyph_name>]")
        print(f"* weight can be either '100', '400' or '1000', can be followed by a 'i' for italics (for example '400i')")
        print("If a glyph name isn't provided, all glyphs supported by the script of the font will be built.")
        return
    
    # Read parameters
    weight = sys.argv[1]
    ufo_dir = sys.argv[2] 

    # Get weight and is_italic parameters
    is_italic = weight[-1] == "i"
    if is_italic:  # remove the "i" at the end
        weight = weight[:-1]

    # Get the list of glyphs to generate
    glyph_list = []
    if len(sys.argv) > 3:
        glyph_list.append(sys.argv[3])
    else:
        glyph_list = get_glyph_list()

    # Generate each glyphs
    nb_glyphs = len(glyph_list)
    if USE_MULTITHREADING:
        processes = [ Process(target=build_single_glyph, args=(glyph_list[i], weight, is_italic, ufo_dir, i, nb_glyphs)) for i in range(nb_glyphs) ]
        # start all processes
        for process in processes:
            process.start()
        # wait for all processes to complete
        for process in processes:
            process.join()
    else:  # single thread (recommended for debug)
        for index, glyph_name in enumerate(glyph_list, start=1):
            build_single_glyph(glyph_name, weight, is_italic, ufo_dir, index, nb_glyphs)

def build_single_glyph(glyph_name, weight, is_italic, ufo_dir, index, nb_glyphs):
    """
    Sub-process of main() supposed to work in parallel which read a line of glyph_list.
    Returns nothing.
    """

    # Display
    sys.stdout.write('\033[2K\033[1G')
    print(f"[{index+1}/{nb_glyphs} ({int((index+1)/nb_glyphs*100)}%)] Working on {glyph_name}...", end="\r")

    # Create the glyph
    base_name = glyph_name.split(".")[0]
    if ".superior" in glyph_name:
        build_small_digit(glyph_name, weight, is_italic, ufo_dir, "superior")
    elif ".subscript" in glyph_name:
        build_small_digit(glyph_name, weight, is_italic, ufo_dir, "subscript")
    elif ".numr" in glyph_name:
        build_small_digit(glyph_name, weight, is_italic, ufo_dir, "numr")
    elif ".dnom" in glyph_name:
        build_small_digit(glyph_name, weight, is_italic, ufo_dir, "dnom")
    elif base_name in FRACTIONS_UNICODE:
        build_fraction(glyph_name, weight, is_italic, ufo_dir)
    # from this point we're sure the glyph name starts by "uniXXXX"
    elif int(base_name[3:], 16) in CIRCLED_UNICODE:
        build_circled_number(glyph_name, weight, is_italic, ufo_dir, "circle")
    elif int(base_name[3:], 16) in BLACK_CIRCLE_UNICODE:
        build_circled_number(glyph_name, weight, is_italic, ufo_dir, "black_circle")
    elif int(base_name[3:], 16) in DOUBLE_CIRCLE_UNICODE:
        build_circled_number(glyph_name, weight, is_italic, ufo_dir, "double_circle")
    elif int(base_name[3:], 16) in PARENTHESIZED_UNICODE:
        build_parenthesized_number(glyph_name, weight, is_italic, ufo_dir)
    elif int(base_name[3:], 16) in FULL_STOP_UNICODE:
        build_full_stop_number(glyph_name, weight, is_italic, ufo_dir)
    else:
        print(f"{sys.argv[0]}: I don't know how to build {glyph_name}")

    return

if __name__ == "__main__":
    main()

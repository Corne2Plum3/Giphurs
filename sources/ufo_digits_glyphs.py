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
import sys
from ufo_utils import *
import xml.etree.ElementTree as ET

DIGITS_NAMES_ENGLISH = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

DIGITS_NAMES = {
    "def": DIGITS_NAMES_ENGLISH,
    "ss01": [ "zero.cv10" ] + [ DIGITS_NAMES_ENGLISH[i] + ".cv" + str(i).zfill(2) for i in range(1,10,1)],
    "ss02": [ "zero.cv20" ] + [ DIGITS_NAMES_ENGLISH[i%10] + ".cv" + str(i).zfill(2) for i in range(11,20,1)]
}

SUPS_NAMES = {
    "def": [ f"{DIGITS_NAMES_ENGLISH[i]}.superior" for i in range(10) ],
    "ss01": [ "zero.cv10.superior" ] + [ DIGITS_NAMES_ENGLISH[i] + ".cv" + str(i).zfill(2) + ".superior" for i in range(1,10,1)],
    "ss02": [ "zero.cv20.superior" ] + [ DIGITS_NAMES_ENGLISH[i%10] + ".cv" + str(i).zfill(2) + ".superior" for i in range(11,20,1)]
}

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

SS_DIGITS = {
    "ss06": 1,
    "ss07": 7,
    "zero": 0
}
SS_GLYPH_NAMES = {
    "ss06": {
        "digit_def": "one.ss06",
        "digit_ss01": "one.cv01.ss06",
        "digit_ss02": "one.cv11.ss06",
        "sups_def": "one.ss06.superior",
        "sups_ss01": "one.cv01.ss06.superior",
        "sups_ss02": "one.cv11.ss06.superior"
    },
    "ss07": {
        "digit_def": "seven.ss07",
        "digit_ss01": "seven.cv07.ss07",
        "digit_ss02": "seven.cv17.ss07",
        "sups_def": "seven.ss07.superior",
        "sups_ss01": "seven.cv07.ss07.superior",
        "sups_ss02": "seven.cv17.ss07.superior"
    },
    "zero": {
        "digit_def": "zero.zero",
        "digit_ss01": "zero.cv10.zero",
        "digit_ss02": "zero.cv20.zero",
        "sups_def": "zero.zero.superior",
        "sups_ss01": "zero.cv10.zero.superior",
        "sups_ss02": "zero.cv20.zero.superior"
    }
}
SS_LIST = ["ss06","ss07","zero"]

# create a .glif file in the {ufo_dir}/glyphs/{new_file_name} directory
def build_glyph(type: str, ufo_dir: str, glyph_name: str, weight: str, digit_1: int, cv_d1: int, ss_d1: str, digit_2: int, cv_d2: int, ss_d2: str):
    global DIGITS_NAMES_ENGLISH, SUPS_NAMES, FRAC_NAMES, SS_GLYPH_NAMES

    # constants
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
    PNUM_SUPS_KERN = {
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
    DIGITS_HEIGHT = 1480
    SUPS_HEIGHT = 858
    ITALIC_SLANT = 10*pi/180  # slant to the RIGHT in radians (the "*pi/180" converts degrees to radians)

    use_sups = type.split("_")[0] in ["superior", "subscript", "numr", "dnom"] or type in ["circle", "black_circle", "double_circle", "frac"]

    # check if italic
    is_italic = weight[-1] == "i"
    if is_italic:  # remove the "i" at the end
        weight = weight[:-1]

    # get the dependencies and the metrics (apply italic offset here if needed)
    base_1 = ""
    base_2 = ""
    base_1_x_metrics = {}
    base_2_x_metrics = {}
    if ss_d1 == "":  # not use custom ss
        cv_search = ["def", "ss01", "ss02"]
        if use_sups:  # use sups
            base_1 = SUPS_NAMES[cv_search[cv_d1]][digit_1 % 10]
        else:  # use normal numbers
            base_1 = DIGITS_NAMES[cv_search[cv_d1]][digit_1 % 10]
    else:            
        if use_sups:  # use sups
            ss_search = ["sups_def", "sups_ss01", "sups_ss02"]
        else:
            ss_search = ["digit_def", "digit_ss01", "digit_ss02"]
        base_1 = SS_GLYPH_NAMES[ss_d1][ss_search[cv_d1]]
    if ss_d2 == "":  # not use custom ss
        cv_search = ["def", "ss01", "ss02"]
        if use_sups:  # use sups
            base_2 = SUPS_NAMES[cv_search[cv_d2]][digit_2 % 10]
        else:  # use normal numbers
            base_2 = DIGITS_NAMES[cv_search[cv_d2]][digit_2 % 10]
    else:            
        if use_sups:  # use sups
            ss_search = ["sups_def", "sups_ss01", "sups_ss02"]
        else:
            ss_search = ["digit_def", "digit_ss01", "digit_ss02"]
        base_2 = SS_GLYPH_NAMES[ss_d2][ss_search[cv_d2]]
    base_1_x_metrics = get_glyph_metrics(base_1, ufo_dir)
    base_2_x_metrics = get_glyph_metrics(base_2, ufo_dir)
        
    # start to build the xml (output)
    xml_root = ET.Element("glyph", {"name": glyph_name, "format": "2"})
    new_file_name = get_glif_from_name(glyph_name, ufo_dir)

    # draw
    if type.split("_")[0] in ["superior", "subscript", "numr", "dnom"]:  # sups/subs/numr/dnom with eventually pnum/tnum on digit_2 !!!!!! 
        # calculate x offset and width
        x_offset = 0
        width = 0
        if len(type.split("_")) == 1:  # no pnum nor tnum
            x_offset = 0
            width = base_2_x_metrics["glyph_width"]
        elif type.split("_")[1] == "pnum":
            if digit_1 == 1:
                x_offset = PNUM_SUPS_KERN[weight]["1"][0] - base_2_x_metrics["left_kern"]
                width = base_2_x_metrics["raw_width"] + PNUM_SUPS_KERN[weight]["1"][0] + PNUM_SUPS_KERN[weight]["1"][1]
            else:
                x_offset = PNUM_SUPS_KERN[weight]["other"][0] - base_2_x_metrics["left_kern"]
                width = base_2_x_metrics["raw_width"] + PNUM_SUPS_KERN[weight]["other"][0] + PNUM_SUPS_KERN[weight]["other"][1]
        elif type.split("_")[1] == "tnum":
            width = TNUM_WIDTH[weight]
            additional_kern = width - base_2_x_metrics["glyph_width"]
            x_offset = int(base_2_x_metrics["left_kern"] + additional_kern / 2)

        # Add more x offset if italic (none if superior) as we move the glyph below
        if is_italic:
            if type.split("_")[0] == "subscript":
                x_offset -= abs(SUPS_Y - SUBS_Y) / tan(pi/2-ITALIC_SLANT)
            elif type.split("_")[0] == "numr":
                x_offset -= abs(SUPS_Y - NUMR_Y) / tan(pi/2-ITALIC_SLANT)
            elif type.split("_")[0] == "dnom":
                x_offset -= abs(SUPS_Y - DNOM_Y) / tan(pi/2-ITALIC_SLANT)

        # calculate the y metrics
        y_offset = 0  # value for superior
        if type.split("_")[0] == "subscript":
            y_offset = SUBS_Y - SUPS_Y
        elif type.split("_")[0] == "numr":
            y_offset = NUMR_Y - SUPS_Y
        elif type.split("_")[0] == "dnom":
            y_offset = DNOM_Y - SUPS_Y
        
        # build the xml
        ET.SubElement(xml_root, "advance", {"width": str(width)})
        if type == "subscript" and cv_d1 == 0 and cv_d2 == 0 and ss_d1 == "" and ss_d2 == "":
            ET.SubElement(xml_root, "unicode", {"hex": hex(UNICODE_VALUES["subscript"][digit_2]).upper()[2:]})
        xml_outline = ET.SubElement(xml_root, "outline")
        ET.SubElement(xml_outline, "component", {"base": base_2, "xOffset": str(int(x_offset)), "yOffset": str(int(y_offset))})

    elif type in ["circle", "black_circle", "double_circle"]:  # ATTENTION: for 2 digits : dozens = digit_1 and units = digit_2 !!!

        # get the circle
        base_circle = ""
        if type == "circle":
            base_circle = "uni25EF"
        elif type == "black_circle":
            base_circle = "H18533"
        else:  # double_circle
            base_circle = "double_circle_empty"
        base_circle_x_metrics = get_glyph_metrics(base_circle, ufo_dir)
        width = base_circle_x_metrics["glyph_width"]

        # start building the xml (base)
        ET.SubElement(xml_root, "advance", {"width": str(width)})
        if cv_d1 == 0 and cv_d2 == 0 and ss_d1 == "" and ss_d2 == "":
            ET.SubElement(xml_root, "unicode", {"hex": hex(UNICODE_VALUES[type][digit_1 * 10 + digit_2]).upper()[2:]})
        xml_outline = ET.SubElement(xml_root, "outline")
        ET.SubElement(xml_outline, "component", {"base": base_circle})

        # add numbers
        y_offset = CENTER_Y - SUPS_Y
        middle = base_circle_x_metrics["left_kern"] + base_circle_x_metrics["raw_width"] / 2
        if digit_1 == 0:  # one digit : digit_2
            x2 = middle - base_2_x_metrics["glyph_width"] / 2
            if is_italic:
                x2 -= abs(y_offset) / tan(pi/2-ITALIC_SLANT)
            ET.SubElement(xml_outline, "component", {"base": base_2, "xOffset": str(int(x2)), "yOffset": str(int(y_offset))})
        else:  # two digits : dozens = digit_1 and units = digit_2 (!)
            both_digits_length = (base_1_x_metrics["glyph_width"] + base_2_x_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
            x1 = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] * (SUPS_HEIGHT / DIGITS_HEIGHT) 
            x2 = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] * (SUPS_HEIGHT / DIGITS_HEIGHT) - base_2_x_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
            if is_italic:
                x1 -= abs(y_offset) / tan(pi/2-ITALIC_SLANT) * TWO_DIGITS_WIDTH_COEF[weight]
                x2 -= abs(y_offset) / tan(pi/2-ITALIC_SLANT) * TWO_DIGITS_WIDTH_COEF[weight]
            ET.SubElement(xml_outline, "component", {"base": base_1, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x1)), "yOffset": str(int(y_offset))})
            ET.SubElement(xml_outline, "component", {"base": base_2, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x2)), "yOffset": str(int(y_offset))})

    elif type == "parenthezed":
        base_pl = "parenleft"
        base_pr = "parenright"
        base_pl_x_metrics = get_glyph_metrics(base_pl, ufo_dir)
        base_pr_x_metrics = get_glyph_metrics(base_pr, ufo_dir)

        # width calculation
        both_digits_length = (base_1_x_metrics["glyph_width"] + base_2_x_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
        width = (base_pl_x_metrics["raw_width"] + base_pr_x_metrics["raw_width"]) * TWO_DIGITS_WIDTH_COEF[weight] + both_digits_length - TWO_DIGITS_OVERLAP[weight]

        ET.SubElement(xml_root, "advance", {"width": str(width)})
        if cv_d1 == 0 and cv_d2 == 0 and ss_d1 == "" and ss_d2 == "":
            ET.SubElement(xml_root, "unicode", {"hex": hex(UNICODE_VALUES[type][digit_1 * 10 + digit_2]).upper()[2:]})
        xml_outline = ET.SubElement(xml_root, "outline")

        xl = DEFAULT_KERN[weight] - base_pl_x_metrics["left_kern"] * TWO_DIGITS_WIDTH_COEF[weight]
        xr = width - DEFAULT_KERN[weight] - (base_pr_x_metrics["left_kern"] + base_pr_x_metrics["raw_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
        ET.SubElement(xml_outline, "component", {"base": base_pl, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(xl)), "yOffset": "0"})
        ET.SubElement(xml_outline, "component", {"base": base_pr, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(xr)), "yOffset": "0"})

        if digit_1 == 0:
            x2 = DEFAULT_KERN[weight] + ((width - 2*DEFAULT_KERN[weight]) - base_2_x_metrics["glyph_width"]) * 0.5
            ET.SubElement(xml_outline, "component", {"base": base_2, "xOffset": str(int(x2)), "yOffset": "0"})
        else:
            middle = width / 2
            x1 = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2
            x2 = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2 - base_2_x_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
            ET.SubElement(xml_outline, "component", {"base": base_1, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x1)), "yOffset": "0"})
            ET.SubElement(xml_outline, "component", {"base": base_2, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x2)), "yOffset": "0"})
    
    elif type == "full_stop":
        base_period = "period"
        base_period_x_metrics = get_glyph_metrics(base_period, ufo_dir)

        # width calculation
        both_digits_length = (base_1_x_metrics["glyph_width"] + base_2_x_metrics["glyph_width"]) * TWO_DIGITS_WIDTH_COEF[weight]
        width = DEFAULT_KERN[weight] / 2 + both_digits_length + base_period_x_metrics["raw_width"] + DEFAULT_KERN[weight] - TWO_DIGITS_OVERLAP[weight]

        ET.SubElement(xml_root, "advance", {"width": str(width)})
        if cv_d1 == 0 and cv_d2 == 0 and ss_d1 == "" and ss_d2 == "":
            ET.SubElement(xml_root, "unicode", {"hex": hex(UNICODE_VALUES[type][digit_1 * 10 + digit_2]).upper()[2:]})
        xml_outline = ET.SubElement(xml_root, "outline")

        xp = width - base_period_x_metrics["left_kern"] - base_period_x_metrics["raw_width"] - DEFAULT_KERN[weight]
        ET.SubElement(xml_outline, "component", {"base": base_period, "xOffset": str(int(xp)), "yOffset": "0"})

        middle = (width - base_period_x_metrics["glyph_width"]) / 2 + DEFAULT_KERN[weight]
        if digit_1 == 0:
            x2 = middle - base_2_x_metrics["glyph_width"] / 2 + DEFAULT_KERN[weight]
            ET.SubElement(xml_outline, "component", {"base": base_2, "xOffset": str(int(x2)), "yOffset": "0"})
        else:
            x1 = middle - both_digits_length / 2 + TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2
            x2 = middle + both_digits_length / 2 - TWO_DIGITS_OVERLAP[weight] * TWO_DIGITS_WIDTH_COEF[weight] / 2 - base_2_x_metrics["glyph_width"] * TWO_DIGITS_WIDTH_COEF[weight]
            ET.SubElement(xml_outline, "component", {"base": base_1, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x1)), "yOffset": "0"})
            ET.SubElement(xml_outline, "component", {"base": base_2, "xScale": str(TWO_DIGITS_WIDTH_COEF[weight]), "xOffset": str(int(x2)), "yOffset": "0"})
    
    elif type == "frac":  # numr = digit_1, dnom = digit_2. For no dnom, set digit_2 to zero. For 1/10 in dnom, set digit_1=1 and digit_2=10
        base_frac = "fraction"
        base_frac_x_metrics = get_glyph_metrics(base_frac, ufo_dir)

        if digit_2 == 10:
            # based on where the denominators are located
            width = base_frac_x_metrics["left_kern"] + base_frac_x_metrics["raw_width"]
            width -= base_1_x_metrics["glyph_width"] / 2
            width += base_1_x_metrics["glyph_width"] - TWO_DIGITS_OVERLAP[weight]
            width += base_2_x_metrics["left_kern"] + base_2_x_metrics["raw_width"] + DEFAULT_KERN[weight]
        else:  # denominator = 0 => same than normal fractions
            width = base_frac_x_metrics["glyph_width"]

        # unicode value
        ET.SubElement(xml_root, "advance", {"width": str(int(width))})
        if cv_d1 == 0 and cv_d2 == 0 and ss_d1 == "" and ss_d2 == "":
            ET.SubElement(xml_root, "unicode", {"hex": hex(UNICODE_VALUES["frac"][digit_2][digit_1]).upper()[2:]})
        xml_outline = ET.SubElement(xml_root, "outline")

        # fractional bar
        ET.SubElement(xml_outline, "component", {"base": base_frac, "xOffset": "0", "yOffset": "0"})

        # numr
        digit_1_middle = base_frac_x_metrics["left_kern"] - DEFAULT_KERN[weight] * 1.5
        x1 = digit_1_middle - base_1_x_metrics["glyph_width"] / 2
        y1 = NUMR_Y - SUPS_Y
        if is_italic:
            x1 -= abs(y1) / tan(pi/2-ITALIC_SLANT)
        ET.SubElement(xml_outline, "component", {"base": base_1, "xOffset": str(int(x1)), "yOffset": str(int(y1))})

        # dnom
        y2 = DNOM_Y - SUPS_Y
        if digit_2 == 0:
            pass
        elif digit_2 == 10:
            digit_21_middle = base_frac_x_metrics["left_kern"] + base_frac_x_metrics["raw_width"]
            x21 = digit_21_middle - base_1_x_metrics["glyph_width"] / 2
            x22 = x21 + base_1_x_metrics["glyph_width"] - base_2_x_metrics["left_kern"] - TWO_DIGITS_OVERLAP[weight]
            if is_italic:
                x21 -= abs(y2) / tan(pi/2-ITALIC_SLANT) 
                x22 -= abs(y2) / tan(pi/2-ITALIC_SLANT)
            ET.SubElement(xml_outline, "component", {"base": base_1, "xOffset": str(int(x21)), "yOffset": str(int(y2))})
            ET.SubElement(xml_outline, "component", {"base": base_2, "xOffset": str(int(x22)), "yOffset": str(int(y2))})
        else:
            digit_2_middle = base_frac_x_metrics["left_kern"] + base_frac_x_metrics["raw_width"] + DEFAULT_KERN[weight] * 1.5
            x2 = digit_2_middle - base_2_x_metrics["glyph_width"] / 2
            if is_italic:
                x2 -= abs(y2) / tan(pi/2-ITALIC_SLANT)
            ET.SubElement(xml_outline, "component", {"base": base_2, "xOffset": str(int(x2)), "yOffset": str(int(y2))})

    # save
    tree = ET.ElementTree(xml_root)
    tree.write(new_file_name, encoding="UTF-8", xml_declaration=True)
    #print(f"{glyph_name}, {base_1}, {base_2}")

    # Unlink reference for black circles
    if type == "black_circle":
        unlink_references(glyph_name, ufo_dir)

    return

# create some glif files inside a ufo
def build_weight(weight: str, ufo_dir: str):
    # sups / subs / numr / dnom / numerics signs such as "(1)"" or "2."
    SS_LIST = [  # ss name, digits affected
        ("ss06", 1),
        ("ss07", 7),
        ("zero", 0)
    ]
    SS_LIST_NAMES = [ ss_data[0] for ss_data in SS_LIST ]
    SS_LIST_DIGITS = [ ss_data[1] for ss_data in SS_LIST ]
    
    glyphs_count = 0
    for i in range(100):
        # calculate the digits (0-9)
        d1 = i // 10
        d2 = i % 10
        # find applicable cv
        cv_suffix_list = [""]
        cv_values_list = [(0,0)]
        for c1 in range(3):
            for c2 in range(3):
                if c1 == 0 and c2 == 0:
                    pass
                elif d1 == d2:  # 2 same digits
                    if c2 == 0:
                        cv_suffix_list.append(f".cv{str((c1 - 1) * 10 + d1).zfill(2) if d1 != 0 else str(c1 * 10)}")
                        cv_values_list.append((c1, c1))
                elif c1 != 0 and c2 == 0:  # digit 1 only
                    cv_suffix_list.append(f".cv{str((c1 - 1) * 10 + d1).zfill(2) if d1 != 0 else str(c1 * 10)}")
                    cv_values_list.append((c1, 0))
                elif c1 == 0 and c2 != 0:  # digit 2 only
                    cv_suffix_list.append(f".cv{str((c2 - 1) * 10 + d2).zfill(2) if d2 != 0 else str(c2 * 10)}")
                    cv_values_list.append((0, c2))
                else:  # both digits
                    cv_d1 = (c1 - 1) * 10 + d1 if d1 != 0 else c1 * 10
                    cv_d2 = (c2 - 1) * 10 + d2 if d2 != 0 else c2 * 10
                    if cv_d1 < cv_d2:
                        cv_suffix_list.append(f".cv{str(cv_d1).zfill(2)}.cv{str(cv_d2).zfill(2)}")
                    else:
                        cv_suffix_list.append(f".cv{str(cv_d2).zfill(2)}.cv{str(cv_d1).zfill(2)}")
                    cv_values_list.append((c1, c2))
        # find applicable ss
        ss_suffix_list = [""]
        ss_values_list = [("","")]
        if d1 == d2 and d2 in SS_LIST_DIGITS:  # 2 same digits
            ss_suffix_list.append("." + SS_LIST_NAMES[SS_LIST_DIGITS.index(d2)])
            ss_values_list.append((SS_LIST_NAMES[SS_LIST_DIGITS.index(d2)], SS_LIST_NAMES[SS_LIST_DIGITS.index(d2)]))
        else:
            if d1 in SS_LIST_DIGITS:  # 2 differents digits
                ss_suffix_list.append("." + SS_LIST_NAMES[SS_LIST_DIGITS.index(d1)])
                ss_values_list.append((SS_LIST_NAMES[SS_LIST_DIGITS.index(d1)], ""))
            if d2 in SS_LIST_DIGITS:
                ss_suffix_list.append("." + SS_LIST_NAMES[SS_LIST_DIGITS.index(d2)])
                ss_values_list.append(("", SS_LIST_NAMES[SS_LIST_DIGITS.index(d2)]))
            if d1 in SS_LIST_DIGITS and d2 in SS_LIST_DIGITS:
                ss_index_d1 = SS_LIST_DIGITS.index(d1)
                ss_index_d2 = SS_LIST_DIGITS.index(d2)
                if ss_index_d1 < ss_index_d2:
                    ss_suffix_list.append(f".{SS_LIST_NAMES[ss_index_d1]}.{SS_LIST_NAMES[ss_index_d2]}")
                else:
                    ss_suffix_list.append(f".{SS_LIST_NAMES[ss_index_d2]}.{SS_LIST_NAMES[ss_index_d1]}")
                ss_values_list.append((SS_LIST_NAMES[ss_index_d1], SS_LIST_NAMES[ss_index_d2]))
        # generate the glyphs
        ss_index = 0
        for ss_suffix in ss_suffix_list:
            cv_index = 0
            for cv_suffix in cv_suffix_list:
                # sups / subs / numr / dnom (on d2)
                if i == 0 or (i != 0 and i < 10 and cv_values_list[cv_index][0] == 0 and ss_values_list[ss_index][0] == ""):
                    for type in ["superior", "subscript", "numr", "dnom"]:
                        if not(type == "superior"):
                            build_glyph(type, ufo_dir, f"{DIGITS_NAMES_ENGLISH[i]}{cv_suffix}{ss_suffix}.{type}", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                            glyphs_count += 1
                        build_glyph(type + "_pnum", ufo_dir, f"{DIGITS_NAMES_ENGLISH[i]}{cv_suffix}{ss_suffix}.{type}.pnum", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        build_glyph(type + "_tnum", ufo_dir, f"{DIGITS_NAMES_ENGLISH[i]}{cv_suffix}{ss_suffix}.{type}.tnum", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        glyphs_count += 2
                # circled numbers etc. (d1 = dozens, d2 = units)
                if i == 0 or (i != 0 and i < 10 and cv_values_list[cv_index][0] == 0 and ss_values_list[ss_index][0] == ""):  # one digit (0-9)
                    build_glyph("circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                    build_glyph("black_circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["black_circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                    glyphs_count += 2
                    if i >= 1:
                        build_glyph("parenthezed", ufo_dir, f"uni{str(hex(UNICODE_VALUES["parenthezed"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        build_glyph("full_stop", ufo_dir, f"uni{str(hex(UNICODE_VALUES["full_stop"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        build_glyph("double_circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["double_circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, 0, 0, "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        glyphs_count += 3
                elif i >= 10 and i <= 20:  # two digits
                    if d1 != d2:  # disable building for 2 same digits that are the same if digit one has a non-null cv or ss to avoid duplicates 
                        build_glyph("circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        build_glyph("black_circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["black_circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        glyphs_count += 2
                        if i >= 1: # 1-20
                            build_glyph("parenthezed", ufo_dir, f"uni{str(hex(UNICODE_VALUES["parenthezed"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                            build_glyph("full_stop", ufo_dir, f"uni{str(hex(UNICODE_VALUES["full_stop"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                            glyphs_count += 2
                    elif d1 == d2:
                        build_glyph("circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        build_glyph("black_circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["black_circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        build_glyph("parenthezed", ufo_dir, f"uni{str(hex(UNICODE_VALUES["parenthezed"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        build_glyph("full_stop", ufo_dir, f"uni{str(hex(UNICODE_VALUES["full_stop"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        glyphs_count += 4

                    if i == 10:  # 10
                        build_glyph("double_circle", ufo_dir, f"uni{str(hex(UNICODE_VALUES["double_circle"][d1 * 10 + d2])).upper()[2:]}{cv_suffix}{ss_suffix}", weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        glyphs_count += 1
                # fractions (digit_1 = numerator, digits_2 = denominator)
                if i == 1:  # as 0/1 doesn't exists, let's put the 1/10 here
                    glyph_name = ""
                    if f"1/10" in FRAC_NAMES:
                        glyph_name = FRAC_NAMES["1/10"]
                    else:
                        glyph_name = f"uni{str(hex(UNICODE_VALUES["frac"][10][1])).upper()[2:]}"
                    build_glyph("frac", ufo_dir, f"uni{str(hex(UNICODE_VALUES["frac"][10][1])).upper()[2:]}" + cv_suffix + ss_suffix, weight, 1, cv_values_list[cv_index][1], ss_values_list[ss_index][1], 10, cv_values_list[cv_index][0], ss_values_list[ss_index][0])
                    glyphs_count += 1
                    #print(str(i).zfill(2), "frac", ufo_dir, glyph_name + cv_suffix + ss_suffix, weight, 1, cv_values_list[cv_index][1], ss_values_list[ss_index][1] if ss_values_list[ss_index][1] == "" else "-", 10, cv_values_list[cv_index][0], ss_values_list[ss_index][0] if ss_values_list[ss_index][0] == "" else "-")
                elif UNICODE_VALUES["frac"][d2][d1] != -1:
                    glyph_name = ""
                    if f"{d1}/{d2}" in FRAC_NAMES:
                        glyph_name = FRAC_NAMES[f"{d1}/{d2}"]
                    else:
                        glyph_name = f"uni{str(hex(UNICODE_VALUES["frac"][d2][d1])).upper()[2:]}"
                    if d2 == 0:  # invisible dnom
                        if cv_values_list[cv_index][1] == 0 and ss_values_list[ss_index][1] == "":
                            build_glyph("frac", ufo_dir, glyph_name + cv_suffix + ss_suffix, weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], 0, 0, "")
                            glyphs_count += 1
                    else:
                        build_glyph("frac", ufo_dir, glyph_name + cv_suffix + ss_suffix, weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0], d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1])
                        glyphs_count += 1
                    #print(str(i).zfill(2), "frac", ufo_dir, glyph_name + cv_suffix + ss_suffix, weight, d1, cv_values_list[cv_index][0], ss_values_list[ss_index][0] if ss_values_list[ss_index][0] == "" else "", d2, cv_values_list[cv_index][1], ss_values_list[ss_index][1] if ss_values_list[ss_index][1] == "" else "-")
                cv_index += 1
            ss_index += 1
    print(f"Done building glyphs for weight {weight} ({glyphs_count} generated)")
    return

def main():
    if len(sys.argv) < 3:
        print(f"{sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <weight> <ufo_directory>")
    else:
        build_weight(sys.argv[1], sys.argv[2])
        print("Done.")

if __name__ == "__main__":
    main()
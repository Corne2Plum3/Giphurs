import sys
import xml.etree.ElementTree as ET

def get_glif_from_name(glyph_name, ufo_dir):
    # remove "/" at the end of the ufo_dir if here
    if ufo_dir[-1] == "/" or ufo_dir[-1] == "\\":
        ufo_dir = ufo_dir[:-1]

    # open contents.plist
    tree = ET.parse(f"{ufo_dir}/glyphs/contents.plist")
    glyphs_dict = tree.getroot().find("dict")

    # find glyph_name
    key_list = glyphs_dict.findall("key")
    string_list = glyphs_dict.findall("string")
    index = 0
    glyph_found = False
    while glyph_found == False and index < len(key_list):
        if key_list[index].text == glyph_name:
            glyph_found = True
        else:
            index += 1

    # return
    if glyph_found:
        return f"{ufo_dir}/glyphs/{string_list[index].text}"
    else:
        print(f"{sys.argv[0]}: WARNING: Glyph not found: {glyph_name}")
        return ""

"""
This script will force the UFO to flatten components when compiled.
Fixes Fontbakery com.google.fonts/check/glyf_nested_components FAIL [code: found-nested-components]
"""

import sys
from xml.etree import ElementTree

def add_flattenComponents_flag_to_lib_plist(ufo_file_path):

    # lib.plist header (const str)
    lib_plist_headers = """<?xml version='1.0' encoding='UTF-8'?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    """

    # what we want to add in lib.plist (2 successive nodes)
    lib_plist_dict_additions_1 = ElementTree.XML("\n<key>com.github.googlei18n.ufo2ft.filters</key>\n")
    lib_plist_dict_additions_2 = ElementTree.XML("<array>\n\t<dict>\n\t\t<key>name</key>\n\t\t<string>flattenComponents</string>\n\t\t<key>pre</key>\n\t\t<integer>1</integer>\n\t</dict>\n</array>\n")

    # adding the nodes
    lib_plist_filename = f"{ufo_file_path}/lib.plist"
    lib_plist_root = ElementTree.parse(lib_plist_filename).getroot()  # root is <plist version="1.0">
    lib_plist_additions_parent = lib_plist_root.find("dict")
    lib_plist_additions_parent.insert(0, lib_plist_dict_additions_1)
    lib_plist_additions_parent.insert(1, lib_plist_dict_additions_2)
    # note: new nodes added doesn't add a newline at their end,
    # ruining a bit the formatting, but seems to not be an issue

    # write xml file
    new_xml_bitstream = ElementTree.tostring(lib_plist_root)
    with open(lib_plist_filename, "wb") as f:
        f.write(lib_plist_headers.encode("utf-8"))  # add headers
        f.write(new_xml_bitstream)  # add xml content


def main():
    assert (len(sys.argv) >= 2), f"{sys.argv[0]}: Too few arguments.\nUsage: python3 {sys.argv[0]} <ufo_file>"
    print(f"{sys.argv[0]}: Adding 'flattenComponents' setting in {sys.argv[1]}/lib.plist")
    add_flattenComponents_flag_to_lib_plist(sys.argv[1])
    print(f"{sys.argv[0]}: Done.")


if __name__ == "__main__":
    main()

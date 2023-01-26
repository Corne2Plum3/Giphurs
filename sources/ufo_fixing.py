import sys
from xml.etree import ElementTree

# lib.plist header (const str)
lib_plist_headers = """<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
"""

if len(sys.argv) <= 1:  # too few arguments

    print(f"{sys.argv[0]}: Too few arguments.\nUsage: python3 {sys.argv[0]} <ufo_file>")

else:

    # FORCE THE UFO FILE TO FLATTEN COMPONENTS (fixes an issue with ttf files)

    # what we want to add in lib.plist (2 successive nodes)
    lib_plist_dict_additions_1 = ElementTree.XML("""
    <key>com.github.googlei18n.ufo2ft.filters</key>\n
    """)

    lib_plist_dict_additions_2 = ElementTree.XML("""
    <array>
      <dict>
        <key>name</key>
        <string>flattenComponents</string>
        <key>pre</key>
        <integer>1</integer>
      </dict>
    </array>
    """)

    # adding the nodes
    lib_plist_filename = f"{sys.argv[1]}/lib.plist"
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
    
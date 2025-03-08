"""
Set the bit 7 ("use typo metrics") of fsSelection in an ufo file.

Note: Doesn't do anything if openTypeOS2Selection is already here, regardless its value
"""

import sys
import xml.etree.ElementTree as ET

def main():
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory>")
    else:
        # load the file and find the root
        tree = ET.parse(f"{sys.argv[1]}/fontinfo.plist")

        # check if it is already set and remove it
        xml_key_list = tree.getroot().find("dict").findall("key")
        key_list = []

        for element in xml_key_list:
            key_list.append(element.text)
        if not "openTypeOS2Selection" in key_list:
            new_key = ET.Element("key", {})
            new_key.text = "openTypeOS2Selection"
            tree.getroot().find("dict").append(new_key)
            new_array = ET.Element("array", {})
            new_integer = ET.Element("integer", {})
            new_integer.text = "7"
            new_array.append(new_integer)
            tree.getroot().find("dict").append(new_array)
            # save
            tree.write(f"{sys.argv[1]}/fontinfo.plist", encoding="UTF-8", xml_declaration=True)

    print("Done.")

if __name__ == "__main__":
    main()
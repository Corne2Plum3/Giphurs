"""
Set the bit 7 ("use typo metrics") of fsSelection in an ufo file.

Note: Doesn't do anything if openTypeOS2Selection is already here, regardless its value
"""

from logger import configure_logging
import sys
import xml.etree.ElementTree as ET

logger = configure_logging()

def use_typo_metrics(ufo_file: str) -> int:
    # load the file and find the root
    tree = ET.parse(f"{ufo_file}/fontinfo.plist")

    # check if it is already set and remove it
    xml_dict = tree.getroot().find("dict")
    if xml_dict is None:
        logger.error('Element <dict> not found.')
        return 1
    xml_key_list = xml_dict.findall("key")

    key_list: list[str] = []
    for element in xml_key_list:
        if element.text is not None:
            key_list.append(element.text)

    if "openTypeOS2Selection" in key_list:
        xml_openTypeOS2Selection: ET.Element[str] | None = xml_dict.find('openTypeOS2Selection')
        if xml_openTypeOS2Selection is not None:
            if xml_openTypeOS2Selection.text != '7':
                logger.warning(f'Overwriting openTypeOS2Selection: {xml_openTypeOS2Selection.text} -> 7...')
            else:
                logger.info(f'Overwriting openTypeOS2Selection: {xml_openTypeOS2Selection.text} -> 7...')
            xml_openTypeOS2Selection.text = "7"
    else:
        logger.info(f'Adding openTypeOS2Selection with value 7...')
        new_key = ET.Element("key", {})
        new_key.text = "openTypeOS2Selection"
        xml_dict.append(new_key)
        new_array = ET.Element("array", {})
        new_integer = ET.Element("integer", {})
        new_integer.text = "7"
        new_array.append(new_integer)
        xml_dict.append(new_array)

    # save
    logger.info(f'Writing into "{ufo_file}/fontinfo.plist"...')
    tree.write(f"{ufo_file}/fontinfo.plist", encoding="UTF-8", xml_declaration=True)
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory>")
        exit(1)
    exit(use_typo_metrics(sys.argv[1]))
    
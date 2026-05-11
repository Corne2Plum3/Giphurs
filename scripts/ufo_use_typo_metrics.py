"""
Set the bit 7 ("use typo metrics") of fsSelection in an ufo file.

Note: Doesn't do anything if openTypeOS2Selection is already here, regardless its value
"""

from logger import configure_logging
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

logger = configure_logging(__name__)

def use_typo_metrics(ufo_file: Path) -> int:
    """
    Set the openTypeOS2Selection value inside 
    """

    # load the file and find the root
    logger.debug(f'Parsing "{ufo_file}/fontinfo.plist"...')
    try:
        tree = ET.parse(f"{ufo_file}/fontinfo.plist")
    except Exception as err:
        logger.error(f'Failed to parse "{ufo_file}/fontinfo.plist": {err}')
        return 1

    # check if it is already set and remove it
    try:
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
    except Exception as err:
        logger.error(f'Internal error when trying to set openTypeOS2Selection to 7: {err}')
        return 1

    # save
    logger.info(f'Writing into "{ufo_file}/fontinfo.plist"...')
    try:
        tree.write(f"{ufo_file}/fontinfo.plist", encoding="UTF-8", xml_declaration=True)
    except Exception as err:
        logger.error(f'Failed to write into "{ufo_file}/fontinfo.plist": {err}')
        return 1
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory>")
        exit(1)
    exit(use_typo_metrics(Path(sys.argv[1])))
    
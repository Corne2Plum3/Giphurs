"""
Set the bit 7 ("use typo metrics") of fsSelection in an ufo file.

Can be used directly on a terminal or by using the use_typo_metrics() function in a Python script.
"""

from logger import configure_logging
from pathlib import Path
import plistlib
import sys
from typing import Any


logger = configure_logging(__name__)

def use_typo_metrics(ufo_dir: Path) -> int:
    """
    Set the openTypeOS2Selection value inside a UFO file. Writes into the fontinfo.plist file of the UFO.

    This function handles the logging.

    Args:
        ufo_dir: UFO to modify
    Returns:
        `0` if success, non-zero otherwise
    """

    # Read file
    logger.info(f'Working on "{ufo_dir}"...')
    plist_raw_content: Any
    try:
        with open(ufo_dir / 'fontinfo.plist', 'rb') as f:
            plist_raw_content = plistlib.load(f)
    except Exception as err:
        logger.critical(f'Failed to read "{ufo_dir / 'fontinfo.plist'}": {err}')
        return 1
    
    if not isinstance(plist_raw_content, dict):
        logger.critical(f'Failed to set version on "{ufo_dir / 'fontinfo.plist'}": a dict was expected, got {type(plist_raw_content)}.')
        return 1
   
    plist_dict: dict[str, Any] = plist_raw_content  # pyright: ignore[reportUnknownVariableType]

    # Early exit if nothing to do
    if 'openTypeOS2Selection' in plist_dict and 7 in plist_dict['openTypeOS2Selection']:
        logger.info(f'Value 7 is already in openTypeOS2Selection.')
        return 0
    
    # Set or add if missing
    if 'openTypeOS2Selection' in plist_dict:
        plist_dict['openTypeOS2Selection'].append(7)
    else:
        plist_dict['openTypeOS2Selection'] = [7]

    # Save
    logger.verbose(f'Writing into "{ufo_dir / 'fontinfo.plist'}"...')  # pyright: ignore[reportUnknownMemberType]
    try:
        with open(ufo_dir / 'fontinfo.plist', 'wb') as f:
            plistlib.dump(plist_dict, f, fmt=plistlib.FMT_XML)
    except Exception as err:
        logger.critical(f'Failed to write into "{ufo_dir / 'fontinfo.plist'}": {err}')
        return 1

    logger.success(f'The value 7 has been added to openTypeOS2Selection')  # pyright: ignore[reportUnknownMemberType]
    return 0

if __name__ == "__main__":
    # Read parameters
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <ufo_directory>")
        exit(1)
    
    # Execute
    exit_code: int = use_typo_metrics(Path(sys.argv[1]))
    
    # Exit
    exit(exit_code)
    
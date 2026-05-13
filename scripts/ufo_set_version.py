"""
Script to set the version of the font inside an UFO file.

Can be used directly on a terminal or by using the set_version() function in a Python script.
"""

from logger import configure_logging
from pathlib import Path
import plistlib
import sys
from typing import Any


logger = configure_logging()

def set_version(version_string: str, ufo_dir: Path) -> int:
    '''
    Set the version value of a UFO. Writes into the fontinfo.plist file of the UFO.

    Version string must be a decimal numbe, for example "2", "2.010" or "2.0.1" (which is the same as "2.010").
    The version string written inside the UFO will be in the form of a decimal number with at least 3 decimals.

    This function handles the logging.

    Args:
        version_string: version of the font value to apply
        ufo_dir: UFO to modify
    Returns:
        `0` if success, non-zero otherwise
    '''

    # Read version string
    version_major: str = version_string.split('.', maxsplit=1)[0]
    version_minor: str
    if len(version_string.split('.', maxsplit=1)) < 2:
        version_minor = '000'
    else:
        version_minor = version_string.split('.', maxsplit=1)[1].replace('.', '')
        while len(version_minor) < 3:
            version_minor += '0'
    if not version_major.isnumeric() or not version_minor.isnumeric():
        logger.critical(f'Invalid version_string value: "{version_string}".')
        return 1

    # Read file
    logger.info(f'Setting font version value of "{ufo_dir}" to {version_major}.{version_minor}')
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

    # Set (add field if missing)
    plist_dict['openTypeNameVersion'] = f'Version {version_major}.{version_minor}'
    plist_dict['versionMajor'] = version_major
    plist_dict['versionMinor'] = version_minor

    # Save
    logger.verbose(f'Writing into "{ufo_dir / 'fontinfo.plist'}"...')  # pyright: ignore[reportUnknownMemberType]
    try:
        with open(ufo_dir / 'fontinfo.plist', 'wb') as f:
            plistlib.dump(plist_dict, f, fmt=plistlib.FMT_XML)
    except Exception as err:
        logger.critical(f'Failed to write into "{ufo_dir / 'fontinfo.plist'}": {err}')
        return 1

    logger.success(f'UFO "{ufo_dir}" font version has been set to {version_major}.{version_minor}')  # pyright: ignore[reportUnknownMemberType]
    return 0


if __name__ == '__main__':    
    # Read parameters
    if len(sys.argv) < 3:
        print(f"ERROR: {sys.argv[0]}: Not enough parameters.")
        print(f"Usage: {sys.argv[0]} <VERSION_STRING> <UFO_DIR>")
        print("* VERSION_STRING: version of the font value to apply")
        print("* UFO_DIR: UFO to modify.")
    version_string: str = sys.argv[1]
    ufo_dir: Path = Path(sys.argv[2])
    
    # Execute
    exit_code = set_version(version_string, ufo_dir)
    
    # Exit
    exit(exit_code)

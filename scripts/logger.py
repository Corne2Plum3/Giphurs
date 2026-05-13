'''Logging configuration so it's used in all scripts.'''

import coloredlogs  # pyright: ignore[reportMissingTypeStubs]
from dotenv import load_dotenv
import os
from pathlib import Path
from verboselogs import VerboseLogger  # pyright: ignore[reportMissingTypeStubs]
import logging


load_dotenv()

# Where to store the logs from this logger
FONT_LOGS: Path = Path(os.environ.get('FONT_LOGS', 'logs/font.log'))


def configure_logging() -> VerboseLogger:
    """Initialize Colored Logging with a consistent config"""
    if not FONT_LOGS.exists():
        os.mkdir(FONT_LOGS.parents[0])

    logging.basicConfig(
        filename=FONT_LOGS,  # name of the log file
        level=logging.DEBUG,  # level of the log
        format='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s'  # log format
    )
    
    coloredlogs.install()  # pyright: ignore[reportUnknownMemberType]

    logger: VerboseLogger = VerboseLogger('logger')  # Get a logger instance
    return logger

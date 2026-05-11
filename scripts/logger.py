'''Logging configuration so it's used in all scripts.'''

import coloredlogs  # pyright: ignore[reportMissingTypeStubs]
from verboselogs import VerboseLogger  # pyright: ignore[reportMissingTypeStubs]

def configure_logging(name: str | None = None, level: str='DEBUG') -> VerboseLogger:
    """Initialize Colored Logging with a consistent config"""            
    coloredlogs.install(   # pyright: ignore[reportUnknownMemberType]
        level=level,
        fmt='%(asctime)s.%(msecs)03d %(programname)s %(levelname)s %(message)s',  # You can also define custom format
    )  
    logger: VerboseLogger = VerboseLogger(name)  # Get a logger instance
    return logger

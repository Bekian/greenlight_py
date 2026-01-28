# this module declares fastapi dependencies that are used throughout the app,
# instead of the struct model used in the book

import logging
from typing import Annotated

from fastapi import Depends

from .config import Config, cfg, logger


# Direct dependencies - no Request needed
def get_config() -> Config:
    return cfg


def get_logger() -> logging.Logger:
    return logger


# Type aliases for convenience
AppConfig = Annotated[Config, Depends(get_config)]
AppLogger = Annotated[logging.Logger, Depends(get_logger)]

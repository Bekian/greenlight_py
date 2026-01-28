import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

version = "1.0.0"  # static for now, this will be managed by version control


# this auto-loaded config is used instead of arg flags
class Config(BaseSettings):
    port: int = 4000  # server port
    env: str = "development"  # environment (development|testing|production)
    version: str = version

    model_config = {
        "env_prefix": "APP_",  # All app env vars start with APP_
        "env_file": ".env",  # Load from .env file
        "case_sensitive": False,  # APP_PORT or APP_port both work
    }


# Setup logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


load_dotenv()
cfg = Config()
logger = setup_logging()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(addr)s - %(env)s - %(name)s",
)

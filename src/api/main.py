import logging
from contextlib import asynccontextmanager

import healthcheck
import movies
from dotenv import load_dotenv
from fastapi import FastAPI
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


# global dependency injection object for app related state
# this is passed to a FastAPI state object
class Application:
    def __init__(self, config: Config, logger: logging.Logger):
        self.config = config
        self.logger = logger


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
app_state = Application(config=cfg, logger=logger)


# setup/graceful shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # set the values for the startup log
    local_cfg = app.state.app.config
    message = "starting server"
    app_state.logger.info(message, extra={"addr": local_cfg.port, "env": local_cfg.env})

    # run the app
    yield

    # graceful shutdown
    message = "shutting down server"
    app_state.logger.info(message)


# add the lifecycle wrapper to the fastapi app
app = FastAPI(lifespan=lifespan)
# store the app state in the app object for dependency injection
app.state.app = app_state
app.include_router(movies.router)
app.include_router(healthcheck.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=app.state.app.config.port,
        reload=True if app.state.app.config.env == "development" else False,
        timeout_keep_alive=60,
        log_config=None,
    )

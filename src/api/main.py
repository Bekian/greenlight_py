import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.internal.dependency import get_config, get_logger

from . import healthcheck, movies


# setup/graceful shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger = get_logger()
    app_config = get_config()
    # startup log message
    app_logger.info(
        "starting server", extra={"addr": app_config.port, "env": app_config.env}
    )

    # run the app
    yield

    # graceful shutdown
    app_logger.info("shutting down server")


# add the lifecycle wrapper to the fastapi app
app = FastAPI(lifespan=lifespan)
app.include_router(movies.router)
app.include_router(healthcheck.router)


async def main():
    app_config = get_config()
    # we use this pattern instead of uvicorn.run,
    # because it's more akin to what will be running at work,
    # work uses 2 indepenent servers for main and healthcheck
    config = uvicorn.Config(
        "src.api.main:app",
        port=app_config.port,
        log_config=None,
        reload=True if app_config.env == "development" else False,
        timeout_keep_alive=60,
        host="0.0.0.0",
    )
    server = uvicorn.Server(config)
    await asyncio.gather(server.serve())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")

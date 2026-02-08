import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.errors import general_exception_handler, http_exception_handler
from src.api.middleware import RateLimitSizeMiddleware
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
# the "fastapi way" is to use a decorator but i prefer this method, and its closer to what the book does
# also passing the app instance around is not ideal
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
# this replaces the `recoverPanic` handler from the book
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(RateLimitSizeMiddleware, max_bytes=1_048_576)

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

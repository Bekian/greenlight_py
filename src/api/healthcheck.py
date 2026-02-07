from fastapi import APIRouter, Request

from src.internal.dependency import AppConfig

router = APIRouter(prefix="/v1py/healthcheck", tags=["health"])


@router.get("")
async def healthcheck(request: Request, app_config: AppConfig):
    # the book uses an envelope wrapper here, i'll add that if this healthcheck requires it later
    # the book also handles a potential error here when marshalling json,
    # this is handled for us so we're not gonna do that
    return {
        "status": "available",
        "system_info": {
            "environment": app_config.env,
            "version": app_config.version,
        },
    }

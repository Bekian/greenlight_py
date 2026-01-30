from fastapi import APIRouter, Request

from src.internal.dependency import AppConfig

router = APIRouter(prefix="/v1py/healthcheck", tags=["health"])


@router.get("")
async def healthcheck(request: Request, app_config: AppConfig):
    # the book uses an envelope wrapper here, i'll add that if this healthcheck requires it later
    return {
        "status": "available",
        "system_info": {
            "environment": app_config.env,
            "version": app_config.version,
        },
    }

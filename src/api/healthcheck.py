from fastapi import APIRouter, Request

from src.internal.dependency import AppConfig

router = APIRouter(prefix="/v1py/healthcheck", tags=["health"])


@router.get("")
async def healthcheck(request: Request, app_config: AppConfig):
    return {
        "data": {
            "status": "available",
            "environment": app_config.env,
            "version": app_config.version,
        }
    }

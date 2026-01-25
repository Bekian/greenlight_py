from fastapi import APIRouter, Request

router = APIRouter(prefix="/v1py/healthcheck", tags=["health"])


@router.get("")
async def healthcheck(request: Request):
    app_state = request.app.state.app
    return {
        "status": "available",
        "environment": app_state.config.env,
        "version": app_state.config.version,
    }

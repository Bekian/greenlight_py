from fastapi import Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


# Chapter 4.03
# apply a 1mb size limit for client requests
class RateLimitSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_bytes: int):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        # Check Content-Length header if it exists
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_bytes:
            return ORJSONResponse(
                status_code=413,  # Content Too Large
                content={"error": "request body too large"},
            )

        return await call_next(request)

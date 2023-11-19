from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from web.api.api_main import app
from web.errors import WebError


@app.exception_handler(WebError)
async def web_error_handler(request: Request, error: WebError):
    return JSONResponse(
        status_code=error.status_code,
        content=jsonable_encoder({"detail": error.detail}),
    )

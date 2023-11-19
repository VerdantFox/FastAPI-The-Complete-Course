from typing import cast

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from datastore import db_models
from datastore.database import DBDependency, Session
from permissions import Role
from web import field_types as ft
from web.api import api_models, errors
from web.auth import LoggedInUser, LoggedInUserOptional
from web.web_app.const import templates

# ----------- Routers -----------
router = APIRouter(tags=["error"], prefix="/errors")


class WebAppError(BaseModel):
    """Base class for all web errors."""

    detail: str = "Unknown error"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@router.get("", response_class=HTMLResponse)
async def general_error(
    request: Request,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail: str = "Unknown error",
):
    web_app_error = WebAppError(detail=detail, status_code=status_code)
    return templates.TemplateResponse(
        "errors/general_error.html",
        {"request": request, "error": web_app_error},
        status_code=web_app_error.status_code,
    )

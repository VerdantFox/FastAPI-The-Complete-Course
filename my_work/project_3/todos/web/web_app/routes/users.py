from typing import cast

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

from datastore import db_models
from datastore.database import DBDependency, Session
from permissions import Role
from web import templates
from web.api import api_models, auth, errors
from web.api import field_types as ft

# ----------- Routers -----------
router = APIRouter(tags=["users"], prefix="/users")


@router.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

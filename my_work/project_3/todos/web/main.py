from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

import datastore.db_models as db_models
from datastore.database import engine
from web.api import api_main
from web.web_app import web_app_main

SESSION_SECRET = "SUPER-SECRET-KEY"

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

db_models.Base.metadata.create_all(bind=engine)


@app.get("/api")
async def api_home(request: Request):
    return RedirectResponse(url=request.url_for("api:swagger_ui_html"), status_code=302)


app.mount("/api", api_main.app, name="api")
app.mount("/", web_app_main.app, name="web_app")

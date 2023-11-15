from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import datastore.db_models as db_models
from datastore.database import engine
from web import STATIC_DIR
from web.api import api_main
from web.web_app.routes import users

app = FastAPI()

app.include_router(users.router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

db_models.Base.metadata.create_all(bind=engine)

app.mount("/api", api_main.app)

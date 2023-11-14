from fastapi import FastAPI

import datastore.db_models as db_models
from api.routes import auth, todos, users
from datastore.database import engine

app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)

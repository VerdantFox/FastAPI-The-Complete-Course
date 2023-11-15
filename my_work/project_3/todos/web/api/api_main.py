from fastapi import FastAPI

from web.api.routes import auth, todos, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)

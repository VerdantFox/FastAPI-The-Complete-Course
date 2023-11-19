from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from web.web_app import flash_messages
from web.web_app.const import STATIC_DIR, templates
from web.web_app.error_handlers import register_error_handlers
from web.web_app.routes import errors, todos, users

SESSION_SECRET = "SUPER-SECRET-KEY"

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

routes = [todos, users, errors]
for route in routes:
    app.include_router(route.router)

register_error_handlers(app)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates.env.globals["get_flashed_messages"] = flash_messages.get_flashed_messages


@app.get("/")
async def home(request: Request):
    return RedirectResponse(
        url=request.url_for("web_app:get_todos"), status_code=status.HTTP_302_FOUND
    )

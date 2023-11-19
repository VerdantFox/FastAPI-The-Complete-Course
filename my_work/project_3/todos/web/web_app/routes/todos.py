from functools import wraps
from inspect import signature
from typing import Annotated, cast

from fastapi import APIRouter, Path, Request, status
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse
from wtforms import (
    BooleanField,
    Form,
    HiddenField,
    IntegerField,
    PasswordField,
    StringField,
    validators,
    widgets,
)

from datastore import db_models
from datastore.database import DBDependency, Session
from permissions import Role
from web import auth, errors
from web import field_types as ft
from web.api import api_models
from web.auth import LoggedInUser
from web.web_app.const import templates
from web.web_models import UnauthenticatedUser

# ----------- Routers -----------
router = APIRouter(tags=["todos"], prefix="/todos")


@router.get("", response_class=HTMLResponse)
async def get_todos(request: Request, db: DBDependency, current_user: LoggedInUser):
    query = db.query(db_models.Todo).filter(db_models.Todo.owner_id == current_user.id)
    todos_list_db = cast(list[db_models.Todo], query.all())
    todos_list_api = [
        api_models.TodoOutLimited(**todo.__dict__) for todo in todos_list_db
    ]

    return templates.TemplateResponse(
        "todos/todos.html",
        {"request": request, "current_user": current_user, "todos": todos_list_api},
    )


class CreateTodoForm(Form):
    title: str = StringField("Title", validators=[validators.Length(min=3, max=25)])


@router.post("")
async def add_todo(request: Request, db: DBDependency, current_user: LoggedInUser):
    form_data = await request.form()
    create_todo_form = CreateTodoForm(**form_data)
    if not create_todo_form.validate():
        return HTMLResponse(content="", status_code=status.HTTP_400_BAD_REQUEST)
    todo = db_models.Todo(
        title=create_todo_form.title.data,
        description="Doesn't matter...",
        priority=1,
        owner_id=current_user.id,
        completed=False,
    )
    db.add(todo)
    db.commit()

    return templates.TemplateResponse(
        "todos/partials/todo.html",
        {"request": request, "todo": todo},
    )


class UpdateTodoForm(Form):
    title: str = StringField("Title", validators=[validators.Length(min=3, max=25)])
    completed: bool = BooleanField("Completed", default=False)


@router.patch("/{todo_id}")
async def update_todo(
    request: Request,
    todo_id: Annotated[int, Path()],
    db: DBDependency,
    current_user: LoggedInUser,
):
    form_data = await request.form()
    update_todo_form = UpdateTodoForm(**form_data)
    todo = db.query(db_models.Todo).filter(db_models.Todo.id == todo_id).first()
    if not todo:
        raise errors.TodoNotFoundError
    if todo.owner_id != current_user.id:
        raise errors.TodoNotOwnedError
    todo.title = update_todo_form.title.data
    todo.completed = update_todo_form.completed.data
    db.commit()
    return templates.TemplateResponse(
        "todos/partials/todo.html",
        {"request": request, "todo": todo},
    )


@router.delete("/{todo_id}")
async def delete_todo(
    request: Request,
    todo_id: Annotated[int, Path()],
    db: DBDependency,
    current_user: LoggedInUser,
):
    todo = db.query(db_models.Todo).filter(db_models.Todo.id == todo_id).first()
    if not todo:
        raise errors.TodoNotFoundError
    if todo.owner_id != current_user.id:
        raise errors.TodoNotOwnedError
    db.delete(todo)
    db.commit()
    return templates.TemplateResponse(
        "todos/partials/todo.html",
        {"request": request, "todo": todo},
    )

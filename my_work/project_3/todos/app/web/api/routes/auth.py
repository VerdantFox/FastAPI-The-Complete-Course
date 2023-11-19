from datetime import timedelta

from fastapi import APIRouter, Response

from app.datastore.database import DBDependency
from app.web import auth
from app.web import field_types as ft

# ----------- Routers -----------
router = APIRouter(tags=["auth"], prefix="/auth")

# ----------- Imported Dependencies -----------
# Oauth2FormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token")
async def login_for_access_token(
    response: Response,
    db: DBDependency,
    username: ft.StrFormField,
    password: ft.StrFormField,
):
    user = auth.authenticate_user(username=username, password=password, db=db)
    token = auth.create_access_token(user=user, expires_delta=timedelta(minutes=15))
    response.set_cookie(
        key="access_token", value=token.access_token, httponly=True, secure=True
    )
    return token

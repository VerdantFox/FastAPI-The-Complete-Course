from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from datastore.database import DBDependency
from web.api import api_models, auth
from web.api.responses import UNAUTHORIZED_RESPONSE

# ----------- Routers -----------
router = APIRouter(tags=["auth"], prefix="/auth")

# ----------- Imported Dependencies -----------
Oauth2FormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post(
    "/token",
    status_code=status.HTTP_200_OK,
    responses=UNAUTHORIZED_RESPONSE,
    response_model=api_models.Token,
)
async def login_for_access_token(
    form_data: Oauth2FormDependency, db: DBDependency
) -> api_models.Token:
    user = auth.authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    return auth.create_access_token(user=user, expires_delta=timedelta(minutes=15))

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

import mixins
import web.api.field_types as ft
from datastore import db_models
from datastore.database import DBDependency
from permissions import Role
from web.api import api_models, errors

# ----------- Constants -----------
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
optional_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth", auto_error=False)


# ----------- Imported Dependencies -----------
TokenDependency = Annotated[str, Depends(oauth2_bearer)]
OptionalTokenDependency = Annotated[str | None, Depends(optional_oauth2_bearer)]


# ----------- User Constants (should be in secrets) -----------
SECRET_KEY = "a32739cd7e677c1b8dfcf560a68d59793efdd035fa14dc488192b815d3b5e498"
ALGORITHM = "HS256"


class UnauthenticatedUser(mixins.AuthUserMixin):
    """Unauthenticated User model"""

    id = -1
    username = "unauthenticated_user"
    is_active = False
    role = Role.UNAUTHENTICATED

    # non-table fields
    is_authenticated: bool = False


# ------------ Functions ------------
async def get_current_user_auth_optional(
    token: OptionalTokenDependency,
    db: DBDependency,
) -> api_models.UserFromAuth | None:
    """Get the current user from the token."""
    if token:
        return await get_current_user_auth_required(token, db)
    return UnauthenticatedUser()


async def get_current_user_auth_required(
    token: TokenDependency, db: DBDependency
) -> api_models.UserFromAuth:
    """Get the current user from the token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError as e:
        raise errors.UserNotValidatedError from e
    username: str = payload.get("sub")
    user_id: int = payload.get("user_id")
    # user_role: str = payload.get("role")
    if not all((username, user_id)):
        raise errors.UserNotValidatedError
    return _get_current_user_by_id(user_id, db)


def create_access_token(
    user: db_models.User, expires_delta: timedelta
) -> api_models.Token:
    expires_at = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role,
        "exp": expires_at,
    }
    access_token = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return api_models.Token(access_token=access_token, token_type="bearer")


def authenticate_user(
    username: str, password: str, db: DBDependency
) -> db_models.User | None:
    user = db.query(db_models.User).filter(db_models.User.username == username).first()
    if not user:
        raise errors.UserNotAuthenticatedError
    if not verify_password(password, user.hashed_password):
        raise errors.UserNotAuthenticatedError
    return user


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def _get_current_user_by_id(user_id: ft.Id, db: DBDependency) -> db_models.User:
    """Get a user by id."""
    if (
        user_model := db.query(db_models.User)
        .filter(db_models.User.id == user_id)
        .first()
    ):
        return user_model
    raise errors.UserNotFoundError


#  ----------- Exported Dependencies -----------
RequiredUserDependency = Annotated[
    db_models.User, Depends(get_current_user_auth_required)
]
OptionalUserDependency = Annotated[
    db_models.User | UnauthenticatedUser, Depends(get_current_user_auth_optional)
]

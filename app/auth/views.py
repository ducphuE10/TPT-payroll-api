from fastapi import APIRouter

from app.auth.models import (
    Role,
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserRead,
    UserRegister,
    UserRegisterResponse,
)
from app.auth.service import CurrentUser, create, get_by_email
from app.db.core import DbSession
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages
from app.core.config import settings


auth_router = APIRouter(prefix=settings.API_VERSION_PREFIX)
user_router = APIRouter(prefix=settings.API_VERSION_PREFIX)


@user_router.post(
    "",
    response_model=UserRead,
)
def create_user(
    user_in: UserCreate,
    db_session: DbSession,
    current_user: CurrentUser,
):
    """Creates a new user."""
    if current_user.role != Role.ADMIN:
        raise AppException(ErrorMessages.ForbiddenAction())

    user = get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise AppException(ErrorMessages.UserWithEmailAlreadyExists())
    user = create(db_session=db_session, user_in=user_in)
    return user


@auth_router.get("/me", response_model=UserRead)
def get_me(
    *,
    db_session: DbSession,
    current_user: CurrentUser,
):
    return current_user


@auth_router.post("/login", response_model=UserLoginResponse)
def login_user(
    user_in: UserLogin,
    db_session: DbSession,
):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user and user.check_password(user_in.password):
        return {
            "access_token": user.token,
            "refresh_token": "",
            "access_token_expires_at": "",
            "refresh_token_expires_at": "",
        }
    raise AppException(ErrorMessages.InvalidUsernameOrPassword())


@auth_router.post("/register", response_model=UserRegisterResponse)
def register_user(
    user_in: UserRegister,
    db_session: DbSession,
):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise AppException(ErrorMessages.UserWithEmailAlreadyExists())
    if user_in.role == Role.ADMIN:
        raise AppException(ErrorMessages.CannotCreateAdminUser())
    user = create(db_session=db_session, user_in=user_in)
    return user

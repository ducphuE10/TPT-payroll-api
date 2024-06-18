from fastapi import APIRouter

from payroll.auth.models import (
    Role,
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserRead,
    UserRegister,
    UserRegisterResponse,
)
from payroll.auth.service import CurrentUser, create, get_by_email
from payroll.database.core import DbSession
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages


auth_router = APIRouter()
user_router = APIRouter()


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
        return {"token": user.token}
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

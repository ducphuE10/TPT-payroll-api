from fastapi import APIRouter, HTTPException, status

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

from payroll.exceptions import (
    ForbiddenError,
    InvalidConfigurationError,
    UnauthorizedError,
)

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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[
                {
                    "msg": "You don't have permissions to create a new user. Please, contract the administrator."
                }
            ],
        )
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise InvalidConfigurationError(msg="User with this email already exists.")
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
    raise UnauthorizedError(msg="Invalid username or password.")


@auth_router.post("/register", response_model=UserRegisterResponse)
def register_user(
    user_in: UserRegister,
    db_session: DbSession,
):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise InvalidConfigurationError(msg="User with this email already exists.")
    if user_in.role == Role.ADMIN:
        raise ForbiddenError(msg="You can't create an admin user.")
    user = create(db_session=db_session, user_in=user_in)
    return user

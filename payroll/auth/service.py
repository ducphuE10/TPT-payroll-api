import logging
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from payroll.auth.models import PayrollUser, UserCreate, UserRegister
from payroll.config import settings
from payroll.utils_functions import get_user_email
from payroll.utils_functions import TokenDep


log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)


def get(*, db_session, user_id: int) -> Optional[PayrollUser]:
    """Returns a user based on the given user id."""
    return db_session.query(PayrollUser).filter(PayrollUser.id == user_id).one_or_none()


def get_by_email(*, db_session, email: str) -> Optional[PayrollUser]:
    """Returns a user based on the given email."""
    return (
        db_session.query(PayrollUser).filter(PayrollUser.email == email).one_or_none()
    )


def create(*, db_session, user_in: UserRegister | UserCreate) -> PayrollUser:
    """Creates a new user."""
    password = bytes(user_in.password, "utf-8")

    user = PayrollUser(**user_in.model_dump(exclude={"password"}), password=password)
    db_session.add(user)
    db_session.commit()
    return user


def get_or_create(*, db_session, user_in: UserRegister) -> PayrollUser:
    """Gets an existing user or creates a new one."""
    user = get_by_email(db_session=db_session, email=user_in.email)

    if not user:
        try:
            user = create(db_session=db_session, user_in=user_in)
        except IntegrityError:
            db_session.rollback()
            log.exception(f"Unable to create user with email address {user_in.email}.")

    return user


def get_current_user(request: Request, authorization: TokenDep) -> PayrollUser:
    """Attempts to get the current user depending on the configured authentication provider."""
    user_email = get_user_email(authorization)
    if not user_email:
        log.exception(
            f"Unable to determine user email based on configured auth provider or no default auth user email defined. Provider: {settings.AUTHENTICATION_PROVIDER_SLUG}"
        )
        raise InvalidCredentialException
    return get_by_email(
        db_session=request.state.db,
        email=user_email,
    )


CurrentUser = Annotated[PayrollUser, Depends(get_current_user)]

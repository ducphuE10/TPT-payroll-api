import secrets
from enum import Enum

import string
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import bcrypt
from jose import jwt

from payroll.config import settings
from payroll.database.core import Base
from payroll.utils.models import Pagination, PayrollBase, TimeStampMixin
from pydantic import field_validator
from pydantic.networks import EmailStr
from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column


def generate_password():
    """Generates a reasonable password if none is provided."""
    alphanumeric = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphanumeric) for i in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)  # noqa
            and sum(c.isdigit() for c in password) >= 3  # noqa
        ):
            break
    return password


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class Role(str, Enum):
    ADMIN = "admin"
    USER = "regular_user"


class PayrollUser(Base, TimeStampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    password: Mapped[bytes] = mapped_column(LargeBinary)
    role: Mapped[Role]

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, fullname={self.fullname!r})"

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @property
    def token(self):
        now = datetime.now(timezone.utc)
        exp = (
            now + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, settings.SECRET_KEY.get_secret_value())


class UserBase(PayrollBase):
    email: EmailStr

    @field_validator("email")
    def email_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string and must be a email")
        return v


class UserLogin(UserBase):
    password: Optional[str] = None

    @field_validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


class UserRegister(UserLogin):
    name: str
    role: Optional[Role] = Role.USER

    @field_validator("password", mode="before")
    def password_required(cls, v):
        # we generate a password for those that don't have one

        password = v or generate_password()
        return hash_password(password)


class UserLoginResponse(PayrollBase):
    # company
    token: Optional[str] = None


class UserRead(UserBase):
    id: int
    role: Optional[str] = None


class UserUpdate(PayrollBase):
    id: int
    password: Optional[str] = None

    @field_validator("password", mode="before")
    def hash(cls, v):
        return hash_password(str(v))


class UserCreate(UserRegister):
    pass


class UserRegisterResponse(PayrollBase):
    token: Optional[str] = None


class UserPagination(Pagination):
    items: List[UserRead] = []

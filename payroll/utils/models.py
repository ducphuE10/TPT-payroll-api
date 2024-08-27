from enum import Enum
from datetime import datetime
import random
import string
from pydantic import BaseModel
from pydantic.types import conint, constr, SecretStr
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.ext.declarative import declared_attr


# pydantic type that limits the range of primary keys
PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(pattern=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)
CompanySlug = constr(pattern=r"^[\w]+(?:_[\w]+)*$", min_length=3)


# SQLAlchemy models...
class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class RandomCodeMixin:
    @staticmethod
    def generate_random_code(length=8):
        """Generates a random alphanumeric code of specified length."""
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    @declared_attr
    def code(cls):
        return Column(
            String(20),
            unique=True,
            nullable=False,
            default=lambda: cls.generate_random_code(),
        )

    @classmethod
    def generate_and_set_code(cls, target, value, oldvalue, initiator):
        """Generates and sets a random code if not already set."""
        if not value:
            target.code = cls.generate_random_code()


# Pydantic models...
class PayrollBase(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class Pagination(PayrollBase):
    itemsPerPage: int
    page: int
    total: int


class TaxType(str, Enum):
    Progressive = "PROGRESSIVE"
    Fixed = "FIXED"


class InsuranceType(str, Enum):
    BasicSalary = "BASIC_SALARY"
    TotalSalary = "TOTAL_SALARY"
    CustomByEmployee = "CUSTOM_BY_EMPLOYEE"


class Day(str, Enum):
    Mon = "Monday"
    Tue = "Tuesday"
    Wed = "Wednesday"
    Thu = "Thursday"
    Fri = "Friday"
    Sat = "Saturday"
    Sun = "Sunday"


class Gender(str, Enum):
    Male = "male"
    Female = "female"


class Nationality(str, Enum):
    VN = "Vietnam"
    JP = "Japan"


class PaymentMethod(str, Enum):
    CASH = "cash"
    BANK = "bank"


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"


class BenefitReplay(str, Enum):
    DAILY = "daily"
    MONTHLY = "monthly"
    YEARLY = "yearly"

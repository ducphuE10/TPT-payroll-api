from datetime import datetime
from typing import List, Optional

from app.utils.models import BenefitType, Pagination, PayrollBase


class BenefitBase(PayrollBase):
    code: str  # required
    name: str  # required
    replay: str
    type: BenefitType
    count_salary: bool
    value: float
    description: Optional[str] = None


class BenefitRead(BenefitBase):
    id: int
    created_at: datetime


class BenefitsRead(PayrollBase):
    count: int
    data: list[BenefitRead] = []


class BenefitUpdate(PayrollBase):
    name: Optional[str] = None
    type: Optional[BenefitType] = None
    count_salary: Optional[bool] = None
    value: Optional[float] = None
    description: Optional[str] = None


class BenefitCreate(PayrollBase):
    code: str  # required
    name: str  # required
    type: BenefitType  # required
    count_salary: bool = False
    value: float
    description: Optional[str] = None


class BenefitPagination(Pagination):
    items: List[BenefitRead] = []

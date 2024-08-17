from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class BenefitBase(PayrollBase):
    code: str  # required
    name: str  # required
    replay: str
    count_salary: bool
    value: float
    description: Optional[str]


class BenefitRead(BenefitBase):
    id: int
    created_at: datetime


class BenefitsRead(PayrollBase):
    count: int
    data: list[BenefitRead] = []


class BenefitUpdate(PayrollBase):
    name: Optional[str] = None
    count_salary: Optional[bool] = None
    value: Optional[float] = None
    description: Optional[str] = None


class BenefitCreate(PayrollBase):
    code: str  # required
    name: str  # required
    replay: str
    value: float
    description: Optional[str]


class BenefitPagination(Pagination):
    items: List[BenefitRead] = []

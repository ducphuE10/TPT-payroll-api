from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class BenefitBase(PayrollBase):
    code: str  # required
    name: str  # required
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
    count_salary: Optional[str] = None
    value: Optional[float] = None
    description: Optional[str] = None


class BenefitCreate(BenefitBase):
    pass


class BenefitPagination(Pagination):
    items: List[BenefitRead] = []

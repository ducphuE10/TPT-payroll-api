from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class WelfareBase(PayrollBase):
    code: str  # required
    name: str  # required
    count_salary: bool
    value: float
    description: Optional[str]


class WelfareRead(WelfareBase):
    id: int
    created_at: datetime


class WelfaresRead(PayrollBase):
    count: int
    data: list[WelfareRead] = []


class WelfareUpdate(PayrollBase):
    name: Optional[str] = None
    count_salary: Optional[str] = None
    value: Optional[float] = None
    description: Optional[str] = None


class WelfareCreate(WelfareBase):
    pass


class WelfarePagination(Pagination):
    items: List[WelfareRead] = []

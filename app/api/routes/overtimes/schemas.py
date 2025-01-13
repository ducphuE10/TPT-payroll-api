from datetime import datetime, date
from typing import List, Optional

from app.utils.models import Pagination, PayrollBase


class OvertimeBase(PayrollBase):
    employee_id: int  # required
    day_overtime: date  # required
    overtime_hours: float  # required
    company_id: int  # required


class OvertimeRead(OvertimeBase):
    id: int
    created_at: datetime


class OvertimesRead(PayrollBase):
    count: int
    data: list[OvertimeRead] = []


class OvertimeUpdate(PayrollBase):
    overtime_hours: Optional[float] = None


class OvertimeCreate(OvertimeBase):
    pass


class OvertimesCreate(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]
    from_date: date
    to_date: date
    overtime_hours: float
    company_id: int


class OvertimesDelete(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]
    from_date: date
    to_date: date


class OvertimePagination(Pagination):
    items: List[OvertimeRead] = []


# For import function
class WorkhoursOvertimeHandlerBase(PayrollBase):
    employee_id: int  # required
    day_overtime: date  # required
    overtime_hours: float  # required
    company_id: int  # required

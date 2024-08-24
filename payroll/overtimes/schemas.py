from datetime import datetime, date, time
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class OvertimeBase(PayrollBase):
    employee_id: int  # required
    day_overtime: date  # required
    overtime_hours: float  # required


class OvertimeRead(OvertimeBase):
    id: int
    created_at: datetime


class OvertimesRead(PayrollBase):
    count: int
    data: list[OvertimeRead] = []


class OvertimeUpdate(PayrollBase):
    work_hours: Optional[float] = None


class OvertimeCreate(OvertimeBase):
    pass


class OvertimePagination(Pagination):
    items: List[OvertimeRead] = []


# For import function
class WorkhoursOvertimeHandlerBase(PayrollBase):
    employee_id: int  # required
    day_overtime: date  # required
    overtime_hours: float  # required


class TimeOvertimeHandlerBase(PayrollBase):
    employee_id: int  # required
    day_overtime: date  # required
    checkin: time  # required
    checkout: time  # required

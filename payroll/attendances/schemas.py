from datetime import datetime, date, time
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class AttendanceBase(PayrollBase):
    employee_id: int  # required
    day_attendance: date  # required
    work_hours: float  # required


class AttendanceRead(AttendanceBase):
    id: int
    created_at: datetime


class AttendancesRead(PayrollBase):
    count: int
    data: list[AttendanceRead] = []


class AttendanceUpdate(PayrollBase):
    work_hours: Optional[float] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendancesCreate(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]
    from_date: date
    to_date: date
    work_hours: float


class AttendancesDelete(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]
    from_date: date
    to_date: date


class AttendancePagination(Pagination):
    items: List[AttendanceRead] = []


# For import function
class WorkhoursAttendanceHandlerBase(PayrollBase):
    employee_id: int  # required
    day_attendance: date  # required
    work_hours: float  # required


class TimeAttendanceHandlerBase(PayrollBase):
    employee_id: int  # required
    day_attendance: date  # required
    checkin: time  # required
    checkout: time  # required

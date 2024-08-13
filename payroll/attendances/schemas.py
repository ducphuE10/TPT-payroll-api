from datetime import datetime, date, time
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class AttendanceBase(PayrollBase):
    employee_id: int  # required
    day_attendance: date  # required
    check_time: time  # required


class AttendanceRead(AttendanceBase):
    id: int
    created_at: datetime


class AttendancesRead(PayrollBase):
    count: int
    data: list[AttendanceRead] = []


class AttendanceUpdate(PayrollBase):
    check_time: Optional[bool] = None


class AttendanceCreate(PayrollBase):
    employee_id: int  # required
    day_attendance: date  # required
    check_time: time  # required


class PositionPagination(Pagination):
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

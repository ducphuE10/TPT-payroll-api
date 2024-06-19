from datetime import datetime, date
from typing import List, Optional
from payroll.utils.models import Pagination, PayrollBase


class AttendanceBase(PayrollBase):
    employee_name: str  # required
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[float]
    afm: Optional[float]
    wait4work: Optional[float]
    day_attendance: date  # required
    employee_id: int  # required


class AttendanceRead(AttendanceBase):
    id: int
    created_at: datetime


class AttendancesRead(PayrollBase):
    data: list[AttendanceRead] = []


class AttendanceUpdate(PayrollBase):
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[float]
    afm: Optional[float]
    wait4work: Optional[float]
    day_attendance: Optional[date]  # required


class AttendanceImport(PayrollBase):
    employee_name: str  # required
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[float]
    afm: Optional[float]
    wait4work: Optional[float]
    day_attendance: date  # required
    employee_id: int  # required


class AttendanceCreate(PayrollBase):
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[float]
    afm: Optional[float]
    wait4work: Optional[float]
    day_attendance: date  # required
    employee_id: int  # required


class PositionPagination(Pagination):
    items: List[AttendanceRead] = []

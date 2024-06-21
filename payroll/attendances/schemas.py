from datetime import datetime, date
from typing import List, Optional

from pydantic import model_validator
from payroll.utils.models import Pagination, PayrollBase


class AttendanceBase(PayrollBase):
    employee_id: int  # required
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[bool]
    afm: Optional[bool]
    wait4work: Optional[bool]
    day_attendance: date  # required


class AttendanceRead(AttendanceBase):
    id: int
    created_at: datetime


class AttendancesRead(PayrollBase):
    data: list[AttendanceRead] = []


class AttendanceUpdate(PayrollBase):
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[bool]
    afm: Optional[bool]
    wait4work: Optional[bool]
    day_attendance: Optional[date]  # required


class AttendanceImport(PayrollBase):
    employee_id: int  # required
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[bool]
    afm: Optional[bool]
    wait4work: Optional[bool]
    day_attendance: date  # required


class AttendanceCreate(PayrollBase):
    employee_id: int  # required
    work_hours: Optional[float] = None
    overtime: Optional[float] = None
    holiday: Optional[bool] = None
    afm: Optional[bool] = None
    wait4work: Optional[bool] = None

    @model_validator(mode="after")
    def check_one_optional_field(cls, values):
        optional_fields = ["work_hours", "overtime", "holiday", "afm", "wait4work"]
        set_fields = [
            field for field in optional_fields if getattr(values, field) is not None
        ]

        if len(set_fields) != 1:
            raise ValueError(
                "Exactly one of work_hours, overtime, holiday, afm, or wait4work must be set."
            )

        return values


class PositionPagination(Pagination):
    items: List[AttendanceRead] = []

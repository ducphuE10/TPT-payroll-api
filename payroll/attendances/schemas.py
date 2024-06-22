from datetime import datetime, date
from typing import List, Optional, Union

from pydantic import model_validator
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.utils.models import Pagination, PayrollBase


# validate that only one of 'work' or 'leave' attributes can be set, not both
def check_work_or_leave_set(
    obj: Union["AttendanceUpdate", "AttendanceCreate"],
) -> Union["AttendanceUpdate", "AttendanceCreate"]:
    work_set = any([obj.work_hours is not None, obj.overtime is not None])
    leave_set = [
        obj.holiday is not None,
        obj.afm is not None,
        obj.wait4work is not None,
    ]

    if work_set and any(leave_set):
        """Only one of 'work' or 'leave' attributes can be set, not both."""
        raise AppException(ErrorMessages.WorkLeaveState())
    if not work_set and not any(leave_set):
        """At least one of 'work' or 'leave' attributes must be set."""
        raise AppException(ErrorMessages.WorkLeaveState())
    if sum(leave_set) > 1:
        """Only one attribute within 'leave' set can be set at a time."""
        raise AppException(ErrorMessages.WorkLeaveState())

    return obj


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

    check_work_or_leave_set = model_validator(mode="after")(check_work_or_leave_set)


class AttendanceCreate(PayrollBase):
    employee_id: int  # required
    work_hours: Optional[float] = None
    overtime: Optional[float] = None
    holiday: Optional[bool] = None
    afm: Optional[bool] = None
    wait4work: Optional[bool] = None
    day_attendance: date  # required

    check_work_or_leave_set = model_validator(mode="after")(check_work_or_leave_set)


class AttendanceImport(PayrollBase):
    employee_id: int  # required
    work_hours: Optional[float]
    overtime: Optional[float]
    holiday: Optional[bool]
    afm: Optional[bool]
    wait4work: Optional[bool]
    day_attendance: date  # required


class PositionPagination(Pagination):
    items: List[AttendanceRead] = []

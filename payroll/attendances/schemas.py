from datetime import datetime, date, time
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase

# from .validators import check_work_or_leave_set


# def check_work_or_leave_set(
#     obj: Union["AttendanceUpdate", "AttendanceCreate"],
# ) -> Union["AttendanceUpdate", "AttendanceCreate"]:
#     work_set = any([obj.work_hours is not None, obj.overtime is not None])
#     leave_set = [
#         obj.holiday is not None,
#         obj.afm is not None,
#         obj.wait4work is not None,
#     ]

#     if work_set and any(leave_set):
#         """Only one of 'work' or 'leave' attributes can be set, not both."""
#         raise AppException(ErrorMessages.WorkLeaveState())
#     if not work_set and not any(leave_set):
#         """At least one of 'work' or 'leave' attributes must be set."""
#         raise AppException(ErrorMessages.WorkLeaveState())
#     if sum(leave_set) > 1:
#         """Only one attribute within 'leave' set can be set at a time."""
#         raise AppException(ErrorMessages.WorkLeaveState())

#     return obj

# id: Mapped[int] = mapped_column(primary_key=True)  # required
# check_time: Mapped[time] = mapped_column(Time)  # required
# day_attendance: Mapped[date]  # required
# employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))  # required
# created_by: Mapped[str] = mapped_column(String(30))  # required

# employee: Mapped["PayrollEmployee"] = relationship(
#     "PayrollEmployee", back_populates="attendances"
# )


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


class AttendanceImport(PayrollBase):
    employee_id: int  # required
    day_attendance: date  # required
    work_hours: Optional[float]  # half required
    overtime: Optional[float]  # half required
    holiday: Optional[bool]  # half required
    afm: Optional[bool]  # half required
    wait4work: Optional[bool]  # half required


class PositionPagination(Pagination):
    items: List[AttendanceRead] = []

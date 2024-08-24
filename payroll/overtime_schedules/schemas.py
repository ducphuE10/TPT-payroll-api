from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase

"""
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    mon: Mapped[Optional[float]]
    tue: Mapped[Optional[float]]
    wed: Mapped[Optional[float]]
    thur: Mapped[Optional[float]]
    fri: Mapped[Optional[float]]
    sat: Mapped[Optional[float]]
    sun: Mapped[Optional[float]]
"""


class OvertimeScheduleBase(PayrollBase):
    code: str  # required
    name: str  # required
    mon: Optional[float] = None
    tue: Optional[float] = None
    wed: Optional[float] = None
    thur: Optional[float] = None
    fri: Optional[float] = None
    sat: Optional[float] = None
    sun: Optional[float] = None


class OvertimeScheduleRead(OvertimeScheduleBase):
    id: int
    created_at: datetime


class OvertimeSchedulesRead(PayrollBase):
    count: int
    data: list[OvertimeScheduleRead] = []


# class ScheduleWithDetailsRead(OvertimeScheduleRead):
#     schedule_details: SimpleScheduleDetailsRead


class OvertimeScheduleUpdate(PayrollBase):
    name: Optional[str] = None
    mon: Optional[float] = None
    tue: Optional[float] = None
    wed: Optional[float] = None
    thur: Optional[float] = None
    fri: Optional[float] = None
    sat: Optional[float] = None
    sun: Optional[float] = None


class OvertimeScheduleCreate(OvertimeScheduleBase):
    pass


class OvertimeSchedulePagination(Pagination):
    items: List[OvertimeScheduleRead] = []

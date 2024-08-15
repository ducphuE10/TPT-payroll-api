from pydantic import Field
from datetime import datetime
from typing import List, Optional
from payroll.utils.models import Day, Pagination, PayrollBase


class ScheduleDetailBase(PayrollBase):
    schedule_id: int
    shift_id: int
    day: Optional[Day]


class ScheduleDetailRead(ScheduleDetailBase):
    id: int
    created_at: datetime


class ScheduleDetailsRead(PayrollBase):
    count: int
    data: list[ScheduleDetailRead] = []


class ScheduleDetailCreate(ScheduleDetailBase):
    pass


class ScheduleDetailsCreate(PayrollBase):
    shift_id: int
    day: Optional[Day]


class SimpleScheduleDetailRead(ScheduleDetailsCreate):
    pass


class SimpleScheduleDetailsRead(PayrollBase):
    count: int
    data: list[SimpleScheduleDetailRead] = []


class ScheduleDetailUpdate(PayrollBase):
    shift_id: Optional[int]
    day: Optional[Day]


class ScheduleDetailsUpdate(PayrollBase):
    id: int = Field(..., Literal=True)
    shift_id: Optional[int]
    day: Optional[Day]


# class ScheduleDetailsCreate(PayrollBase):
#     data: list[ScheduleDetailCreate] = []


class ScheduleDetailPagination(Pagination):
    items: List[ScheduleDetailRead] = []

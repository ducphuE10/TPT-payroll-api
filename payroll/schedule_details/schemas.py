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


class ScheduleDetailUpdate(PayrollBase):
    shift_id: Optional[int]
    day: Optional[Day]


class ScheduleDetailCreate(ScheduleDetailBase):
    pass


class ScheduleDetailsCreate(PayrollBase):
    data: list[ScheduleDetailCreate] = []


class PositionPagination(Pagination):
    items: List[ScheduleDetailRead] = []

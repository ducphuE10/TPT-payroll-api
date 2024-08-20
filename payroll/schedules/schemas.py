from datetime import datetime
from typing import List, Optional

from payroll.schedule_details.schemas import (
    SimpleScheduleDetailRead,
)
from payroll.utils.models import Pagination, PayrollBase


class ScheduleBase(PayrollBase):
    code: str  # required
    name: str  # required
    shift_per_day: int  # required


class ScheduleRead(ScheduleBase):
    id: int
    created_at: datetime


class SchedulesRead(PayrollBase):
    count: int
    data: list[ScheduleRead] = []


class ScheduleWithDetailsRead(PayrollBase):
    schedule_in: ScheduleBase
    schedule_detail_list_in: List[SimpleScheduleDetailRead]


class ScheduleUpdate(PayrollBase):
    name: Optional[str] = None
    shift_per_day: Optional[int] = None


class ScheduleCreate(ScheduleBase):
    pass


class SchedulePagination(Pagination):
    items: List[ScheduleRead] = []

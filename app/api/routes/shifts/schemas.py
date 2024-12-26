from datetime import datetime
from typing import List, Optional

from app.utils.models import Pagination, PayrollBase


class ShiftBase(PayrollBase):
    code: str  # required
    name: str  # required
    standard_work_hours: float  # required
    # checkin: time
    # earliest_checkin: time
    # latest_checkin: time
    # checkout: time
    # earliest_checkout: time
    # latest_checkout: time


class ShiftRead(ShiftBase):
    id: int
    created_at: datetime


class ShiftsRead(PayrollBase):
    count: int
    data: list[ShiftRead] = []


class ShiftUpdate(PayrollBase):
    name: Optional[str] = None
    standard_work_hours: Optional[float] = None
    # checkin: Optional[time] = None
    # earliest_checkin: Optional[time] = None
    # latest_checkin: Optional[time] = None
    # checkout: Optional[time] = None
    # earliest_checkout: Optional[time] = None
    # latest_checkout: Optional[time] = None


class ShiftCreate(ShiftBase):
    pass


class ShiftPagination(Pagination):
    items: List[ShiftRead] = []

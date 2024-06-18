from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class PositionBase(PayrollBase):
    code: str  # required
    name: str  # required
    description: Optional[str] = None


class PositionRead(PositionBase):
    id: int
    created_at: datetime


class PositionsRead(PayrollBase):
    data: list[PositionRead] = []


class PositionUpdate(PositionBase):
    name: Optional[str] = None
    description: Optional[str] = None


class PositionCreate(PositionBase):
    pass


class PositionPagination(Pagination):
    items: List[PositionRead] = []

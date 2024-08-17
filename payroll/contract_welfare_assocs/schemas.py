from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class CWAssocBase(PayrollBase):
    contract_id: int
    welfare_id: int


class CWAssocRead(CWAssocBase):
    id: int
    created_at: datetime


class CWAssocsRead(PayrollBase):
    count: int
    data: list[CWAssocRead] = []


class CWAssocUpdate(PayrollBase):
    welfare_id: Optional[int]


class CWAssocCreate(CWAssocBase):
    pass


class CWAssocPagination(Pagination):
    items: List[CWAssocRead] = []

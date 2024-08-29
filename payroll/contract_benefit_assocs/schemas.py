from datetime import datetime
from typing import List, Optional

from pydantic import Field

from payroll.utils.models import Pagination, PayrollBase


class CBAssocBase(PayrollBase):
    contract_id: int
    benefit_id: int


class CBAssocRead(CBAssocBase):
    id: int
    created_at: datetime


class CBAssocsRead(PayrollBase):
    count: int
    data: list[CBAssocRead] = []


class CBAssocUpdate(PayrollBase):
    benefit_id: Optional[int]


class CBAssocsUpdate(PayrollBase):
    id: int = Field(..., Literal=True)
    benefit_id: Optional[int]


class CBAssocCreate(CBAssocBase):
    pass


class CBAssocsCreate(PayrollBase):
    benefit_id: int


class CBAssocPagination(Pagination):
    items: List[CBAssocRead] = []

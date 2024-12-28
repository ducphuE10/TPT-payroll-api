from datetime import datetime
from typing import List, Optional

from app.utils.models import Pagination, PayrollBase


class CompanyBase(PayrollBase):
    code: str  # required
    name: str  # required
    description: Optional[str] = None


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime


class CompaniesRead(PayrollBase):
    count: int
    data: list[CompanyRead] = []


class CompanyUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyPagination(Pagination):
    items: List[CompanyRead] = []

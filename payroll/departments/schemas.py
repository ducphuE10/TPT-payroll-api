from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class DepartmentBase(PayrollBase):
    code: str  # required
    name: str  # required
    description: Optional[str] = None


class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime


class DepartmentsRead(PayrollBase):
    count: int
    data: list[DepartmentRead] = []


class DepartmentUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentPagination(Pagination):
    items: List[DepartmentRead] = []

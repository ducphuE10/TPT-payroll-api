from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class DepartmentBase(PayrollBase):
    code: str
    name: str
    description: Optional[str] = None
    created_by: str


class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime


class DepartmentsRead(PayrollBase):
    data: list[DepartmentRead] = []


class DepartmentUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    created_by: Optional[str] = None


class DepartmentPagination(Pagination):
    items: List[DepartmentRead] = []

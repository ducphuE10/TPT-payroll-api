from datetime import datetime
from typing import List

from payroll.utils.models import Pagination, PayrollBase


class PayrollManagementBase(PayrollBase):
    employee_id: int  # required
    value: float  # required
    month: int  # required
    year: int


class PayrollManagementRead(PayrollManagementBase):
    id: int
    created_at: datetime


class PayrollManagementsRead(PayrollBase):
    count: int
    data: list[PayrollManagementRead] = []


class PayrollManagementCreate(PayrollBase):
    employee_id: int  # required
    month: int  # required
    year: int


class PayrollManagementBPagination(Pagination):
    items: List[PayrollManagementRead] = []

from datetime import datetime, date
from typing import List, Optional

from payroll.employees.schemas import EmployeeBase
from payroll.utils.models import PaymentMethod, Status
from payroll.utils.models import Pagination, PayrollBase


class ContractBase(PayrollBase):
    code: str  # required
    name: str  # required
    status: Status  # required
    description: Optional[str] = None
    employee_code: str  # required
    type_code: str  # required
    ct_date: date  # required
    ct_code: str  # required
    sign_date: date  # required
    start_date: date  # required
    end_date: date  # required
    is_current: bool  # required
    active_from: date  # required
    payment_method: PaymentMethod  # required
    attachments: Optional[str] = None
    salary: float  # required
    basic_salary: float  # required


class ContractRead(ContractBase):
    id: int
    created_at: datetime
    employee: EmployeeBase


class ContractsRead(PayrollBase):
    data: list[ContractRead] = []


class ContractCreate(ContractBase):
    created_by: Optional[str] = None


class ContractUpdate(ContractBase):
    pass


class ContractPagination(Pagination):
    items: List[ContractRead] = []

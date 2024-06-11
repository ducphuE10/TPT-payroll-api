from datetime import datetime
from typing import List, Optional

from payroll.utils_models import InsurancePolicy, TaxPolicy
from payroll.utils_models import Pagination, PayrollBase


class ContractTypeBase(PayrollBase):
    code: str
    name: str
    description: str
    number_of_months: int
    note: Optional[str] = None
    created_by: str
    is_probation: bool
    tax_policy: TaxPolicy
    insurance_policy: InsurancePolicy
    template: bytes


class ContractTypeRead(ContractTypeBase):
    id: int
    created_at: datetime


class ContractTypesRead(PayrollBase):
    data: list[ContractTypeRead] = []


class ContractTypeCreate(ContractTypeBase):
    created_by: Optional[str] = None


class ContractTypePagination(Pagination):
    items: List[ContractTypeRead] = []

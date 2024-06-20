from datetime import datetime
from typing import List, Optional

from payroll.utils.models import InsuranceType, TaxType
from payroll.utils.models import Pagination, PayrollBase


class ContractTypeBase(PayrollBase):
    code: str  # required
    name: str  # required
    description: Optional[str] = None
    number_of_months: int  # required
    note: Optional[str] = None
    is_probation: bool  # required
    tax_policy: TaxType  # required
    insurance_policy: InsuranceType  # required
    template: bytes
    created_by: str  # required


class ContractTypeRead(ContractTypeBase):
    id: int
    created_at: datetime


class ContractTypesRead(PayrollBase):
    data: list[ContractTypeRead] = []


class ContractTypeCreate(ContractTypeBase):
    created_by: Optional[str] = None


class ContractTypePagination(Pagination):
    items: List[ContractTypeRead] = []

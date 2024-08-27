from datetime import datetime
from typing import List, Optional


from payroll.insurances.schemas import InsurancePolicyRead
from payroll.taxes.schemas import TaxPolicyRead
from payroll.utils.models import Pagination, PayrollBase


class ContractTypeBase(PayrollBase):
    code: str  # required
    name: str  # required
    description: Optional[str] = None
    number_of_months: int  # required
    note: Optional[str] = None
    is_probation: bool  # required
    template: Optional[str] = None  # url to the file
    created_by: str  # required


class ContractTypeRead(ContractTypeBase):
    id: int
    created_at: datetime
    tax_policy: TaxPolicyRead
    insurance_policy: InsurancePolicyRead


class ContractTypesRead(PayrollBase):
    data: list[ContractTypeRead] = []


class ContractTypeCreate(ContractTypeBase):
    tax_policy_id: int  # required
    insurance_policy_id: int  # required


class ContractTypePagination(Pagination):
    items: List[ContractTypeRead] = []

from datetime import datetime
from typing import List, Optional
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, LargeBinary

from payroll.database.core import Base
from payroll.models import Pagination, PayrollBase, TimeStampMixin


class TaxPolicy(str, Enum):
    TPolicy1 = "tax_policy_1"
    TPolicy2 = "tax_policy_2"


class InsurancePolicy(str, Enum):
    IPolicy1 = "insurance_policy_1"
    IPolicy2 = "insurance_policy_2"


class PayrollContractType(Base, TimeStampMixin):
    __tablename__ = "contracttypes"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255))
    number_of_months: Mapped[int] = mapped_column()
    note: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))
    is_probation: Mapped[bool] = mapped_column()
    tax_policy: Mapped[TaxPolicy]
    insurance_policy: Mapped[InsurancePolicy]
    template: Mapped[bytes] = mapped_column(LargeBinary)
    created_by: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"ContractType (name={self.name!r})"


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


# class ContractTypeUpdate(PayrollBase):
#     explain: Optional[str] = None
#     month: Optional[int] = None
#     probation: Optional[bool] = None
#     tax_policy: Optional[TaxPolicy] = None
#     insurance_policy: Optional[InsurancePolicy] = None


class ContractTypeCreate(ContractTypeBase):
    created_by: Optional[str] = None


class ContractTypePagination(Pagination):
    items: List[ContractTypeRead] = []

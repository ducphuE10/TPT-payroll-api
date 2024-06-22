from datetime import datetime
from typing import Optional

from pydantic.types import confloat

from payroll.utils.models import InsuranceType, PayrollBase

PercentageType = confloat(ge=0.0, le=100.0)


class InsurancePolicyRead(PayrollBase):
    id: int
    code: str
    name: str
    based_on: InsuranceType
    description: Optional[str] = None
    is_active: bool
    company_percentage: PercentageType
    employee_percentage: PercentageType
    created_at: datetime
    updated_at: datetime


class InsurancePoliciesRead(PayrollBase):
    data: list[InsurancePolicyRead] = []


class InsurancePolicyCreate(PayrollBase):
    code: str  # required
    name: str  # required
    based_on: InsuranceType  # required
    description: Optional[str] = None
    is_active: Optional[bool] = True
    company_percentage: PercentageType
    employee_percentage: PercentageType


class InsurancePolicyUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    company_percentage: Optional[PercentageType] = None
    employee_percentage: Optional[PercentageType] = None

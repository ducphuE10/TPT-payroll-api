from datetime import datetime
from typing import Optional

from pydantic.types import confloat

from app.utils.models import PayrollBase

PercentageType = confloat(ge=0.0, le=100.0)


class InsurancePolicyRead(PayrollBase):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    company_percentage: PercentageType
    employee_percentage: PercentageType
    created_at: datetime


class InsurancePoliciesRead(PayrollBase):
    data: list[InsurancePolicyRead] = []


class InsurancePolicyCreate(PayrollBase):
    code: str  # required
    name: str  # required
    description: Optional[str] = None
    company_percentage: PercentageType
    employee_percentage: PercentageType


class InsurancePolicyUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None
    company_percentage: Optional[PercentageType] = None
    employee_percentage: Optional[PercentageType] = None

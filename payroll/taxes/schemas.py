from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import confloat
from pydantic import AfterValidator
from payroll.utils.models import PayrollBase, TaxType


def check_percentage_common(v, info):
    if "tax_type" in info.data:
        if v is not None and info.data["tax_type"] == TaxType.Progressive:
            raise ValueError("percentage must be None when tax_type is progressive")
        if v is None and info.data["tax_type"] == TaxType.Fixed:
            raise ValueError("percentage must not be None when tax_type is fixed")

    return v


def change_percentage(v, info):
    if "tax_type" in info.data:
        if info.data["tax_type"] == TaxType.Progressive:
            return None
    return v


class TaxPolicyRead(PayrollBase):
    id: int
    code: str
    name: str
    tax_type: TaxType
    description: Optional[str] = None
    is_active: bool
    percentage: Annotated[
        Optional[confloat(ge=0.0, le=100.0)], AfterValidator(change_percentage)
    ] = None
    created_at: datetime
    updated_at: datetime


class TaxPoliciesRead(PayrollBase):
    data: list[TaxPolicyRead] = []


class TaxPolicyCreate(PayrollBase):
    code: str  # required
    name: str  # required
    tax_type: TaxType  # required
    description: Optional[str] = None
    is_active: Optional[bool] = True
    percentage: Annotated[
        Optional[confloat(ge=0.0, le=100.0)], AfterValidator(check_percentage_common)
    ] = None


class TaxPolicyUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    percentage: Annotated[
        Optional[confloat(ge=0.0, le=100.0)], AfterValidator(check_percentage_common)
    ] = None

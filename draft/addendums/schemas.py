from datetime import datetime, date
from typing import List, Optional

# from payroll.contract_benefit_assocs.schemas import CBAssocsRead
from payroll.contract_histories.schemas import ContractBase
from payroll.utils.models import PaymentMethod, Status
from payroll.utils.models import Pagination, PayrollBase


class AddendumBase(PayrollBase):
    code: str  # required
    name: str  # required
    status: Status  # required
    description: Optional[str] = None
    contract_id: str  # required
    addendum_date: date  # required
    signed_date: date  # required
    start_date: date  # required
    payment_method: PaymentMethod  # required
    new_position_id: int
    new_salary: float  # required
    new_basic_salary: float  # required
    new_meal_benefit: float
    new_transportation_benefit: float
    new_housing_benefit: float
    new_toxic_benefit: float
    new_phone_benefit: float
    new_attendant_benefit: float
    template: Optional[str] = None


class AddendumRead(AddendumBase):
    id: int
    created_at: datetime
    contract: ContractBase


class AddendumsRead(PayrollBase):
    count: int
    data: list[AddendumRead] = []


class AddendumCreate(PayrollBase):
    code: str  # required
    name: str  # required
    status: Status  # required
    description: Optional[str] = None
    contract_id: str  # required
    addendum_date: date  # required
    signed_date: date  # required
    start_date: date  # required
    payment_method: Optional[PaymentMethod] = None
    new_position_id: Optional[int] = None
    new_salary: Optional[float] = None
    new_basic_salary: Optional[float] = None
    new_meal_benefit: Optional[float] = None
    new_transportation_benefit: Optional[float] = None
    new_housing_benefit: Optional[float] = None
    new_toxic_benefit: Optional[float] = None
    new_phone_benefit: Optional[float] = None
    new_attendant_benefit: Optional[float] = None
    template: Optional[str] = None
    created_by: Optional[str] = None


class AddendumUpdate(PayrollBase):
    name: Optional[str] = None
    status: Optional[Status] = None
    description: Optional[str] = None
    addendum_date: Optional[date] = None
    signed_date: Optional[date] = None
    start_date: Optional[date] = None
    payment_method: Optional[PaymentMethod] = None
    new_position_id: Optional[int] = None
    new_salary: Optional[float] = None
    new_basic_salary: Optional[float] = None
    new_meal_benefit: Optional[float] = None
    new_transportation_benefit: Optional[float] = None
    new_housing_benefit: Optional[float] = None
    new_toxic_benefit: Optional[float] = None
    new_phone_benefit: Optional[float] = None
    new_attendant_benefit: Optional[float] = None
    template: Optional[str] = None


class AddendumPagination(Pagination):
    items: List[AddendumRead] = []

from datetime import datetime, date
from typing import List, Optional

# from payroll.contract_benefit_assocs.schemas import CBAssocsRead
from payroll.employees.schemas import EmployeeBase
from payroll.utils.models import PaymentMethod, Status
from payroll.utils.models import Pagination, PayrollBase


class ContractBase(PayrollBase):
    code: str  # required
    name: str  # required
    status: Status  # required
    description: Optional[str] = None
    number_of_months: int  # required
    is_probation: bool
    employee_code: str  # required
    ct_date: date  # required
    ct_code: str  # required
    signed_date: date  # required
    start_date: date  # required
    end_date: Optional[date]  # required
    is_current: bool  # required
    active_from: date  # required
    payment_method: PaymentMethod  # required
    attachments: Optional[str] = None
    salary: float  # required
    basic_salary: float  # required
    meal_benefit: float
    transportation_benefit: float
    housing_benefit: float
    toxic_benefit: float
    phone_benefit: float
    attendant_benefit: float
    template: Optional[str] = None


class ContractRead(ContractBase):
    id: int
    created_at: datetime
    employee: EmployeeBase


# class ContractWithBenefitRead(PayrollBase):
#     contract_in: ContractBase
#     benefits_list_in: Optional[CBAssocsRead] = None


class ContractsRead(PayrollBase):
    data: list[ContractRead] = []


class ContractCreate(ContractBase):
    created_by: Optional[str] = None


class ContractUpdate(PayrollBase):
    name: Optional[str] = None
    status: Optional[Status] = None
    description: Optional[str] = None
    number_of_months: Optional[str] = None
    is_probation: Optional[bool] = None
    employee_code: Optional[str] = None
    ct_date: Optional[date] = None
    ct_code: Optional[str] = None
    signed_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    active_from: Optional[date] = None
    payment_method: Optional[PaymentMethod] = None
    attachments: Optional[str] = None
    salary: Optional[float] = None
    basic_salary: Optional[float] = None
    meal_benefit: Optional[float] = None
    transportation_benefit: Optional[float] = None
    housing_benefit: Optional[float] = None
    toxic_benefit: Optional[float] = None
    phone_benefit: Optional[float] = None
    attendant_benefit: Optional[float] = None
    template: Optional[str] = None


class BenefitRead(PayrollBase):
    id: int
    meal_benefit: float
    transportation_benefit: float
    housing_benefit: float
    toxic_benefit: float
    phone_benefit: float
    attendant_benefit: float
    employee: EmployeeBase


class BenefitsRead(PayrollBase):
    count: int
    data: list[BenefitRead] = []


class ContractPagination(Pagination):
    items: List[ContractRead] = []

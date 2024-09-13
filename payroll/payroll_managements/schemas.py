from datetime import datetime
from typing import List, Optional

from payroll.employees.schemas import EmployeeBase
from payroll.utils.models import Pagination, PayrollBase


class PayrollManagementBase(PayrollBase):
    employee_id: int  # required
    contract_id: int
    net_income: float  # required
    month: int  # required
    year: int
    salary: float  # required
    work_days: float  # required
    work_days_salary: float
    overtime_1_5x_hours: Optional[float] = None
    overtime_1_5x_salary: Optional[float] = None
    overtime_2_0x_hours: Optional[float] = None
    overtime_2_0x_salary: Optional[float] = None
    transportation_benefit_salary: float
    attendant_benefit_salary: float
    housing_benefit_salary: float
    phone_benefit_salary: float
    meal_benefit_salary: float
    gross_income: float
    employee_insurance: Optional[float] = None
    company_insurance: Optional[float] = None
    no_tax_salary: float
    dependant_people: Optional[int] = None
    tax_salary: Optional[float] = None
    tax: Optional[float] = None
    total_deduction: Optional[float] = None


class PayrollManagementRead(PayrollManagementBase):
    id: int
    created_at: datetime
    employee: EmployeeBase


class PayrollManagementsRead(PayrollBase):
    count: int
    data: list[PayrollManagementRead] = []


class PayrollManagementCreate(PayrollBase):
    employee_id: int  # required
    month: int  # required
    year: int


class PayrollManagementDetail(PayrollManagementBase):
    pass


class PayrollManagementsCreate(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]
    month: int
    year: int


class PayrollManagementBPagination(Pagination):
    items: List[PayrollManagementRead] = []

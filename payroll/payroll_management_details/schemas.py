from datetime import datetime
from typing import List, Optional

from payroll.utils.models import Pagination, PayrollBase


class PayrollManagementDetailBase(PayrollBase):
    payroll_management_id: int  # required
    salary: float  # required
    work_days: float  # required
    work_days_salary: float
    overtime_1_5x_hours: Optional[float] = None
    overtime_1_5x_salary: Optional[float] = None
    overtime_2_0x_hours: Optional[float] = None
    overtime_2_0x_salary: Optional[float] = None
    travel_benefit_salary: float
    attendant_benefit_salary: float
    housing_benefit_salary: float
    phone_benefit_salary: float
    meal_benefit_salary: float
    gross_income: float
    employee_insurance: Optional[float] = None
    company_insurance: Optional[float] = None
    no_tax_salary: float
    dependant_people: Optional[float] = None
    tax_salary: Optional[float] = None
    tax: Optional[float] = None
    total_deduction: Optional[float] = None


class PayrollManagementDetailRead(PayrollManagementDetailBase):
    id: int
    created_at: datetime


class PayrollManagementDetailsRead(PayrollBase):
    count: int
    data: list[PayrollManagementDetailRead] = []


# class PayrollManagementDetailUpdate(PayrollBase):
#     name: Optional[str] = None
#     description: Optional[str] = None


class PayrollManagementDetailCreate(PayrollBase):
    pass


class PayrollManagementDetailBPagination(Pagination):
    items: List[PayrollManagementDetailRead] = []

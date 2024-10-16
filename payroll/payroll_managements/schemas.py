from datetime import datetime
from typing import List, Optional

from pydantic import field_validator

from payroll.employees.schemas import EmployeeBase
from payroll.utils.models import Pagination, PayrollBase


class PayrollManagementBase(PayrollBase):
    employee_id: int  # required
    contract_history_id: int
    insurance_policy_id: Optional[int] = None
    net_income: float  # required
    month: int  # required
    year: int
    salary: float  # required
    work_days_standard: float
    work_days: float  # required
    work_days_salary: float
    overtime_1_5x_hours: Optional[float] = None
    overtime_1_5x_salary: Optional[float] = None
    overtime_2_0x_hours: Optional[float] = None
    overtime_2_0x_salary: Optional[float] = None
    transportation_benefit_salary: float
    attendant_benefit_salary: float
    housing_benefit_salary: float
    toxic_benefit_salary: float
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

    @field_validator(
        "salary",
        "work_days_salary",
        "overtime_1_5x_salary",
        "overtime_2_0x_salary",
        "transportation_benefit_salary",
        "attendant_benefit_salary",
        "housing_benefit_salary",
        "toxic_benefit_salary",
        "phone_benefit_salary",
        "meal_benefit_salary",
        "gross_income",
        "employee_insurance",
        "company_insurance",
        "no_tax_salary",
        "tax_salary",
        "tax",
        "total_deduction",
        "net_income",
    )
    @classmethod
    def double(cls, v: float) -> int:
        return round(v, -3)


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
    work_days_standard: float
    apply_insurance: bool = False
    insurance_id: Optional[int] = None


class PayrollManagementDetail(PayrollManagementBase):
    pass


class PayrollManagementsCreate(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]
    month: int
    year: int
    work_days_standard: float
    apply_insurance: bool = False
    insurance_id: Optional[int] = None


class PayrollManagementBPagination(Pagination):
    items: List[PayrollManagementRead] = []

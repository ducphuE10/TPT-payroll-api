from datetime import datetime, date
from typing import List, Optional
from payroll.departments.schemas import DepartmentBase
from payroll.positions.schemas import PositionBase
from payroll.schedules.schemas import ScheduleBase
from payroll.utils.models import (
    Gender,
    Nationality,
    Pagination,
    PaymentMethod,
    PayrollBase,
)


class EmployeeBase(PayrollBase):
    code: str  # required
    name: str  # required
    date_of_birth: date  # required
    gender: Gender  # required
    nationality: Optional[Nationality] = None
    mst: str  # required
    cccd: str  # required
    cccd_date: Optional[date] = None
    cccd_place: Optional[str] = None
    permanent_addr: Optional[str] = None
    phone: Optional[str] = None
    # -----------------------
    department_id: int  # required
    position_id: int  # required
    is_probation: bool
    start_date: date
    end_date: Optional[date] = None
    salary: float
    meal_benefit: float
    transportation_benefit: float
    housing_benefit: float
    toxic_benefit: float
    phone_benefit: float
    attendant_benefit: float
    schedule_id: Optional[int] = None
    # -----------------------
    bank_account: Optional[str] = None
    bank_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    cv: Optional[bytes] = None
    note: Optional[str] = None


class EmployeeRead(EmployeeBase):
    id: int
    created_at: datetime
    department: DepartmentBase
    position: PositionBase
    schedule: Optional[ScheduleBase]


class EmployeesRead(PayrollBase):
    count: int
    data: list[EmployeeRead] = []


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeDelete(PayrollBase):
    id: int
    code: str
    name: str
    department: str
    position: str


class EmployeeUpdatePersonal(PayrollBase):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    nationality: Optional[Nationality] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    mst: Optional[str] = None
    cccd: Optional[str] = None
    cccd_date: Optional[date] = None
    cccd_place: Optional[str] = None
    permanent_addr: Optional[str] = None
    phone: Optional[str] = None
    schedule_id: Optional[int] = None
    payment_method: Optional[PaymentMethod] = None
    bank_account: Optional[str] = None
    bank_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    cv: Optional[bytes] = None
    note: Optional[str] = None


class EmployeeUpdateSalary(PayrollBase):
    name: Optional[str] = None
    is_probation: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    salary: Optional[float] = None
    meal_benefit: Optional[float] = None
    transportation_benefit: Optional[float] = None
    housing_benefit: Optional[float] = None
    toxic_benefit: Optional[float] = None
    phone_benefit: Optional[float] = None
    attendant_benefit: Optional[float] = None


class EmployeeImport(PayrollBase):
    code: str
    name: str
    gender: Gender
    department_code: str
    position_code: str
    mst: str
    date_of_birth: date
    cccd: str
    cccd_date: Optional[date] = None
    cccd_place: Optional[str] = None
    permanent_addr: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_probation: bool
    salary: float
    housing_benefit: float
    attendant_benefit: float
    transportation_benefit: float
    meal_benefit: float
    toxic_benefit: float
    phone_benefit: float


class EmployeePagination(Pagination):
    items: List[EmployeeRead] = []


class EmployeesScheduleUpdate(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]


class EmployeesScheduleUpdateRead(PayrollBase):
    data: EmployeesRead


class BenefitRead(PayrollBase):
    id: int
    code: str
    name: str
    meal_benefit: float
    transportation_benefit: float
    housing_benefit: float
    toxic_benefit: float
    phone_benefit: float
    attendant_benefit: float


class BenefitsRead(PayrollBase):
    count: int
    data: list[BenefitRead] = []

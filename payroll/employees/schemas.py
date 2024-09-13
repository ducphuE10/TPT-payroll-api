from datetime import datetime, date
from typing import List, Optional
from payroll.departments.schemas import DepartmentBase
from payroll.positions.schemas import PositionBase
from payroll.schedules.schemas import ScheduleBase
from payroll.utils.models import Gender, Nationality, Pagination, PayrollBase


class EmployeeBase(PayrollBase):
    code: str  # required
    name: str  # required
    date_of_birth: date  # required
    gender: Gender  # required
    nationality: Optional[Nationality] = None
    ethnic: Optional[str] = None
    religion: Optional[str] = None
    cccd: str  # required
    cccd_date: Optional[date] = None
    cccd_place: Optional[str] = None
    domicile: Optional[str] = None
    permanent_addr: Optional[str] = None
    temp_addr: Optional[str] = None
    phone: Optional[str] = None
    academic_level: Optional[str] = None
    bank_account: Optional[str] = None
    bank_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    mst: str  # required
    kcb_number: Optional[str] = None
    hospital_info: Optional[str] = None
    start_work: Optional[date] = None
    note: Optional[str] = None
    department_id: int  # required
    position_id: int  # required
    schedule_id: Optional[int] = None
    overtime_schedule_id: Optional[int] = None
    email: Optional[str] = None
    cv: Optional[bytes] = None


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


class EmployeeUpdate(PayrollBase):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    nationality: Optional[Nationality] = None
    ethnic: Optional[str] = None
    religion: Optional[str] = None
    cccd: Optional[str] = None
    cccd_date: Optional[date] = None
    cccd_place: Optional[str] = None
    domicile: Optional[str] = None
    permanent_addr: Optional[str] = None
    temp_addr: Optional[str] = None
    phone: Optional[str] = None
    academic_level: Optional[str] = None
    bank_account: Optional[str] = None
    bank_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    mst: Optional[str] = None
    kcb_number: Optional[str] = None
    hospital_info: Optional[str] = None
    start_work: Optional[date] = None
    note: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    schedule_id: Optional[int] = None
    overtime_schedule_id: Optional[int] = None
    email: Optional[str] = None
    cv: Optional[bytes] = None


class EmployeeImport(PayrollBase):
    code: str = None
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    nationality: Optional[Nationality] = None
    cccd: Optional[str] = None
    cccd_date: Optional[date] = None
    cccd_place: Optional[str] = None
    domicile: Optional[str] = None
    permanent_addr: Optional[str] = None
    phone: Optional[str] = None
    bank_account: Optional[str] = None
    bank_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    mst: Optional[str] = None
    department_code: Optional[str] = None
    position_code: Optional[str] = None


class EmployeePagination(Pagination):
    items: List[EmployeeRead] = []


class EmployeesScheduleUpdate(PayrollBase):
    apply_all: bool = False
    list_emp: List[int]


class EmployeesScheduleUpdateRead(PayrollBase):
    data: EmployeesRead

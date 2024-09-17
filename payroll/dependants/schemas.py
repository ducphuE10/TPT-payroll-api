from datetime import datetime, date
from typing import List, Optional
from payroll.utils.models import Gender, Nationality, Pagination, PayrollBase


class DependantBase(PayrollBase):
    code: str  # required
    name: str  # required
    employee_id: int
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
    note: Optional[str] = None
    email: Optional[str] = None


class DependantRead(DependantBase):
    id: int
    created_at: datetime


class DependantsRead(PayrollBase):
    count: int
    data: list[DependantRead] = []


class DependantCreate(DependantBase):
    pass


class DependantUpdate(PayrollBase):
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
    note: Optional[str] = None
    email: Optional[str] = None


class DependantPagination(Pagination):
    items: List[DependantRead] = []

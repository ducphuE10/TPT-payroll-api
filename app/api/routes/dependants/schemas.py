from datetime import datetime, date
from typing import List, Optional
from app.api.routes.employees.schemas import EmployeeBase
from app.utils.models import (
    DependantRelationship,
    IDDocType,
    Pagination,
    PayrollBase,
)


class DependantBase(PayrollBase):
    code: str  # required
    name: str  # required
    employee_id: int
    date_of_birth: date  # required
    phone: Optional[str] = None
    mst: str  # required
    id_doc_type: IDDocType
    doc_number: str
    relationship: DependantRelationship
    deduction_from: date
    deduction_to: date
    note: Optional[str] = None
    company_id: int


class DependantRead(DependantBase):
    id: int
    created_at: datetime
    employee: EmployeeBase


class DependantsRead(PayrollBase):
    count: int
    data: list[DependantRead] = []


class DependantCreate(DependantBase):
    pass


class DependantUpdate(PayrollBase):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    mst: Optional[str] = None
    id_doc_type: Optional[IDDocType] = None
    doc_number: Optional[str] = None
    relationship: Optional[DependantRelationship] = None
    deduction_from: Optional[date] = None
    deduction_to: Optional[date] = None
    note: Optional[str] = None
    company_id: Optional[int] = None


class DependantImport(PayrollBase):
    code: str
    name: str
    employee_code: str
    date_of_birth: date
    id_doc_type: IDDocType
    doc_number: str
    relationship: DependantRelationship
    deduction_from: date
    deduction_to: date
    mst: str


class DependantPagination(Pagination):
    items: List[DependantRead] = []

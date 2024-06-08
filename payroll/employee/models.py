from datetime import datetime, date
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, LargeBinary, String
from payroll.database.core import Base
from payroll.department.models import PayrollDepartment
from payroll.models import Pagination, PayrollBase, TimeStampMixin
from payroll.position.models import PayrollPosition


class Gender(str, Enum):
    Male = "male"
    Female = "female"


class Nationality(str, Enum):
    VN = "Vietnam"
    JP = "Japan"


class PayrollEmployee(Base, TimeStampMixin):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    date_of_birth: Mapped[Optional[date]]
    gender: Mapped[Gender]
    nationality: Mapped[Optional[Nationality]]
    ethnic: Mapped[Optional[str]] = mapped_column(String(10))
    religion: Mapped[Optional[str]] = mapped_column(String(30))
    cccd: Mapped[Optional[str]] = mapped_column(String(30))
    cccd_date: Mapped[Optional[date]]
    cccd_place: Mapped[Optional[str]] = mapped_column(String(255))
    domicile: Mapped[Optional[str]] = mapped_column(String(255))
    permanent_addr: Mapped[Optional[str]] = mapped_column(String(255))
    temp_addr: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    academic_level: Mapped[Optional[str]] = mapped_column(String(30))
    bank_account: Mapped[Optional[str]] = mapped_column(String(30))
    bank_holder_name: Mapped[Optional[str]] = mapped_column(String(30))
    bank_name: Mapped[Optional[str]] = mapped_column(String(30))
    mst: Mapped[str] = mapped_column(String(30))
    kcb_number: Mapped[Optional[str]] = mapped_column(String(30))
    hospital_info: Mapped[Optional[str]] = mapped_column(String(255))
    start_work: Mapped[Optional[date]]
    note: Mapped[Optional[str]] = mapped_column(String(255))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    cv: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    department: Mapped["PayrollDepartment"] = relationship(
        "PayrollDepartment", back_populates="employees"
    )
    position: Mapped["PayrollPosition"] = relationship(
        "PayrollPosition", back_populates="employees"
    )

    def __repr__(self) -> str:
        return f"Employee (name={self.name!r})"


class EmployeeBase(PayrollBase):
    code: str
    name: str
    date_of_birth: Optional[date] = None
    gender: Gender
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
    mst: str
    kcb_number: Optional[str] = None
    hospital_info: Optional[str] = None
    start_work: Optional[date] = None
    note: Optional[str] = None
    department_id: int
    position_id: int
    email: Optional[str] = None
    cv: Optional[bytes] = None


class EmployeeRead(EmployeeBase):
    id: int
    created_at: datetime


class EmployeesRead(PayrollBase):
    data: list[EmployeeRead] = []


class EmployeeUpdate(PayrollBase):
    code: Optional[str] = None
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
    department_id: Optional[int] = None
    position_id: Optional[int] = None


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


class EmployeeCreate(EmployeeBase):
    pass


class PositionPagination(Pagination):
    items: List[EmployeeRead] = []

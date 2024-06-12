from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, LargeBinary
from sqlalchemy.orm import relationship

from payroll.database.core import Base
from payroll.utils.models import (
    Gender,
    InsurancePolicy,
    Nationality,
    TaxPolicy,
    TimeStampMixin,
)


class PayrollContractType(Base, TimeStampMixin):
    __tablename__ = "contracttypes"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    number_of_months: Mapped[int] = mapped_column()
    note: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))
    is_probation: Mapped[bool] = mapped_column()
    tax_policy: Mapped[TaxPolicy]
    insurance_policy: Mapped[InsurancePolicy]
    template: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    created_by: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"ContractType (name={self.name!r})"


class PayrollDepartment(Base, TimeStampMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))
    employees: Mapped[List["PayrollEmployee"]] = relationship(
        "PayrollEmployee", back_populates="department"
    )

    def __repr__(self) -> str:
        return f"Department (name={self.name!r})"


class PayrollPosition(Base, TimeStampMixin):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))
    employees: Mapped[List["PayrollEmployee"]] = relationship(
        "PayrollEmployee", back_populates="position"
    )

    def __repr__(self) -> str:
        return f"Position (name={self.name!r})"


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

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
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    description: Mapped[Optional[str]] = mapped_column(String(255))
    number_of_months: Mapped[int] = mapped_column()  # required
    note: Mapped[Optional[str]] = mapped_column(String(255))
    is_probation: Mapped[bool] = mapped_column()  # required
    tax_policy: Mapped[TaxPolicy]  # required
    insurance_policy: Mapped[InsurancePolicy]  # required
    template: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    created_by: Mapped[str] = mapped_column(String(30))  # required

    def __repr__(self) -> str:
        return f"ContractType (name={self.name!r})"


class PayrollDepartment(Base, TimeStampMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))  # required
    employees: Mapped[List["PayrollEmployee"]] = relationship(
        "PayrollEmployee", back_populates="department"
    )

    def __repr__(self) -> str:
        return f"Department (name={self.name!r})"


class PayrollPosition(Base, TimeStampMixin):
    __tablename__ = "positions"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    description: Mapped[Optional[str]] = mapped_column(String(255))
    employees: Mapped[List["PayrollEmployee"]] = relationship(
        "PayrollEmployee", back_populates="position"
    )

    def __repr__(self) -> str:
        return f"Position (name={self.name!r})"


class PayrollEmployee(Base, TimeStampMixin):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    date_of_birth: Mapped[date]  # required
    gender: Mapped[Gender]  # required
    nationality: Mapped[Optional[Nationality]]
    ethnic: Mapped[Optional[str]] = mapped_column(String(10))
    religion: Mapped[Optional[str]] = mapped_column(String(30))
    cccd: Mapped[str] = mapped_column(String(30), unique=True)  # required
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
    mst: Mapped[str] = mapped_column(String(30), unique=True)  # required
    kcb_number: Mapped[Optional[str]] = mapped_column(String(30))
    hospital_info: Mapped[Optional[str]] = mapped_column(String(255))
    start_work: Mapped[Optional[date]]
    note: Mapped[Optional[str]] = mapped_column(String(255))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))  # required
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))  # required
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

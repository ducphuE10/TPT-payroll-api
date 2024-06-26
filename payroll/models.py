from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, ForeignKey, String, LargeBinary, Float
from sqlalchemy.orm import relationship

from payroll.database.core import Base
from payroll.utils.models import (
    Gender,
    InsuranceType,
    Nationality,
    TaxType,
    PaymentMethod,
    Status,
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
    tax_policy_id: Mapped[int] = mapped_column(
        ForeignKey("tax_policies.id")
    )  # required
    tax_policy: Mapped["TaxPolicy"] = relationship("TaxPolicy", backref="contracttypes")
    insurance_policy_id: Mapped[int] = mapped_column(
        ForeignKey("insurance_policies.id")
    )  # required
    insurance_policy: Mapped["InsurancePolicy"] = relationship(
        "InsurancePolicy", backref="contracttypes"
    )
    template: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    created_by: Mapped[str] = mapped_column(String(30))  # required

    def __repr__(self) -> str:
        return f"ContractType (name={self.name!r})"


class PayrollContract(Base, TimeStampMixin):
    __tablename__ = "contracts"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    status: Mapped[Status]  # required
    description: Mapped[Optional[str]] = mapped_column(String(255))
    type_code: Mapped[str] = mapped_column(ForeignKey("contracttypes.code"))  # required
    ct_date: Mapped[date]  # required
    ct_code: Mapped[str] = mapped_column(String(30))  # required
    employee_code: Mapped[str] = mapped_column(ForeignKey("employees.code"))  # required
    employee: Mapped["PayrollEmployee"] = relationship(
        "PayrollEmployee",
        backref="contracts",
    )
    signed_date: Mapped[date]  # required
    start_date: Mapped[date]  # required
    end_date: Mapped[date]  # required
    is_current: Mapped[bool]  # required
    active_from: Mapped[date]  # required
    payment_method: Mapped[PaymentMethod]  # required
    attachments: Mapped[Optional[str]] = mapped_column(String(255))
    salary: Mapped[float]  # required
    basic_salary: Mapped[float]  # required
    created_by: Mapped[str] = mapped_column(String(30))  # required

    def __repr__(self) -> str:
        return f"Contract (name={self.name!r})"


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

    attendances: Mapped[List["PayrollAttendance"]] = relationship(
        "PayrollAttendance", back_populates="employee"
    )
    department: Mapped["PayrollDepartment"] = relationship(
        "PayrollDepartment", back_populates="employees"
    )
    position: Mapped["PayrollPosition"] = relationship(
        "PayrollPosition", back_populates="employees"
    )

    def __repr__(self) -> str:
        return f"Employee (name={self.name!r})"


class TaxPolicy(Base, TimeStampMixin):
    __tablename__ = "tax_policies"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    tax_type: Mapped[TaxType]
    description: Mapped[Optional[str]] = mapped_column(String(255))
    percentage: Mapped[Optional[float]] = mapped_column(Float)
    is_active: Mapped[bool]

    def __repr__(self) -> str:
        return f"TaxPolicy(name={self.name!r})"


class InsurancePolicy(Base, TimeStampMixin):
    __tablename__ = "insurance_policies"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    based_on: Mapped[InsuranceType]
    company_percentage: Mapped[float] = mapped_column(Float)  # required
    employee_percentage: Mapped[float] = mapped_column(Float)  # required
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool]

    def __repr__(self) -> str:
        return f"InsurancePolicy(name={self.name!r})"


class PayrollAttendance(Base, TimeStampMixin):
    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(primary_key=True)  # required
    work_hours: Mapped[Optional[float]]
    overtime: Mapped[Optional[float]]
    holiday: Mapped[Optional[bool]] = mapped_column(Boolean)
    afm: Mapped[Optional[bool]] = mapped_column(Boolean)
    wait4work: Mapped[Optional[bool]] = mapped_column(Boolean)
    day_attendance: Mapped[date]  # required
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))  # required

    employee: Mapped["PayrollEmployee"] = relationship(
        "PayrollEmployee", back_populates="attendances"
    )

    def __repr__(self) -> str:
        return f"Attendance (employee_name={self.employee_id!r}, work_days={self.work_hours!r}, date={self.day_attendance!r})"

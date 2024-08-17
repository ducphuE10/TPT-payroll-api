from datetime import date, time
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey,
    String,
    LargeBinary,
    Float,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from payroll.database.core import Base
from payroll.utils.models import (
    BenefitReplay,
    Day,
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

    benefits: Mapped[List["PayrollCBAssoc"]] = relationship()

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
    created_by: Mapped[str] = mapped_column(String(30))  # required

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
    schedule_id: Mapped[Optional[int]] = mapped_column(ForeignKey("schedules.id"))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    cv: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    created_by: Mapped[str] = mapped_column(String(30))  # required

    attendances: Mapped[List["PayrollAttendance"]] = relationship(
        "PayrollAttendance", back_populates="employee", cascade="all, delete-orphan"
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
    created_by: Mapped[str] = mapped_column(String(30))  # required

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
    created_by: Mapped[str] = mapped_column(String(30))  # required

    def __repr__(self) -> str:
        return f"InsurancePolicy(name={self.name!r})"


class PayrollAttendance(Base, TimeStampMixin):
    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(primary_key=True)  # required
    work_hours: Mapped[float]  # required
    day_attendance: Mapped[date]  # required
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE")
    )  # required
    created_by: Mapped[str] = mapped_column(String(30))  # required

    employee: Mapped["PayrollEmployee"] = relationship(
        "PayrollEmployee", back_populates="attendances"
    )

    __table_args__ = (
        UniqueConstraint(
            "employee_id", "day_attendance", name="uq_employee_attendance"
        ),
    )

    def __repr__(self) -> str:
        return f"Attendance (employee_id={self.employee_id!r}, work_hours={self.work_hours!r}, day_attendance={self.day_attendance!r})"


class PayrollScheduleDetail(Base, TimeStampMixin):
    __tablename__ = "schedule_details"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE")
    )
    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id"))
    day: Mapped[Day]  # 'mon', 'tue', etc.
    created_by: Mapped[str] = mapped_column(String(30))  # required

    shift: Mapped["PayrollShift"] = relationship()
    schedule: Mapped["PayrollSchedule"] = relationship(
        "PayrollSchedule", back_populates="shifts"
    )

    __table_args__ = (
        UniqueConstraint(
            "schedule_id", "shift_id", "day", name="uq_schedule_shift_day"
        ),
    )

    def __repr__(self) -> str:
        return f"Schedule detail (schedule_id={self.schedule_id!r}, shift_id={self.shift_id!r}, day={self.day!r})"


class PayrollShift(Base, TimeStampMixin):
    __tablename__ = "shifts"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    standard_work_hours: Mapped[float]  # required
    checkin: Mapped[Optional[time]] = mapped_column(Time)
    earliest_checkin: Mapped[Optional[time]] = mapped_column(Time)
    latest_checkin: Mapped[Optional[time]] = mapped_column(Time)
    checkout: Mapped[Optional[time]] = mapped_column(Time)
    earliest_checkout: Mapped[Optional[time]] = mapped_column(Time)
    latest_checkout: Mapped[Optional[time]] = mapped_column(Time)
    created_by: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Shift (name={self.name!r}, code={self.code!r}, checkin={self.checkin!r}, checkout={self.checkout!r})"


class PayrollSchedule(Base, TimeStampMixin):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    shift_per_day: Mapped[int]
    created_by: Mapped[str] = mapped_column(String(30))  # required

    shifts: Mapped[List["PayrollScheduleDetail"]] = relationship(
        "PayrollScheduleDetail", cascade="all, delete-orphan", back_populates="schedule"
    )

    def __repr__(self) -> str:
        return f"Schedule (name={self.name!r}, code={self.code!r})"


class PayrollBenefit(Base, TimeStampMixin):
    __tablename__ = "benefits"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(10), unique=True)  # required
    name: Mapped[str] = mapped_column(String(30))  # required
    replay: Mapped[BenefitReplay] = mapped_column(default=BenefitReplay.DAILY)
    count_salary: Mapped[bool]
    value: Mapped[float]
    description: Mapped[Optional[str]]
    created_by: Mapped[str] = mapped_column(String(30))  # required

    def __repr__(self) -> str:
        return f"Benefit (name={self.name!r}, code={self.code!r})"


class PayrollCBAssoc(Base, TimeStampMixin):
    __tablename__ = "contract_benefit_association"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id"), primary_key=True
    )
    benefit_id: Mapped[int] = mapped_column(ForeignKey("benefits.id"), primary_key=True)

    benefit: Mapped["PayrollBenefit"] = relationship()

    def __repr__(self) -> str:
        return f"CBAssoc (contract_id={self.contract_id!r}, benefit_id={self.benefit_id!r})"

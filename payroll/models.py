from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey,
    String,
    LargeBinary,
    Float,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from payroll.database.core import Base
from payroll.utils.models import (
    ContractHistoryType,
    Day,
    DependantRelationship,
    Gender,
    IDDocType,
    Nationality,
    PaymentMethod,
    TimeStampMixin,
)


class PayrollDepartment(Base, TimeStampMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(30), unique=True)  # required
    name: Mapped[str] = mapped_column(String(50))  # required
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
    code: Mapped[str] = mapped_column(String(30), unique=True)  # required
    name: Mapped[str] = mapped_column(String(50))  # required
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
    code: Mapped[str] = mapped_column(String(30), unique=True)  # required
    name: Mapped[str] = mapped_column(String(50))  # required
    date_of_birth: Mapped[date]  # required
    gender: Mapped[Gender]  # required
    nationality: Mapped[Optional[Nationality]]
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))  # required
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))  # required
    mst: Mapped[str] = mapped_column(String(10), unique=True)  # required
    cccd: Mapped[str] = mapped_column(String(12), unique=True)  # required
    cccd_date: Mapped[date]
    cccd_place: Mapped[str] = mapped_column(String(255))
    permanent_addr: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    is_probation: Mapped[bool] = mapped_column()  # required
    start_date: Mapped[date]  # required
    end_date: Mapped[Optional[date]]  # required
    is_offboard: Mapped[bool]
    salary: Mapped[float]  # required
    meal_benefit: Mapped[float]
    transportation_benefit: Mapped[float]
    housing_benefit: Mapped[float]
    toxic_benefit: Mapped[float]
    phone_benefit: Mapped[float]
    attendant_benefit: Mapped[float]
    schedule_id: Mapped[Optional[int]] = mapped_column(ForeignKey("schedules.id"))
    payment_method: Mapped[Optional[PaymentMethod]]
    bank_account: Mapped[Optional[str]] = mapped_column(String(30))
    bank_holder_name: Mapped[Optional[str]] = mapped_column(String(30))
    bank_name: Mapped[Optional[str]] = mapped_column(String(30))
    cv: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    note: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))  # required

    department: Mapped["PayrollDepartment"] = relationship(
        "PayrollDepartment",
        backref="departments",
    )
    position: Mapped["PayrollPosition"] = relationship(
        "PayrollPosition",
        backref="positions",
    )
    schedule: Mapped[Optional["PayrollSchedule"]] = relationship(
        "PayrollSchedule",
        backref="schedules",
    )
    department: Mapped["PayrollDepartment"] = relationship(
        "PayrollDepartment", back_populates="employees"
    )
    position: Mapped["PayrollPosition"] = relationship(
        "PayrollPosition", back_populates="employees"
    )
    attendances: Mapped[List["PayrollAttendance"]] = relationship(
        "PayrollAttendance", back_populates="employee", cascade="all, delete-orphan"
    )
    overtimes: Mapped[List["PayrollOvertime"]] = relationship(
        "PayrollOvertime", back_populates="employee", cascade="all, delete-orphan"
    )
    payroll_managements: Mapped[List["PayrollPayrollManagement"]] = relationship(
        "PayrollPayrollManagement", back_populates="employee"
    )
    contract_histories: Mapped[List["PayrollContractHistory"]] = relationship(
        "PayrollContractHistory",
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    dependants: Mapped[List["PayrollDependant"]] = relationship(
        "PayrollDependant",
        back_populates="employee",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Employee (name={self.name!r})"


class InsurancePolicy(Base, TimeStampMixin):
    __tablename__ = "insurance_policies"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(30), unique=True)  # required
    name: Mapped[str] = mapped_column(String(50))  # required
    company_percentage: Mapped[float] = mapped_column(Float)  # required
    employee_percentage: Mapped[float] = mapped_column(Float)  # required
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))  # required

    def __repr__(self) -> str:
        return f"InsurancePolicy(name={self.name!r})"


class PayrollShift(Base, TimeStampMixin):
    __tablename__ = "shifts"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(30), unique=True)  # required
    name: Mapped[str] = mapped_column(String(50))  # required
    standard_work_hours: Mapped[float]  # required
    # checkin: Mapped[Optional[time]] = mapped_column(Time)
    # earliest_checkin: Mapped[Optional[time]] = mapped_column(Time)
    # latest_checkin: Mapped[Optional[time]] = mapped_column(Time)
    # checkout: Mapped[Optional[time]] = mapped_column(Time)
    # earliest_checkout: Mapped[Optional[time]] = mapped_column(Time)
    # latest_checkout: Mapped[Optional[time]] = mapped_column(Time)
    created_by: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Shift (name={self.name!r}, code={self.code!r}, standard_work_hours={self.standard_work_hours!r})"


class PayrollSchedule(Base, TimeStampMixin):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(30), unique=True)  # required
    name: Mapped[str] = mapped_column(String(50))  # required
    shift_per_day: Mapped[int]
    created_by: Mapped[str] = mapped_column(String(30))  # required

    shifts: Mapped[List["PayrollScheduleDetail"]] = relationship(
        "PayrollScheduleDetail", cascade="all, delete-orphan", back_populates="schedule"
    )

    def __repr__(self) -> str:
        return f"Schedule (name={self.name!r}, code={self.code!r})"


class PayrollScheduleDetail(Base, TimeStampMixin):
    __tablename__ = "schedule_details"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE")
    )
    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id"))
    day: Mapped[Day]
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


class PayrollAttendance(Base, TimeStampMixin):
    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(primary_key=True)  # required
    work_hours: Mapped[float]  # required
    day_attendance: Mapped[date]  # required
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE")
    )  # required
    is_holiday: Mapped[bool]
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


class PayrollOvertime(Base, TimeStampMixin):
    __tablename__ = "overtimes"

    id: Mapped[int] = mapped_column(primary_key=True)  # required
    overtime_hours: Mapped[float]  # required
    day_overtime: Mapped[date]  # required
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE")
    )  # required
    created_by: Mapped[str] = mapped_column(String(30))  # required

    employee: Mapped["PayrollEmployee"] = relationship(
        "PayrollEmployee", back_populates="overtimes"
    )

    __table_args__ = (
        UniqueConstraint("employee_id", "day_overtime", name="uq_employee_overtime"),
    )

    def __repr__(self) -> str:
        return f"Overtime (employee_id={self.employee_id!r}, overtime_hours={self.overtime_hours!r}, day_overtime={self.day_overtime!r})"


class PayrollDependant(Base, TimeStampMixin):
    __tablename__ = "dependants"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    code: Mapped[str] = mapped_column(String(30), unique=True)  # required
    name: Mapped[str] = mapped_column(String(50))  # required
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"),
    )  # required
    date_of_birth: Mapped[date]  # required
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    mst: Mapped[str] = mapped_column(String(30), unique=True)  # required
    id_doc_type: Mapped[IDDocType]
    doc_number: Mapped[str] = mapped_column(String(30))
    relationship: Mapped[DependantRelationship]
    deduction_from: Mapped[date]
    deduction_to: Mapped[date]
    note: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))  # required

    employee: Mapped["PayrollEmployee"] = relationship(
        "PayrollEmployee", back_populates="dependants"
    )

    def __repr__(self) -> str:
        return f"Dependant (name={self.name!r}, (employee_id={self.employee_id!r}))"


class PayrollContractHistory(Base, TimeStampMixin):
    __tablename__ = "contract_histories"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"),
    )  # required
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    is_probation: Mapped[bool] = mapped_column()  # required
    start_date: Mapped[date]  # required
    end_date: Mapped[Optional[date]]  # required
    salary: Mapped[float]  # required
    meal_benefit: Mapped[float]
    transportation_benefit: Mapped[float]
    housing_benefit: Mapped[float]
    toxic_benefit: Mapped[float]
    phone_benefit: Mapped[float]
    attendant_benefit: Mapped[float]
    contract_type: Mapped[ContractHistoryType]
    schedule_id: Mapped[Optional[int]] = mapped_column(ForeignKey("schedules.id"))
    # template: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))  # required

    employee: Mapped["PayrollEmployee"] = relationship(
        "PayrollEmployee",
        back_populates="contract_histories",
    )

    payroll_managements: Mapped[List["PayrollPayrollManagement"]] = relationship(
        "PayrollPayrollManagement", back_populates="contract"
    )


class PayrollPayrollManagement(Base, TimeStampMixin):
    __tablename__ = "payroll_managements"
    id: Mapped[int] = mapped_column(primary_key=True)  # required
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))  # required
    contract_history_id: Mapped[int] = mapped_column(
        ForeignKey("contract_histories.id")
    )
    # tax_policy_id: Mapped[int] = mapped_column(
    #     ForeignKey("tax_policies.id")
    # )
    insurance_policy_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("insurance_policies.id")
    )
    net_income: Mapped[float]
    month: Mapped[int]
    year: Mapped[int]
    salary: Mapped[float]
    work_days_standard: Mapped[float]
    work_days: Mapped[float]
    work_days_salary: Mapped[float]
    overtime_1_5x_hours: Mapped[Optional[float]]
    overtime_1_5x_salary: Mapped[Optional[float]]
    overtime_2_0x_hours: Mapped[Optional[float]]
    overtime_2_0x_salary: Mapped[Optional[float]]
    transportation_benefit_salary: Mapped[float]
    attendant_benefit_salary: Mapped[float]
    housing_benefit_salary: Mapped[float]
    toxic_benefit_salary: Mapped[float]
    phone_benefit_salary: Mapped[float]
    meal_benefit_salary: Mapped[float]
    gross_income: Mapped[float]
    employee_insurance: Mapped[Optional[float]]
    company_insurance: Mapped[Optional[float]]
    no_tax_salary: Mapped[float]
    dependant_people: Mapped[Optional[int]]
    tax_salary: Mapped[Optional[float]]
    tax: Mapped[Optional[float]]
    total_deduction: Mapped[Optional[float]]

    created_by: Mapped[str] = mapped_column(String(30))  # required

    employee: Mapped["PayrollEmployee"] = relationship(
        "PayrollEmployee", back_populates="payroll_managements"
    )
    contract: Mapped["PayrollContractHistory"] = relationship(
        "PayrollContractHistory", back_populates="payroll_managements"
    )
    # tax_policy: Mapped["TaxPolicy"] = relationship("TaxPolicy", backref="contracttypes")
    insurance_policy: Mapped[Optional["InsurancePolicy"]] = relationship(
        "InsurancePolicy", backref="contracttypes"
    )

    def __repr__(self) -> str:
        return f"Payroll (employee_id={self.employee_id!r}, value={self.net_income!r}, month={self.month!r})"


# class TaxPolicy(Base, TimeStampMixin):
#     __tablename__ = "tax_policies"
#     id: Mapped[int] = mapped_column(primary_key=True)  # required
#     code: Mapped[str] = mapped_column(String(30), unique=True)  # required
#     name: Mapped[str] = mapped_column(String(50))  # required
#     tax_type: Mapped[TaxType]
#     description: Mapped[Optional[str]] = mapped_column(String(255))
#     percentage: Mapped[Optional[float]] = mapped_column(Float)
#     is_active: Mapped[bool]
#     created_by: Mapped[str] = mapped_column(String(30))  # required

#     def __repr__(self) -> str:
#         return f"TaxPolicy(name={self.name!r})"

# class PayrollContract(Base, TimeStampMixin):
#     __tablename__ = "contracts"
#     id: Mapped[int] = mapped_column(primary_key=True)  # required
#     code: Mapped[str] = mapped_column(String(30), unique=True)  # required
#     name: Mapped[str] = mapped_column(String(50))  # required
#     status: Mapped[Status]  # required
#     description: Mapped[Optional[str]] = mapped_column(String(255))
#     number_of_months: Mapped[int] = mapped_column()  # required
#     is_probation: Mapped[bool] = mapped_column()  # required
#     employee_code: Mapped[str] = mapped_column(ForeignKey("employees.code"))  # required
#     contract_date: Mapped[date]  # required
#     signed_date: Mapped[date]  # required
#     start_date: Mapped[date]  # required
#     end_date: Mapped[Optional[date]]  # required
#     payment_method: Mapped[PaymentMethod]  # required
#     attachments: Mapped[Optional[str]] = mapped_column(String(255))
#     salary: Mapped[float]  # required
#     basic_salary: Mapped[float]  # required
#     meal_benefit: Mapped[float]
#     transportation_benefit: Mapped[float]
#     housing_benefit: Mapped[float]
#     toxic_benefit: Mapped[float]
#     phone_benefit: Mapped[float]
#     attendant_benefit: Mapped[float]
#     template: Mapped[Optional[str]] = mapped_column(String(255))
#     created_by: Mapped[str] = mapped_column(String(30))  # required

#     employee: Mapped["PayrollEmployee"] = relationship(
#         "PayrollEmployee",
#         backref="contracts",
#     )
#     addendums: Mapped[List["PayrollAddendum"]] = relationship(
#         "PayrollAddendum", cascade="all, delete-orphan", back_populates="contract"
#     )
#     payroll_managements: Mapped[List["PayrollPayrollManagement"]] = relationship(
#         "PayrollPayrollManagement", back_populates="contract"
#     )

#     def __repr__(self) -> str:
#         return f"Contract (name={self.name!r})"


# class PayrollAddendum(Base, TimeStampMixin):
#     __tablename__ = "addendums"
#     id: Mapped[int] = mapped_column(primary_key=True)  # required
#     code: Mapped[str] = mapped_column(String(30), unique=True)  # required
#     name: Mapped[str] = mapped_column(String(50))  # required
#     status: Mapped[Status]  # required
#     description: Mapped[Optional[str]] = mapped_column(String(255))
#     contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))  # required
#     addendum_date: Mapped[date]  # required
#     signed_date: Mapped[date]  # required
#     start_date: Mapped[date]  # required
#     payment_method: Mapped[PaymentMethod]  # required
#     new_position_id: Mapped[int] = None
#     new_salary: Mapped[Optional[float]] = None  # required
#     new_basic_salary: Mapped[Optional[float]] = None  # required
#     new_meal_benefit: Mapped[Optional[float]] = None
#     new_transportation_benefit: Mapped[Optional[float]] = None
#     new_housing_benefit: Mapped[Optional[float]] = None
#     new_toxic_benefit: Mapped[Optional[float]] = None
#     new_phone_benefit: Mapped[Optional[float]] = None
#     new_attendant_benefit: Mapped[Optional[float]] = None
#     template: Mapped[Optional[str]] = mapped_column(String(255))
#     created_by: Mapped[str] = mapped_column(String(30))  # required

#     contract: Mapped["PayrollContract"] = relationship(
#         "PayrollContract",
#         back_populates="addendums",
#     )

#     def __repr__(self) -> str:
#         return f"Addendum (name={self.name!r})"

# class PayrollBenefit(Base, TimeStampMixin):
#     __tablename__ = "benefits"
#     id: Mapped[int] = mapped_column(primary_key=True)  # required
#     code: Mapped[str] = mapped_column(String(30), unique=True)  # required
#     name: Mapped[str] = mapped_column(String(50))  # required
#     replay: Mapped[BenefitReplay] = mapped_column(default=BenefitReplay.DAILY)
#     type: Mapped[BenefitType]
#     count_salary: Mapped[bool]
#     value: Mapped[float]
#     description: Mapped[Optional[str]]
#     created_by: Mapped[str] = mapped_column(String(30))  # required

#     def __repr__(self) -> str:
#         return f"Benefit (name={self.name!r}, code={self.code!r})"


# class PayrollCBAssoc(Base, TimeStampMixin):
#     __tablename__ = "contract_benefit_association"
#     id: Mapped[int] = mapped_column(primary_key=True)  # required
#     contract_id: Mapped[int] = mapped_column(
#         ForeignKey("contracts.id", ondelete="CASCADE")
#     )
#     benefit_id: Mapped[int] = mapped_column(ForeignKey("benefits.id"))
#     created_by: Mapped[str] = mapped_column(String(30))  # required

#     benefit: Mapped["PayrollBenefit"] = relationship()
#     contract: Mapped["PayrollContract"] = relationship(
#         "PayrollContract",
#         back_populates="benefits",
#     )

#     def __repr__(self) -> str:
#         return f"CBAssoc (contract_id={self.contract_id!r}, benefit_id={self.benefit_id!r})"

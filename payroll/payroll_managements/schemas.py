from datetime import date, datetime
from typing import List

from payroll.utils.models import Pagination, PayrollBase

# class PayrollPayroll(Base, TimeStampMixin):
#     _tablename_ = "payrolls"
#     id: Mapped[int] = mapped_column(primary_key=True)  # required
#     employee_id: Mapped[int] = mapped_column(
#         ForeignKey("employees.id")
#     )  # required
#     value: Mapped[float]
#     month: Mapped[date]
#     created_by: Mapped[str] = mapped_column(String(30))  # required
#     employee: Mapped["PayrollEmployee"] = relationship(
#         "PayrollEmployee", back_populates="payrolls"
#     )


class PayrollManagementBase(PayrollBase):
    employee_id: int  # required
    value: float  # required
    month: date  # required


class PayrollManagementRead(PayrollManagementBase):
    id: int
    created_at: datetime


class PayrollManagementsRead(PayrollBase):
    count: int
    data: list[PayrollManagementRead] = []


# class PayrollManagementUpdate(PayrollBase):
#     name: Optional[str] = None
#     description: Optional[str] = None


class PayrollManagementCreate(PayrollBase):
    employee_id: int  # required
    month: date  # required


class PayrollManagementBPagination(Pagination):
    items: List[PayrollManagementRead] = []

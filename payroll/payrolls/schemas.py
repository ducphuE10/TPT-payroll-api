from datetime import date, datetime
from typing import List, Optional

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


class PayrollBase(PayrollBase):
    employee_id: int  # required
    value: float  # required
    month: date  # required


class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime


class DepartmentsRead(PayrollBase):
    count: int
    data: list[DepartmentRead] = []


class DepartmentUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentPagination(Pagination):
    items: List[DepartmentRead] = []

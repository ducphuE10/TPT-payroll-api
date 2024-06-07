from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from payroll.database.core import Base
from payroll.models import Pagination, PayrollBase, TimeStampMixin

class PayrollDepartment(Base, TimeStampMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[str] = mapped_column(String(30))

    @property
    def employees(self):
        from payroll.employee.models import PayrollEmployee
        return relationship(PayrollEmployee, back_populates="department")
    
    def __repr__(self) -> str:
        return f"Department (name={self.name!r})"


class DepartmentBase(PayrollBase):
    code: str
    name: str
    description: Optional[str] = None
    created_by: str


class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime


class DepartmentsRead(PayrollBase):
    data: list[DepartmentRead] = []


class DepartmentUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    created_by: Optional[str] = None


class DepartmentPagination(Pagination):
    items: List[DepartmentRead] = []

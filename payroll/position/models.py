from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from payroll.database.core import Base
from payroll.models import Pagination, PayrollBase, TimeStampMixin


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

    # @property
    # def employees(self):
    #     from payroll.employee.models import PayrollEmployee
    #     return relationship(PayrollEmployee, back_populates="position")

    def __repr__(self) -> str:
        return f"Position (name={self.name!r})"


class PositionBase(PayrollBase):
    code: str
    name: str
    description: Optional[str] = None
    created_by: str


class PositionRead(PositionBase):
    id: int
    created_at: datetime


class PositionsRead(PayrollBase):
    data: list[PositionRead] = []


class PositionUpdate(PayrollBase):
    name: Optional[str] = None
    description: Optional[str] = None


class PositionCreate(PositionBase):
    created_by: Optional[str] = None


class PositionPagination(Pagination):
    items: List[PositionRead] = []

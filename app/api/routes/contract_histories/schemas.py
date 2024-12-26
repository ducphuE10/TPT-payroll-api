from datetime import datetime, date
from typing import List, Optional

# from payroll.contract_benefit_assocs.schemas import CBAssocsRead
from app.api.routes.employees.schemas import EmployeeBase
from app.utils.models import ContractHistoryType
from app.utils.models import Pagination, PayrollBase


class ContractHistoryBase(PayrollBase):
    employee_id: int
    department_id: int
    position_id: int
    is_probation: bool
    start_date: date  # required
    end_date: Optional[date] = None
    salary: float  # required
    meal_benefit: float
    transportation_benefit: float
    housing_benefit: float
    toxic_benefit: float
    phone_benefit: float
    attendant_benefit: float
    contract_type: ContractHistoryType
    schedule_id: Optional[int] = None


class ContractHistoryRead(ContractHistoryBase):
    id: int
    created_at: datetime
    employee: EmployeeBase


class ContractHistoriesRead(PayrollBase):
    count: int
    data: list[ContractHistoryRead] = []


class ContractHistoryCreate(ContractHistoryBase):
    pass


class ContractHistoryUpdate(PayrollBase):
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    is_probation: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    salary: Optional[float] = None
    meal_benefit: Optional[float] = None
    transportation_benefit: Optional[float] = None
    housing_benefit: Optional[float] = None
    toxic_benefit: Optional[float] = None
    phone_benefit: Optional[float] = None
    attendant_benefit: Optional[float] = None
    contract_type: Optional[ContractHistoryType] = None
    schedule_id: Optional[int] = None


class ContractsExport(PayrollBase):
    list_contracts: List[int]
    detail_benefit: Optional[bool] = (None,)
    detail_insurance: Optional[bool] = (None,)


class ContractPagination(Pagination):
    items: List[ContractHistoryRead] = []

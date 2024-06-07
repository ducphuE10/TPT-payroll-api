from fastapi import APIRouter

from payroll.employee.models import (
    EmployeeRead,
    EmployeeCreate,
    EmployeesRead,
    EmployeeUpdate,
)
from payroll.database.core import DbSession
from payroll.employee.service import get_by_id, delete, get, create, update

employee_router = APIRouter()


@employee_router.get("/", response_model=EmployeesRead)
def retrieve_employees(
    *,
    db_session: DbSession,
):
    return get(db_session=db_session)


@employee_router.get("/{id}", response_model=EmployeeRead)
def retrieve_employee(*, db_session: DbSession, id: int):
    return get_by_id(db_session=db_session, id=id)


@employee_router.post("/", response_model=EmployeeRead)
def create_employee(*, employee_in: EmployeeCreate, db_session: DbSession):
    """Creates a new employee."""
    employee = create(db_session=db_session, employee_in=employee_in)
    return employee


@employee_router.put("/{id}", response_model=EmployeeRead)
def update_employee(*, db_session: DbSession, id: int, employee_in: EmployeeUpdate):
    return update(db_session=db_session, id=id, employee_in=employee_in)


@employee_router.delete("/{id}", response_model=EmployeeRead)
def delete_employee(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)

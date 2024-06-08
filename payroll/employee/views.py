from fastapi import APIRouter, File, UploadFile

from payroll.employee.models import (
    EmployeeRead,
    EmployeeCreate,
    EmployeesRead,
    EmployeeUpdate,
)
from payroll.database.core import DbSession
from payroll.employee.service import get_by_id, get, create, update, uploadXLSX

employee_router = APIRouter()


@employee_router.get("", response_model=EmployeesRead)
def retrieve_employees(
    *,
    db_session: DbSession,
):
    return get(db_session=db_session)


@employee_router.get("/{id}", response_model=EmployeeRead)
def retrieve_employee(*, db_session: DbSession, id: int):
    return get_by_id(db_session=db_session, id=id)


@employee_router.post("", response_model=EmployeeRead)
def create_employee(*, employee_in: EmployeeCreate, db_session: DbSession):
    """Creates a new employee."""
    employee = create(db_session=db_session, employee_in=employee_in)
    return employee


@employee_router.put("/{id}", response_model=EmployeeRead)
def update_employee(*, db_session: DbSession, id: int, employee_in: EmployeeUpdate):
    return update(db_session=db_session, id=id, employee_in=employee_in)


@employee_router.post("/import-excel")
def import_excel(*, db: DbSession, file: UploadFile = File(...)):
    return uploadXLSX(db_session=db, file=file)

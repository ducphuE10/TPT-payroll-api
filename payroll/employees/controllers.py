from fastapi import APIRouter, File, Form, UploadFile

from payroll.attendances.services import get_employee_attendances
from payroll.attendances.schemas import AttendancesRead
from payroll.employees.schemas import (
    EmployeeRead,
    EmployeeCreate,
    EmployeesRead,
    EmployeeUpdate,
)
from payroll.database.core import DbSession
from payroll.employees.repositories import (
    get_all,
    create,
    update,
    delete,
)
from payroll.employees.services import get_employee_by_id, uploadXLSX

employee_router = APIRouter()


@employee_router.get("", response_model=EmployeesRead)
def retrieve_employees(
    *,
    db_session: DbSession,
):
    return get_all(db_session=db_session)


@employee_router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(*, db_session: DbSession, employee_id: int):
    return get_employee_by_id(db_session=db_session, employee_id=employee_id)


@employee_router.get("/{employee_id}/attendances", response_model=AttendancesRead)
def retrieve_employee_attendances(*, db_session: DbSession, employee_id: int):
    """Returns all attendances of an employee."""
    return get_employee_attendances(db_session=db_session, employee_id=employee_id)


@employee_router.post("", response_model=EmployeeRead)
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


@employee_router.post("/import-excel")
def import_excel(
    *, db: DbSession, file: UploadFile = File(...), update_on_exists: bool = Form(False)
):
    return uploadXLSX(db_session=db, file=file, update_on_exists=update_on_exists)

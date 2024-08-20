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
from payroll.employees.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    search_employee_by_name,
    uploadXLSX,
)

employee_router = APIRouter()


# GET /employees
@employee_router.get("", response_model=EmployeesRead)
def retrieve_employees(
    *,
    db_session: DbSession,
):
    """Returns all employees."""
    return get_all_employees(db_session=db_session)


# GET /employees/{employee_id}
@employee_router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(*, db_session: DbSession, employee_id: int):
    """Returns a employee based on the given id."""
    return get_employee_by_id(db_session=db_session, employee_id=employee_id)


@employee_router.get("/{employee_id}/attendances", response_model=AttendancesRead)
def retrieve_employee_attendances(*, db_session: DbSession, employee_id: int):
    """Returns all attendances of an employee."""
    return get_employee_attendances(db_session=db_session, employee_id=employee_id)


# POST /employees
@employee_router.post("", response_model=EmployeeRead)
def create(*, employee_in: EmployeeCreate, db_session: DbSession):
    """Creates a new employee."""
    return create_employee(db_session=db_session, employee_in=employee_in)


# PUT /employees/{employee_id}
@employee_router.put("/{employee_id}", response_model=EmployeeRead)
def update(*, db_session: DbSession, employee_id: int, employee_in: EmployeeUpdate):
    """Updates a employee with the given data."""
    return update_employee(
        db_session=db_session, employee_id=employee_id, employee_in=employee_in
    )


# DELETE /employees/{employee_id}
@employee_router.delete("/{employee_id}", response_model=EmployeeRead)
def delete(*, db_session: DbSession, employee_id: int):
    """Deletes a employee based on the given id."""
    return delete_employee(db_session=db_session, employee_id=employee_id)


# POST /employees/import-excel
@employee_router.post("/import-excel")
def import_excel(
    *, db: DbSession, file: UploadFile = File(...), update_on_exists: bool = Form(False)
):
    return uploadXLSX(db_session=db, file=file, update_on_exists=update_on_exists)


@employee_router.get("/search", response_model=EmployeesRead)
def search_employee(*, db_session: DbSession, name: str):
    return search_employee_by_name(db_session=db_session, name=name)

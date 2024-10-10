from datetime import date
from typing import Optional
from fastapi import APIRouter, File, Form, UploadFile

# from payroll.attendances.services import get_employee_attendances
from payroll.contract_histories.services import (
    get_active_contract_history_detail_by_period,
)
from payroll.employees.schemas import (
    BenefitsRead,
    EmployeeDelete,
    EmployeeRead,
    EmployeeCreate,
    EmployeeUpdatePersonal,
    EmployeeUpdateSalary,
    EmployeesRead,
    EmployeesScheduleUpdate,
    EmployeesScheduleUpdateRead,
)
from payroll.database.core import DbSession
from payroll.employees.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    get_employees_active_benefits,
    search_employee_by_name,
    update_employee_personal,
    update_employee_salary,
    update_multi_employees_schedule,
    uploadXLSX,
)

employee_router = APIRouter()


# GET /employees
@employee_router.get("", response_model=EmployeesRead)
def retrieve_employees(*, db_session: DbSession, name: str = None):
    """Returns all employees."""
    if name:
        return search_employee_by_name(db_session=db_session, name=name)
    return get_all_employees(db_session=db_session)


@employee_router.get("/benefits", response_model=BenefitsRead)
def get_active_benefits(*, db_session: DbSession):
    return get_employees_active_benefits(db_session=db_session)


@employee_router.get("/{employee_id}/detail")
def get_contract_history_detail(
    *,
    db_session: DbSession,
    employee_id: int,
    from_date: date = date.today(),
    to_date: Optional[date] = None,
):
    return get_active_contract_history_detail_by_period(
        db_session=db_session,
        employee_id=employee_id,
        from_date=from_date,
        to_date=to_date,
    )


# GET /employees/{employee_id}
@employee_router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(*, db_session: DbSession, employee_id: int):
    """Returns a employee based on the given id."""
    return get_employee_by_id(db_session=db_session, employee_id=employee_id)


# @employee_router.get("/{employee_id}/attendances", response_model=AttendancesRead)
# def retrieve_employee_attendances(*, db_session: DbSession, employee_id: int):
#     """Returns all attendances of an employee."""
#     return get_employee_attendances(db_session=db_session, employee_id=employee_id)


# POST /employees
@employee_router.post("", response_model=EmployeeRead)
def create(*, employee_in: EmployeeCreate, db_session: DbSession):
    """Creates a new employee."""
    return create_employee(db_session=db_session, employee_in=employee_in)


@employee_router.put(
    "/multi-apply/{schedule_id}", response_model=EmployeesScheduleUpdateRead
)
def update_multi(
    *,
    db_session: DbSession,
    employee_list_in: EmployeesScheduleUpdate,
    schedule_id: int,
):
    """Creates a new attendance."""
    return update_multi_employees_schedule(
        db_session=db_session,
        employee_list_in=employee_list_in,
        schedule_id=schedule_id,
    )


# PUT /employees/{employee_id}
@employee_router.put("/{employee_id}/personal_info", response_model=EmployeeRead)
def update_personal(
    *, db_session: DbSession, employee_id: int, employee_in: EmployeeUpdatePersonal
):
    """Updates a employee with the given data."""
    return update_employee_personal(
        db_session=db_session, employee_id=employee_id, employee_in=employee_in
    )


@employee_router.put("/{employee_id}/salary_info", response_model=EmployeeRead)
def update_salary(
    *,
    db_session: DbSession,
    employee_id: int,
    employee_in: EmployeeUpdateSalary,
    is_addendum: bool,
):
    """Updates a employee with the given data."""
    return update_employee_salary(
        db_session=db_session,
        employee_id=employee_id,
        employee_in=employee_in,
        is_addendum=is_addendum,
    )


# DELETE /employees/{employee_id}
@employee_router.delete("/{employee_id}", response_model=EmployeeDelete)
def delete(*, db_session: DbSession, employee_id: int):
    """Deletes a employee based on the given id."""
    return delete_employee(db_session=db_session, employee_id=employee_id)


# POST /employees/import-excel
@employee_router.post("/import-excel")
def import_excel(
    *, db: DbSession, file: UploadFile = File(...), update_on_exists: bool = Form(False)
):
    return uploadXLSX(db_session=db, file=file, update_on_exists=update_on_exists)

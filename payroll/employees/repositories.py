import logging

from sqlalchemy import func

from payroll.employees.schemas import (
    EmployeeCreate,
    EmployeesRead,
    EmployeeUpdate,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollEmployee
from payroll.departments.repositories import get_department_by_id
from payroll.positions.repositories import get_position_by_id

log = logging.getLogger(__name__)


def get_employee_by_id(*, db_session, id: int) -> PayrollEmployee:
    """Returns a employee based on the given id."""
    employee = (
        db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id).first()
    )
    return employee


def get_employee_by_code(*, db_session, code: str) -> PayrollEmployee:
    """Returns a employee based on the given code."""
    employee = (
        db_session.query(PayrollEmployee).filter(PayrollEmployee.code == code).first()
    )
    return employee


def search_employees_by_partial_name(*, db_session, name: str):
    """Searches for employees based on a partial name match (case-insensitive).

    Args:
        db_session (Session): The database session.
        name (str): The name to search for.

    Returns:
        PayrollEmployee: A list of employees matching the search criteria.
    """
    employees = (
        db_session.query(PayrollEmployee)
        .filter(func.lower(PayrollEmployee.name).like(f"%{name.lower()}%"))
        .all()
    )

    return employees


def get_all(*, db_session) -> PayrollEmployee:
    """Returns all employees."""
    data = db_session.query(PayrollEmployee).all()
    return EmployeesRead(data=data)


def get_one_by_id(*, db_session, id: int) -> PayrollEmployee:
    """Returns a employee based on the given id."""
    print("AAAAAAAAAAAAAAAAAAAAA")
    employee = get_employee_by_id(db_session=db_session, id=id)
    if not employee:
        raise AppException(ErrorMessages.ResourceNotFound())
    return employee


def create(*, db_session, employee_in: EmployeeCreate) -> PayrollEmployee:
    """Creates a new employee."""
    employee = PayrollEmployee(**employee_in.model_dump())
    employee_db = get_employee_by_code(db_session=db_session, code=employee.code)
    if employee_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    if get_department_by_id(db_session=db_session, id=employee.department_id) is None:
        raise AppException(ErrorMessages.ResourceNotFound())
    if get_position_by_id(db_session=db_session, id=employee.position_id) is None:
        raise AppException(ErrorMessages.ResourceNotFound())
    db_session.add(employee)
    db_session.commit()
    return employee


def update(*, db_session, id: int, employee_in: EmployeeUpdate) -> PayrollEmployee:
    """Updates a employee with the given data."""
    employee_db = get_employee_by_id(db_session=db_session, id=id)

    if not employee_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = employee_in.model_dump(exclude_unset=True)

    db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id).update(
        update_data, synchronize_session=False
    )

    db_session.commit()
    return employee_db


def delete(*, db_session, id: int) -> PayrollEmployee:
    """Deletes a employee based on the given id."""
    query = db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id)
    employee = query.first()

    if not employee:
        raise AppException(ErrorMessages.ResourceNotFound())

    db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id).delete()

    db_session.commit()
    return employee

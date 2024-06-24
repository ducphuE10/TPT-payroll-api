import logging

from payroll.employees.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
)
from payroll.models import PayrollEmployee

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /employees
def retrieve_all_employees(*, db_session) -> PayrollEmployee:
    """Returns all employees."""
    query = db_session.query(PayrollEmployee)
    count = query.count()
    employees = query.all()
    return {"count": count, "data": employees}


def retrieve_employee_by_code(*, db_session, employee_code: str) -> PayrollEmployee:
    """Returns a employee based on the given code."""
    employee = (
        db_session.query(PayrollEmployee)
        .filter(PayrollEmployee.code == employee_code)
        .first()
    )
    return employee


# GET /employees/{employee_id}
def retrieve_employee_by_id(*, db_session, employee_id: int) -> PayrollEmployee:
    """Returns a employee based on the given id."""
    employee = (
        db_session.query(PayrollEmployee)
        .filter(PayrollEmployee.id == employee_id)
        .first()
    )
    return employee


# POST /employees
def add_employee(*, db_session, employee_in: EmployeeCreate) -> PayrollEmployee:
    """Creates a new employee."""
    employee = PayrollEmployee(**employee_in.model_dump())
    db_session.add(employee)
    db_session.commit()
    return employee


# PUT /employees/{employee_id}
def modify_employee(
    *, db_session, employee_id: int, employee_in: EmployeeUpdate
) -> PayrollEmployee:
    """Updates a employee with the given data."""
    update_data = employee_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollEmployee).filter(PayrollEmployee.id == employee_id)
    query.update(update_data, synchronize_session=False)
    db_session.commit()

    updated_employee = query.first()
    return updated_employee


# DELETE /employees/{employee_id}
def remove_employee(*, db_session, employee_id: int) -> PayrollEmployee:
    """Deletes a employee based on the given id."""
    db_session.query(PayrollEmployee).filter(PayrollEmployee.id == employee_id).delete()
    db_session.commit()

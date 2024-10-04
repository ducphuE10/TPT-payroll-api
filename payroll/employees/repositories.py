import logging

from sqlalchemy import func

from payroll.employees.schemas import (
    EmployeeCreate,
    EmployeeDelete,
    EmployeeUpdatePersonal,
    EmployeeUpdateSalary,
)
from payroll.models import PayrollEmployee, PayrollSchedule

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


def retrieve_schedule_by_employee_id(
    *, db_session, employee_id: int
) -> PayrollSchedule:
    """Returns a schedule based on the given id."""
    return (
        db_session.query(PayrollEmployee.schedule_id)
        .filter(PayrollEmployee.id == employee_id)
        .scalar()
    )


# GET /employees/{employee_id}
def retrieve_employee_by_id(*, db_session, employee_id: int) -> PayrollEmployee:
    """Returns a employee based on the given id."""
    return (
        db_session.query(PayrollEmployee)
        .filter(PayrollEmployee.id == employee_id)
        .first()
    )


def retrieve_employee_by_code(*, db_session, employee_code: str) -> PayrollEmployee:
    """Returns a employee based on the given code."""
    return (
        db_session.query(PayrollEmployee)
        .filter(PayrollEmployee.code == employee_code)
        .first()
    )


def retrieve_employee_by_cccd(
    *, db_session, employee_cccd: str, exclude_employee_id: int = None
) -> PayrollEmployee:
    """Returns a employee based on the given code."""
    query = db_session.query(PayrollEmployee).filter(
        PayrollEmployee.cccd == employee_cccd
    )
    if exclude_employee_id:
        query = query.filter(PayrollEmployee.id != exclude_employee_id)

    return query.first()


def retrieve_employee_by_mst(
    *, db_session, employee_mst: str, exclude_employee_id: int = None
) -> PayrollEmployee:
    """Returns a employee based on the given code."""
    query = db_session.query(PayrollEmployee).filter(
        PayrollEmployee.mst == employee_mst
    )
    if exclude_employee_id:
        query = query.filter(PayrollEmployee.id != exclude_employee_id)

    return query.first()


def retrieve_employee_by_position(*, db_session, position_id: int) -> PayrollEmployee:
    """Returns a employee based on the given code."""
    return (
        db_session.query(PayrollEmployee)
        .filter(PayrollEmployee.position_id == position_id)
        .all()
    )


def retrieve_employee_by_department(
    *, db_session, department_id: int
) -> PayrollEmployee:
    """Returns a employee based on the given code."""
    return (
        db_session.query(PayrollEmployee)
        .filter(PayrollEmployee.department_id == department_id)
        .all()
    )


# GET /employees
def retrieve_all_employees(*, db_session) -> PayrollEmployee:
    """Returns all employees."""
    query = db_session.query(PayrollEmployee)
    count = query.count()
    employees = query.order_by(PayrollEmployee.id.asc()).all()

    return {"count": count, "data": employees}


def retrieve_active_employees_benefits(*, db_session):
    query = db_session.query(
        PayrollEmployee.id,
        PayrollEmployee.code,
        PayrollEmployee.name,
        PayrollEmployee.meal_benefit,
        PayrollEmployee.transportation_benefit,
        PayrollEmployee.housing_benefit,
        PayrollEmployee.toxic_benefit,
        PayrollEmployee.phone_benefit,
        PayrollEmployee.attendant_benefit,
    )
    count = query.count()
    benefits = query.order_by(PayrollEmployee.id.asc()).all()

    return {"count": count, "data": benefits}


def search_employees_by_partial_name(*, db_session, name: str):
    """Searches for employees based on a partial name match (case-insensitive)."""
    query = db_session.query(PayrollEmployee).filter(
        func.lower(PayrollEmployee.name).like(f"%{name.lower()}%")
    )
    count = query.count()
    employees = query.all()

    return {"count": count, "data": employees}


# POST /employees
def add_employee(*, db_session, employee_in: EmployeeCreate) -> PayrollEmployee:
    """Creates a new employee."""
    employee = PayrollEmployee(**employee_in.model_dump())
    employee.created_by = "admin"
    db_session.add(employee)

    return employee


# PUT /employees/{employee_id}
def modify_employee(
    *,
    db_session,
    employee_id: int,
    employee_in: EmployeeUpdatePersonal | EmployeeUpdateSalary,
) -> PayrollEmployee:
    """Updates a employee with the given data."""
    update_data = employee_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollEmployee).filter(PayrollEmployee.id == employee_id)
    query.update(update_data, synchronize_session=False)
    updated_employee = query.first()

    return updated_employee


# DELETE /employees/{employee_id}
def remove_employee(*, db_session, employee_id: int):
    """Deletes a employee based on the given id."""
    query = db_session.query(PayrollEmployee).filter(PayrollEmployee.id == employee_id)
    deleted_employee = query.first()
    deleted_employee = EmployeeDelete(
        id=deleted_employee.id,
        code=deleted_employee.name,
        name=deleted_employee.name,
        department=deleted_employee.department.name,
        position=deleted_employee.position.name,
    )
    query.delete()

    return deleted_employee

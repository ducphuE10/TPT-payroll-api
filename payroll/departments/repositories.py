import logging

from payroll.departments.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
)
from payroll.models import PayrollDepartment

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /departments/{department_id}
def retrieve_department_by_id(*, db_session, department_id: int) -> PayrollDepartment:
    """Returns a department based on the given id."""
    return (
        db_session.query(PayrollDepartment)
        .filter(PayrollDepartment.id == department_id)
        .first()
    )


def retrieve_department_by_code(
    *, db_session, department_code: str
) -> PayrollDepartment:
    """Returns a department based on the given code."""
    return (
        db_session.query(PayrollDepartment)
        .filter(PayrollDepartment.code == department_code)
        .first()
    )


# GET /departments
def retrieve_all_departments(*, db_session) -> PayrollDepartment:
    """Returns all departments."""
    query = db_session.query(PayrollDepartment)
    count = query.count()
    departments = query.order_by(PayrollDepartment.id.asc()).all()

    return {"count": count, "data": departments}


# POST /departments
def add_department(*, db_session, department_in: DepartmentCreate) -> PayrollDepartment:
    """Creates a new department."""
    department = PayrollDepartment(**department_in.model_dump())
    department.created_by = "admin"
    db_session.add(department)

    return department


# PUT /departments/{department_id}
def modify_department(
    *, db_session, department_id: int, department_in: DepartmentUpdate
) -> PayrollDepartment:
    """Updates a department with the given data."""
    query = db_session.query(PayrollDepartment).filter(
        PayrollDepartment.id == department_id
    )
    update_data = department_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_department = query.first()

    return updated_department


# DELETE /departments/{department_id}
def remove_department(*, db_session, department_id: int):
    """Deletes a department based on the given id."""
    query = db_session.query(PayrollDepartment).filter(
        PayrollDepartment.id == department_id
    )
    deleted_department = query.first()
    query.delete()

    return deleted_department

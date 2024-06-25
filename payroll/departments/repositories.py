import logging

from payroll.departments.schemas import (
    DepartmentCreate,
    DepartmentsRead,
    DepartmentUpdate,
)
from payroll.models import PayrollDepartment

log = logging.getLogger(__name__)


# GET /departments/{department_id}
def retrieve_department_by_id(*, db_session, department_id: int) -> PayrollDepartment:
    """Returns a department based on the given id."""
    department = (
        db_session.query(PayrollDepartment)
        .filter(PayrollDepartment.id == department_id)
        .first()
    )
    return department


def retrieve_department_by_code(
    *, db_session, department_code: str
) -> PayrollDepartment:
    """Returns a department based on the given code."""
    department = (
        db_session.query(PayrollDepartment)
        .filter(PayrollDepartment.code == department_code)
        .first()
    )
    return department


# GET /departments
def retrieve_all_departments(*, db_session) -> DepartmentsRead:
    """Returns all departments."""
    query = db_session.query(PayrollDepartment)
    count = query.count()
    departments = query.all()
    return {"count": count, "data": departments}


# POST /departments
def add_department(*, db_session, department_in: DepartmentCreate) -> PayrollDepartment:
    """Creates a new department."""
    department = PayrollDepartment(**department_in.model_dump())
    db_session.add(department)
    db_session.commit()
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
    db_session.commit()
    updated_department = query.first()
    return updated_department


# DELETE /departments/{department_id}
def remove_department(*, db_session, department_id: int):
    """Deletes a department based on the given id."""
    db_session.query(PayrollDepartment).filter(
        PayrollDepartment.id == department_id
    ).delete()

    db_session.commit()

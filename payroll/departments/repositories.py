import logging

from payroll.departments.schemas import (
    DepartmentCreate,
    DepartmentsRead,
    DepartmentUpdate,
)

from payroll.exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollDepartment

log = logging.getLogger(__name__)


def get_department_by_id(*, db_session, id: int) -> PayrollDepartment:
    """Returns a department based on the given id."""
    department = (
        db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id).first()
    )
    return department


def get_department_by_code(*, db_session, code: str) -> PayrollDepartment:
    """Returns a department based on the given code."""
    department = (
        db_session.query(PayrollDepartment)
        .filter(PayrollDepartment.code == code)
        .first()
    )
    return department


def get_all(*, db_session) -> DepartmentsRead:
    """Returns all departments."""
    data = db_session.query(PayrollDepartment).all()
    return DepartmentsRead(data=data)


def get_one_by_id(*, db_session, id: int) -> PayrollDepartment:
    """Returns a department based on the given id."""
    department = get_department_by_id(db_session=db_session, id=id)

    if not department:
        raise AppException(ErrorMessages.ResourceNotFound())
    return department


def create(*, db_session, department_in: DepartmentCreate) -> PayrollDepartment:
    """Creates a new department."""
    department = PayrollDepartment(**department_in.model_dump())
    department_db = get_department_by_code(db_session=db_session, code=department.code)
    if department_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    db_session.add(department)
    db_session.commit()
    return department


def update(
    *, db_session, id: int, department_in: DepartmentUpdate
) -> PayrollDepartment:
    """Updates a department with the given data."""
    department_db = get_department_by_id(db_session=db_session, id=id)

    if not department_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = department_in.model_dump(exclude_unset=True)

    db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id).update(
        update_data, synchronize_session=False
    )

    db_session.commit()
    return department_db


def delete(*, db_session, id: int) -> PayrollDepartment:
    """Deletes a department based on the given id."""
    query = db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id)
    department = query.first()

    if not department:
        raise AppException(ErrorMessages.ResourceNotFound())

    db_session.query(PayrollDepartment).filter(PayrollDepartment.id == id).delete()

    db_session.commit()
    return department

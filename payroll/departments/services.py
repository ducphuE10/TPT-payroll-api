from payroll.departments.repositories import (
    add_department,
    modify_department,
    remove_department,
    retrieve_all_departments,
    retrieve_department_by_code,
    retrieve_department_by_id,
)
from payroll.departments.schemas import DepartmentCreate, DepartmentUpdate
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollDepartment
from payroll.utils.functions import check_depend_employee


def check_exist_department_by_id(*, db_session, department_id: int) -> bool:
    """Check if department exists in the database."""
    department = retrieve_department_by_id(
        db_session=db_session, department_id=department_id
    )
    return department is not None


def check_exist_department_by_code(*, db_session, department_code: str) -> bool:
    """Check if department exists in the database."""
    department = retrieve_department_by_code(
        db_session=db_session, department_code=department_code
    )
    return department is not None


# GET /departments/{department_id}
def get_department_by_id(*, db_session, department_id: int):
    """Returns a department based on the given id."""
    if not check_exist_department_by_id(
        db_session=db_session, department_id=department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    department = retrieve_department_by_id(
        db_session=db_session, department_id=department_id
    )
    return department


def get_department_by_code(*, db_session, department_code: int):
    """Returns a department based on the given code."""
    if not check_exist_department_by_code(
        db_session=db_session, department_code=department_code
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    department = retrieve_department_by_code(
        db_session=db_session, department_code=department_code
    )
    return department


# GET /departments
def get_all_department(*, db_session):
    """Returns all departments."""
    departments = retrieve_all_departments(db_session=db_session)
    if not departments["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return departments


# POST /departments
def create_department(*, db_session, department_in: DepartmentCreate):
    """Creates a new department."""
    if check_exist_department_by_code(
        db_session=db_session, department_code=department_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    department = add_department(db_session=db_session, department_in=department_in)
    return department


# PUT /departments/{department_id}
def update_department(
    *, db_session, department_id: int, department_in: DepartmentUpdate
):
    """Updates a department with the given data."""
    if not check_exist_department_by_id(
        db_session=db_session, department_id=department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())

    updated_department = modify_department(
        db_session=db_session, department_id=department_id, department_in=department_in
    )

    return updated_department


# DELETE /departments/{department_id}
def delete_department(*, db_session, department_id: int) -> PayrollDepartment:
    """Deletes a department based on the given id."""
    if not check_exist_department_by_id(
        db_session=db_session, department_id=department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())

    if check_depend_employee(db_session=db_session, department_id=department_id):
        raise AppException(ErrorMessages.ExistDependEmployee())

    remove_department(db_session=db_session, department_id=department_id)
    return {"message": "Department deleted successfully."}

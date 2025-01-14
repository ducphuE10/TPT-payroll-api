from app.api.routes.departments.repositories import (
    add_department,
    modify_department,
    remove_department,
    retrieve_all_departments_by_company_id,
    retrieve_department_by_code,
    retrieve_department_by_id,
)
from app.api.routes.departments.schemas import DepartmentCreate, DepartmentUpdate
from app.api.routes.employees.repositories import retrieve_employee_by_department
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages


def check_exist_department_by_id(*, db_session, department_id: int):
    """Check if department exists in the database."""
    return bool(
        retrieve_department_by_id(db_session=db_session, department_id=department_id)
    )


def check_exist_department_by_code(
    *, db_session, department_code: str, company_id: int
):
    """Check if department exists in the database."""
    return bool(
        retrieve_department_by_code(
            db_session=db_session,
            department_code=department_code,
            company_id=company_id,
        )
    )


# GET /departments/{department_id}
def get_department_by_id(*, db_session, department_id: int):
    """Returns a department based on the given id."""
    if not check_exist_department_by_id(
        db_session=db_session, department_id=department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "department")

    return retrieve_department_by_id(db_session=db_session, department_id=department_id)


def get_department_by_code(*, db_session, department_code: int, company_id: int):
    """Returns a department based on the given code."""
    if not check_exist_department_by_code(
        db_session=db_session, department_code=department_code, company_id=company_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "department")

    return retrieve_department_by_code(
        db_session=db_session, department_code=department_code, company_id=company_id
    )


# GET /departments
def get_all_department(*, db_session, company_id: int):
    """Returns all departments."""
    departments = retrieve_all_departments_by_company_id(
        db_session=db_session, company_id=company_id
    )
    if not departments["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "department")

    return departments


# POST /departments
def create_department(*, db_session, department_in: DepartmentCreate):
    """Creates a new department."""
    if check_exist_department_by_code(
        db_session=db_session,
        department_code=department_in.code,
        company_id=department_in.company_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "department")

    try:
        department = add_department(db_session=db_session, department_in=department_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return department


# PUT /departments/{department_id}
def update_department(
    *, db_session, department_id: int, department_in: DepartmentUpdate
):
    """Updates a department with the given data."""
    if not check_exist_department_by_id(
        db_session=db_session, department_id=department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "department")

    try:
        department = modify_department(
            db_session=db_session,
            department_id=department_id,
            department_in=department_in,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return department


# DELETE /departments/{department_id}
def delete_department(*, db_session, department_id: int):
    """Deletes a department based on the given id."""
    if not check_exist_department_by_id(
        db_session=db_session, department_id=department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "department")

    if retrieve_employee_by_department(
        db_session=db_session, department_id=department_id
    ):
        raise AppException(
            ErrorMessages.ExistDependObject(), ["department", "employee"]
        )

    try:
        department = remove_department(
            db_session=db_session, department_id=department_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return department

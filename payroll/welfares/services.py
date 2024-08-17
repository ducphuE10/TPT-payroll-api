from payroll.welfares.repositories import (
    add_welfare,
    modify_welfare,
    remove_welfare,
    retrieve_all_welfares,
    retrieve_welfare_by_code,
    retrieve_welfare_by_id,
)
from payroll.welfares.schemas import WelfareCreate, WelfareUpdate

# from payroll.employees.repositories import retrieve_employee_by_welfare
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages


def check_exist_welfare_by_id(*, db_session, welfare_id: int):
    """Check if welfare exists in the database."""
    return bool(retrieve_welfare_by_id(db_session=db_session, welfare_id=welfare_id))


def check_exist_welfare_by_code(*, db_session, welfare_code: str):
    """Check if welfare exists in the database."""
    return bool(
        retrieve_welfare_by_code(db_session=db_session, welfare_code=welfare_code)
    )


# GET /welfares/{welfare_id}
def get_welfare_by_id(*, db_session, welfare_id: int):
    """Returns a welfare based on the given id."""
    if not check_exist_welfare_by_id(db_session=db_session, welfare_id=welfare_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "welfare")

    return retrieve_welfare_by_id(db_session=db_session, welfare_id=welfare_id)


def get_welfare_by_code(*, db_session, welfare_code: int):
    """Returns a welfare based on the given code."""
    if not check_exist_welfare_by_code(
        db_session=db_session, welfare_code=welfare_code
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "welfare")

    return retrieve_welfare_by_code(db_session=db_session, welfare_code=welfare_code)


# GET /welfares
def get_all_welfare(*, db_session):
    """Returns all welfares."""
    welfares = retrieve_all_welfares(db_session=db_session)
    if not welfares["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "welfare")

    return welfares


# POST /welfares
def create_welfare(*, db_session, welfare_in: WelfareCreate):
    """Creates a new welfare."""
    if check_exist_welfare_by_code(db_session=db_session, welfare_code=welfare_in.code):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "welfare")

    try:
        welfare = add_welfare(db_session=db_session, welfare_in=welfare_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return welfare


# PUT /welfares/{welfare_id}
def update_welfare(*, db_session, welfare_id: int, welfare_in: WelfareUpdate):
    """Updates a welfare with the given data."""
    if not check_exist_welfare_by_id(db_session=db_session, welfare_id=welfare_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "welfare")

    try:
        welfare = modify_welfare(
            db_session=db_session,
            welfare_id=welfare_id,
            welfare_in=welfare_in,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return welfare


# DELETE /welfares/{welfare_id}
def delete_welfare(*, db_session, welfare_id: int):
    """Deletes a welfare based on the given id."""
    if not check_exist_welfare_by_id(db_session=db_session, welfare_id=welfare_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "welfare")

    # if retrieve_employee_by_welfare(
    #     db_session=db_session, welfare_id=welfare_id
    # ):
    #     raise AppException(
    #         ErrorMessages.ExistDependObject(), ["welfare", "employee"]
    #     )

    try:
        welfare = remove_welfare(db_session=db_session, welfare_id=welfare_id)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return welfare

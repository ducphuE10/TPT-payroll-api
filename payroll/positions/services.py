from payroll.employees.repositories import retrieve_employee_by_position
from payroll.positions.repositories import (
    add_position,
    modify_position,
    remove_position,
    retrieve_all_positions,
    retrieve_position_by_code,
    retrieve_position_by_id,
)
from payroll.positions.schemas import PositionCreate, PositionUpdate
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages


def check_exist_position_by_id(*, db_session, position_id: int):
    """Check if position exists in the database."""
    return bool(retrieve_position_by_id(db_session=db_session, position_id=position_id))


def check_exist_position_by_code(*, db_session, position_code: str):
    """Check if position exists in the database."""
    return bool(
        retrieve_position_by_code(db_session=db_session, position_code=position_code)
    )


# GET /positions/{position_id}
def get_position_by_id(*, db_session, position_id: int):
    """Returns a position based on the given id."""
    if not check_exist_position_by_id(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "position")

    return retrieve_position_by_id(db_session=db_session, position_id=position_id)


def get_position_by_code(*, db_session, position_code: int):
    """Returns a position based on the given code."""
    if not check_exist_position_by_code(
        db_session=db_session, position_code=position_code
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "position")

    return retrieve_position_by_code(db_session=db_session, position_code=position_code)


# GET /positions
def get_all_position(*, db_session):
    """Returns all positions."""
    positions = retrieve_all_positions(db_session=db_session)
    if not positions["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "position")

    return positions


# POST /positions
def create_position(*, db_session, position_in: PositionCreate):
    """Creates a new position."""
    if check_exist_position_by_code(
        db_session=db_session, position_code=position_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "position")

    try:
        position = add_position(db_session=db_session, position_in=position_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return position


# PUT /positions/{position_id}
def update_position(*, db_session, position_id: int, position_in: PositionUpdate):
    """Updates a position with the given data."""
    if not check_exist_position_by_id(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "position")

    try:
        position = modify_position(
            db_session=db_session, position_id=position_id, position_in=position_in
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return position


# DELETE /positions/{position_id}
def delete_position(*, db_session, position_id: int):
    """Deletes a position based on the given id."""
    if not check_exist_position_by_id(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "position")

    if retrieve_employee_by_position(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ExistDependObject(), ["position", "employee"])

    try:
        position = remove_position(db_session=db_session, position_id=position_id)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return position

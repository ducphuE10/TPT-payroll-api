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
from payroll.models import PayrollPosition
from payroll.utils.functions import check_depend_employee


def check_exist_position_by_id(*, db_session, position_id: int) -> bool:
    """Check if position exists in the database."""
    position = retrieve_position_by_id(db_session=db_session, position_id=position_id)
    return position is not None


def check_exist_position_by_code(*, db_session, position_code: str) -> bool:
    """Check if position exists in the database."""
    position = retrieve_position_by_code(
        db_session=db_session, position_code=position_code
    )
    return position is not None


# GET /positions/{position_id}
def get_position_by_id(*, db_session, position_id: int):
    """Returns a position based on the given id."""
    if not check_exist_position_by_id(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ResourceNotFound())
    position = retrieve_position_by_id(db_session=db_session, position_id=position_id)
    return position


def get_position_by_code(*, db_session, position_code: int):
    """Returns a position based on the given code."""
    if not check_exist_position_by_code(
        db_session=db_session, position_code=position_code
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    position = retrieve_position_by_code(
        db_session=db_session, position_code=position_code
    )
    return position


# GET /positions
def get_all_position(*, db_session):
    """Returns all positions."""
    positions = retrieve_all_positions(db_session=db_session)
    if not positions["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return positions


# POST /positions
def create_position(*, db_session, position_in: PositionCreate):
    """Creates a new position."""
    if check_exist_position_by_code(
        db_session=db_session, position_code=position_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    position = add_position(db_session=db_session, position_in=position_in)
    return position


# PUT /positions/{position_id}
def update_position(*, db_session, position_id: int, position_in: PositionUpdate):
    """Updates a position with the given data."""
    if not check_exist_position_by_id(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ResourceNotFound())

    updated_position = modify_position(
        db_session=db_session, position_id=position_id, position_in=position_in
    )

    return updated_position


# DELETE /positions/{position_id}
def delete_position(*, db_session, position_id: int) -> PayrollPosition:
    """Deletes a position based on the given id."""
    if not check_exist_position_by_id(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ResourceNotFound())

    if check_depend_employee(db_session=db_session, position_id=position_id):
        raise AppException(ErrorMessages.ExistDependEmployee())

    remove_position(db_session=db_session, position_id=position_id)
    return {"message": "Position deleted successfully."}

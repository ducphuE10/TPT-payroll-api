from payroll.shifts.repositories import (
    add_shift,
    modify_shift,
    remove_shift,
    retrieve_all_shifts,
    retrieve_shift_by_code,
    retrieve_shift_by_id,
)
from payroll.shifts.schemas import ShiftCreate, ShiftUpdate
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollShift


def check_exist_shift_by_id(*, db_session, shift_id: int) -> bool:
    """Check if shift exists in the database."""
    shift = retrieve_shift_by_id(db_session=db_session, shift_id=shift_id)
    return shift is not None


def check_exist_shift_by_code(*, db_session, shift_code: str) -> bool:
    """Check if shift exists in the database."""
    shift = retrieve_shift_by_code(db_session=db_session, shift_code=shift_code)
    return shift is not None


# GET /shifts/{shift_id}
def get_shift_by_id(*, db_session, shift_id: int):
    """Returns a shift based on the given id."""
    if not check_exist_shift_by_id(db_session=db_session, shift_id=shift_id):
        raise AppException(ErrorMessages.ResourceNotFound())
    shift = retrieve_shift_by_id(db_session=db_session, shift_id=shift_id)
    return shift


def get_shift_by_code(*, db_session, shift_code: int):
    """Returns a shift based on the given code."""
    if not check_exist_shift_by_code(db_session=db_session, shift_code=shift_code):
        raise AppException(ErrorMessages.ResourceNotFound())
    shift = retrieve_shift_by_code(db_session=db_session, shift_code=shift_code)
    return shift


# GET /shifts
def get_all_shift(*, db_session):
    """Returns all shifts."""
    shifts = retrieve_all_shifts(db_session=db_session)
    if not shifts["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return shifts


# POST /shifts
def create_shift(*, db_session, shift_in: ShiftCreate):
    """Creates a new shift."""
    if check_exist_shift_by_code(db_session=db_session, shift_code=shift_in.code):
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    shift = add_shift(db_session=db_session, shift_in=shift_in)
    return shift


# PUT /shifts/{shift_id}
def update_shift(*, db_session, shift_id: int, shift_in: ShiftUpdate):
    """Updates a shift with the given data."""
    if not check_exist_shift_by_id(db_session=db_session, shift_id=shift_id):
        raise AppException(ErrorMessages.ResourceNotFound())

    updated_shift = modify_shift(
        db_session=db_session, shift_id=shift_id, shift_in=shift_in
    )

    return updated_shift


# DELETE /shifts/{shift_id}
def delete_shift(*, db_session, shift_id: int) -> PayrollShift:
    """Deletes a shift based on the given id."""
    if not check_exist_shift_by_id(db_session=db_session, shift_id=shift_id):
        raise AppException(ErrorMessages.ResourceNotFound())

    remove_shift(db_session=db_session, shift_id=shift_id)
    return {"message": "Shift deleted successfully."}

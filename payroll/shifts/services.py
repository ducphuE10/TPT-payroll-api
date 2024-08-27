from payroll.schedule_details.repositories import retrieve_schedule_detail_by_shift
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


def check_exist_shift_by_id(*, db_session, shift_id: int):
    """Check if shift exists in the database."""
    return bool(retrieve_shift_by_id(db_session=db_session, shift_id=shift_id))


def check_exist_shift_by_code(*, db_session, shift_code: str):
    """Check if shift exists in the database."""
    return bool(retrieve_shift_by_code(db_session=db_session, shift_code=shift_code))


def validate_work_hours(*, standard_work_hours: float):
    if standard_work_hours < 0 or standard_work_hours > 24:
        return False
    return True


# GET /shifts/{shift_id}
def get_shift_by_id(*, db_session, shift_id: int):
    """Returns a shift based on the given id."""
    if not check_exist_shift_by_id(db_session=db_session, shift_id=shift_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "shift")

    return retrieve_shift_by_id(db_session=db_session, shift_id=shift_id)


def get_shift_by_code(*, db_session, shift_code: int):
    """Returns a shift based on the given code."""
    if not check_exist_shift_by_code(db_session=db_session, shift_code=shift_code):
        raise AppException(ErrorMessages.ResourceNotFound(), "shift")

    return retrieve_shift_by_code(db_session=db_session, shift_code=shift_code)


# GET /shifts
def get_all_shift(*, db_session):
    """Returns all shifts."""
    shifts = retrieve_all_shifts(db_session=db_session)
    if not shifts["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "shift")

    return shifts


# POST /shifts
def create_shift(*, db_session, shift_in: ShiftCreate):
    """Creates a new shift."""
    if check_exist_shift_by_code(db_session=db_session, shift_code=shift_in.code):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "shift")
    if not validate_work_hours(standard_work_hours=shift_in.standard_work_hours):
        raise AppException(ErrorMessages.InvalidInput(), "work hours")

    try:
        shift = add_shift(db_session=db_session, shift_in=shift_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return shift


# PUT /shifts/{shift_id}
def update_shift(*, db_session, shift_id: int, shift_in: ShiftUpdate):
    """Updates a shift with the given data."""
    if not check_exist_shift_by_id(db_session=db_session, shift_id=shift_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "shift")
    if not validate_work_hours(standard_work_hours=shift_in.standard_work_hours):
        raise AppException(ErrorMessages.InvalidInput(), "work hours")

    try:
        shift = modify_shift(
            db_session=db_session, shift_id=shift_id, shift_in=shift_in
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return shift


# DELETE /shifts/{shift_id}
def delete_shift(*, db_session, shift_id: int):
    """Deletes a shift based on the given id."""
    if not check_exist_shift_by_id(db_session=db_session, shift_id=shift_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "shift")
    if retrieve_schedule_detail_by_shift(db_session=db_session, shift_id=shift_id):
        raise AppException(
            ErrorMessages.ExistDependObject(), ["shift", "schedule detail"]
        )

    try:
        shift = remove_shift(db_session=db_session, shift_id=shift_id)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return shift

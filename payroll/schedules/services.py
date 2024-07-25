from payroll.schedules.repositories import (
    add_schedule,
    modify_schedule,
    remove_schedule,
    retrieve_all_schedules,
    retrieve_schedule_by_code,
    retrieve_schedule_by_id,
)
from payroll.schedules.schemas import ScheduleCreate, ScheduleUpdate
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollSchedule


def check_exist_schedule_by_id(*, db_session, schedule_id: int) -> bool:
    """Check if schedule exists in the database."""
    schedule = retrieve_schedule_by_id(db_session=db_session, schedule_id=schedule_id)
    return schedule is not None


def check_exist_schedule_by_code(*, db_session, schedule_code: str) -> bool:
    """Check if schedule exists in the database."""
    schedule = retrieve_schedule_by_code(
        db_session=db_session, schedule_code=schedule_code
    )
    return schedule is not None


# GET /schedules/{schedule_id}
def get_schedule_by_id(*, db_session, schedule_id: int):
    """Returns a schedule based on the given id."""
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound())
    schedule = retrieve_schedule_by_id(db_session=db_session, schedule_id=schedule_id)
    return schedule


def get_schedule_by_code(*, db_session, schedule_code: int):
    """Returns a schedule based on the given code."""
    if not check_exist_schedule_by_code(
        db_session=db_session, schedule_code=schedule_code
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    schedule = retrieve_schedule_by_code(
        db_session=db_session, schedule_code=schedule_code
    )
    return schedule


# GET /schedules
def get_all_schedule(*, db_session):
    """Returns all schedules."""
    schedules = retrieve_all_schedules(db_session=db_session)
    if not schedules["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return schedules


# POST /schedules
def create_schedule(*, db_session, schedule_in: ScheduleCreate):
    """Creates a new schedule."""
    if check_exist_schedule_by_code(
        db_session=db_session, schedule_code=schedule_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    schedule = add_schedule(db_session=db_session, schedule_in=schedule_in)
    return schedule


# PUT /schedules/{schedule_id}
def update_schedule(*, db_session, schedule_id: int, schedule_in: ScheduleUpdate):
    """Updates a schedule with the given data."""
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound())

    updated_schedule = modify_schedule(
        db_session=db_session, schedule_id=schedule_id, schedule_in=schedule_in
    )

    return updated_schedule


# DELETE /schedules/{schedule_id}
def delete_schedule(*, db_session, schedule_id: int) -> PayrollSchedule:
    """Deletes a schedule based on the given id."""
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound())

    remove_schedule(db_session=db_session, schedule_id=schedule_id)
    return {"message": "Schedule deleted successfully."}

import logging

from payroll.schedule_details.repositories import (
    add_schedule_detail,
    modify_schedule_detail,
    remove_schedule_detail,
    retrieve_all_schedule_details,
    retrieve_schedule_detail_by_id,
    retrieve_schedule_detail_by_info,
    retrieve_shifts_by_schedule_id,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.schedule_details.schemas import (
    ScheduleDetailBase,
    ScheduleDetailCreate,
    ScheduleDetailUpdate,
    ScheduleDetailsCreate,
    ScheduleDetailsRead,
)
from payroll.schedules.services import check_exist_schedule_by_id
from payroll.shifts.services import check_exist_shift_by_id

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_schedule_detail_by_id(*, db_session, schedule_detail_id: int) -> bool:
    """Check if schedule_detail exists in the database."""
    schedule_detail = retrieve_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )
    return schedule_detail is not None


def check_exist_schedule_detail(
    *, db_session, schedule_detail_in: ScheduleDetailBase
) -> bool:
    """Check if schedule_detail exists in the database."""
    schedule_detail = retrieve_schedule_detail_by_info(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    )
    return schedule_detail is not None


# GET /schedule_details
def get_all_schedule_details(*, db_session):
    """Returns all schedule_details."""
    list_schedule_details = retrieve_all_schedule_details(db_session=db_session)
    if not list_schedule_details["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return list_schedule_details


# GET /schedule_details/{schedule_detail_id}
def get_schedule_detail_by_id(*, db_session, schedule_detail_id: int):
    """Returns a schedule_detail based on the given id."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    schedule_detail = retrieve_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )
    return schedule_detail


# GET /schedule_details/?schedule_id={schedule_id}
def get_shifts_by_schedule_id(*, db_session, schedule_id: int):
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound())

    schedule_detail = retrieve_shifts_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )
    return schedule_detail


# POST /schedule_details
def create_schedule_detail(*, db_session, schedule_detail_in: ScheduleDetailCreate):
    """Creates a new schedule_detail."""
    if not check_exist_schedule_by_id(
        db_session=db_session, schedule_id=schedule_detail_in.schedule_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())

    if not check_exist_shift_by_id(
        db_session=db_session, shift_id=schedule_detail_in.shift_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())

    schedule_detail_in = ScheduleDetailBase(**schedule_detail_in.model_dump())

    if check_exist_schedule_detail(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists())

    schedule_detail = add_schedule_detail(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    )

    return schedule_detail


# POST /schedule_details/list
def create_multi_schedule_detail(
    *, db_session, schedule_detail_list_in: ScheduleDetailsCreate
):
    """Creates multiple schedule_details"""
    schedule_detail_list = schedule_detail_list_in.data
    created_schedule_details = []

    for schedule_detail in schedule_detail_list:
        created_detail = create_schedule_detail(
            db_session=db_session, schedule_detail_in=schedule_detail
        )
        created_schedule_details.append(created_detail)

    return ScheduleDetailsRead(
        count=len(created_schedule_details), data=created_schedule_details
    )


# PUT /schedule_details/{schedule_detail_id}
def update_schedule_detail(
    *, db_session, schedule_detail_id: int, schedule_detail_in: ScheduleDetailUpdate
):
    """Updates a schedule_detail with the given data."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())

    updated_schedule_detail = modify_schedule_detail(
        db_session=db_session,
        schedule_detail_id=schedule_detail_id,
        schedule_detail_in=schedule_detail_in,
    )
    return updated_schedule_detail


# DELETE /schedule_details/{schedule_detail_id}
def delete_schedule_detail(*, db_session, schedule_detail_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    remove_schedule_detail(db_session=db_session, schedule_detail_id=schedule_detail_id)
    return {"message": "Schedule detail deleted successfully"}

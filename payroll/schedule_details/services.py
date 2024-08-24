import logging
from typing import List

from payroll.schedule_details.repositories import (
    add_schedule_detail,
    add_schedule_detail_with_schedule_id,
    modify_schedule_detail,
    remove_schedule_detail,
    retrieve_all_schedule_details,
    retrieve_schedule_detail_by_id,
    retrieve_schedule_detail_by_info,
    retrieve_schedule_details_by_schedule_id,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.schedule_details.schemas import (
    ScheduleDetailBase,
    ScheduleDetailCreate,
    ScheduleDetailUpdate,
    ScheduleDetailsCreate,
    ScheduleDetailsUpdate,
)
from payroll.schedules.repositories import retrieve_schedule_by_id
from payroll.schedules.services import check_exist_schedule_by_id
from payroll.shifts.services import check_exist_shift_by_id
from payroll.utils.models import Day

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_schedule_detail_by_id(*, db_session, schedule_detail_id: int):
    """Check if schedule_detail exists in the database."""
    return bool(
        retrieve_schedule_detail_by_id(
            db_session=db_session, schedule_detail_id=schedule_detail_id
        )
    )


def check_exist_schedule_detail(*, db_session, schedule_detail_in: ScheduleDetailBase):
    """Check if schedule_detail exists in the database."""
    return bool(
        retrieve_schedule_detail_by_info(
            db_session=db_session, schedule_detail_in=schedule_detail_in
        )
    )


def check_limit_of_shifts_per_day(*, db_session, schedule_id: int, day: Day):
    """Check if the number of shifts per day is less than or equal to 4."""
    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )
    schedule = retrieve_schedule_by_id(db_session=db_session, schedule_id=schedule_id)
    count = 0
    for schedule_detail in schedule_details["data"]:
        if schedule_detail.day == day:
            count += 1
    if count >= schedule.shift_per_day:
        return True
    return False


# GET /schedule_details
def get_all_schedule_details(*, db_session):
    """Returns all schedule_details."""
    list_schedule_details = retrieve_all_schedule_details(db_session=db_session)
    if not list_schedule_details["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule details")

    return list_schedule_details


# GET /schedule_details/{schedule_detail_id}
def get_schedule_detail_by_id(*, db_session, schedule_detail_id: int):
    """Returns a schedule_detail based on the given id."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule detail")

    return retrieve_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )


# GET /schedule_details/?schedule_id={schedule_id}
def get_schedule_details_by_schedule_id(*, db_session, schedule_id: int):
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    return retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )


# POST /schedule_details
def create_schedule_detail(*, db_session, schedule_detail_in: ScheduleDetailCreate):
    """Creates a new schedule_detail."""
    if not check_exist_schedule_by_id(
        db_session=db_session, schedule_id=schedule_detail_in.schedule_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    if not check_exist_shift_by_id(
        db_session=db_session, shift_id=schedule_detail_in.shift_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "shift")

    schedule_detail_in = ScheduleDetailBase(**schedule_detail_in.model_dump())

    if check_exist_schedule_detail(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "schedule detail")

    if check_limit_of_shifts_per_day(
        db_session=db_session,
        schedule_id=schedule_detail_in.schedule_id,
        day=schedule_detail_in.day,
    ):
        raise AppException(
            ErrorMessages.InvalidInput(), "input due to reach limit shifts per day"
        )

    schedule_detail = add_schedule_detail(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    )

    return schedule_detail


# POST /schedule_details/list
def create_multi_schedule_details(
    *,
    db_session,
    schedule_detail_list_in: List[ScheduleDetailsCreate],
    schedule_id: int,
):
    """Creates multiple schedule_details"""
    try:
        for schedule_detail in schedule_detail_list_in:
            if not check_exist_shift_by_id(
                db_session=db_session, shift_id=schedule_detail.shift_id
            ):
                raise AppException(ErrorMessages.ResourceNotFound(), "shift")

            if check_limit_of_shifts_per_day(
                db_session=db_session,
                schedule_id=schedule_id,
                day=schedule_detail.day,
            ):
                raise AppException(
                    ErrorMessages.InvalidInput(),
                    "input due to reach limit shifts per day",
                )

            schedule_detail = add_schedule_detail_with_schedule_id(
                db_session=db_session,
                schedule_detail_in=schedule_detail,
                schedule_id=schedule_id,
            )
        db_session.commit()

    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )


# PUT /schedule_details/{schedule_detail_id}
def update_schedule_detail(
    *, db_session, schedule_detail_id: int, schedule_detail_in: ScheduleDetailUpdate
):
    """Updates a schedule_detail with the given data."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule detail")

    try:
        schedule = modify_schedule_detail(
            db_session=db_session,
            schedule_detail_id=schedule_detail_id,
            schedule_detail_in=schedule_detail_in,
        )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return schedule


def update_multi_schedule_details(
    *,
    db_session,
    schedule_detail_list_in: List[ScheduleDetailsUpdate],
    schedule_id: int,
):
    """Creates multiple schedule_details"""
    try:
        for schedule_detail in schedule_detail_list_in:
            if not check_exist_schedule_detail_by_id(
                db_session=db_session, schedule_detail_id=schedule_detail.id
            ):
                print("AAAAAAAAAAAAAAAAAAAAAA")
                schedule_detail_create = ScheduleDetailCreate(
                    **schedule_detail.model_dump(), schedule_id=schedule_id
                )
                add_schedule_detail(
                    db_session=db_session, schedule_detail_in=schedule_detail_create
                )

            if not check_exist_shift_by_id(
                db_session=db_session, shift_id=schedule_detail.shift_id
            ):
                raise AppException(ErrorMessages.ResourceNotFound(), "shift")

            schedule_detail = modify_schedule_detail(
                db_session=db_session,
                schedule_detail_id=schedule_detail.id,
                schedule_detail_in=schedule_detail,
            )

        db_session.commit()

    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )


# DELETE /schedule_details/{schedule_detail_id}
def delete_schedule_detail(*, db_session, schedule_detail_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule detail")

    try:
        schedule = remove_schedule_detail(
            db_session=db_session, schedule_detail_id=schedule_detail_id
        )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return schedule

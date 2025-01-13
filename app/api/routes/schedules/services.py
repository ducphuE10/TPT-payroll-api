from typing import List, Optional
from app.api.routes.employees.repositories import (
    retrieve_schedule_by_employee_id,
)

from app.api.routes.schedule_details.services import (
    create_multi_schedule_details,
    update_multi_schedule_details,
)

from app.api.routes.schedule_details.repositories import (
    retrieve_schedule_details_by_schedule_id,
)
from app.api.routes.schedule_details.schemas import (
    ScheduleDetailsCreate,
    ScheduleDetailsRead,
    ScheduleDetailsUpdate,
)

from app.api.routes.schedules.repositories import (
    add_schedule,
    modify_schedule,
    remove_schedule,
    retrieve_all_schedules,
    retrieve_schedule_by_code,
    retrieve_schedule_by_id,
)
from app.api.routes.schedules.schemas import (
    ScheduleCreate,
    ScheduleUpdate,
)
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages
from app.db.models import PayrollSchedule


def check_exist_schedule_by_id(*, db_session, schedule_id: int):
    """Check if schedule exists in the database."""
    return bool(retrieve_schedule_by_id(db_session=db_session, schedule_id=schedule_id))


def check_exist_schedule_by_code(*, db_session, schedule_code: str, company_id: int):
    """Check if schedule exists in the database."""
    return bool(
        retrieve_schedule_by_code(
            db_session=db_session, schedule_code=schedule_code, company_id=company_id
        )
    )


def check_exist_schedule_by_employee_id(*, db_session, employee_id: int):
    return bool(
        retrieve_schedule_by_employee_id(db_session=db_session, employee_id=employee_id)
    )


def validate_shift_per_day(*, shift_per_day: int):
    if shift_per_day < 1 or shift_per_day > 4:
        raise False
    return True


# GET /schedules/{schedule_id}
def get_schedule_by_id(*, db_session, schedule_id: int):
    """Returns a schedule based on the given id."""
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    return retrieve_schedule_by_id(db_session=db_session, schedule_id=schedule_id)


def get_schedule_by_code(*, db_session, schedule_code: str, company_id: int):
    """Returns a schedule based on the given code."""
    if not check_exist_schedule_by_code(
        db_session=db_session, schedule_code=schedule_code, company_id=company_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    return retrieve_schedule_by_code(db_session=db_session, schedule_code=schedule_code)


def get_schedule_with_details_by_id(*, db_session, schedule_id: int):
    """Returns a schedule based on the given id."""
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    schedule = retrieve_schedule_by_id(db_session=db_session, schedule_id=schedule_id)
    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )
    schedule_with_details = ScheduleDetailsRead(**schedule_details).model_dump()["data"]
    # schedule_with_details["schedule_in"] = {"name":schedule.name,"shift_per_day":schedule.shift_per_day}

    return {"schedule_in": schedule, "schedule_detail_list_in": schedule_with_details}


# GET /schedules
def get_all_schedule(*, db_session):
    """Returns all schedules."""
    schedules = retrieve_all_schedules(db_session=db_session)
    if not schedules["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    return schedules


# POST /schedules
def create_schedule(*, db_session, schedule_in: ScheduleCreate):
    """Creates a new schedule."""
    if check_exist_schedule_by_code(
        db_session=db_session,
        schedule_code=schedule_in.code,
        company_id=schedule_in.company_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "schedule")
    if not validate_shift_per_day(shift_per_day=schedule_in.shift_per_day):
        AppException(ErrorMessages.InvalidInput(), "shifts per day")

    try:
        schedule = add_schedule(db_session=db_session, schedule_in=schedule_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return schedule


def create_schedule_with_details(
    *,
    db_session,
    schedule_in: ScheduleCreate,
    schedule_detail_list_in: List[ScheduleDetailsCreate],
):
    try:
        if check_exist_schedule_by_code(
            db_session=db_session,
            schedule_code=schedule_in.code,
            company_id=schedule_in.company_id,
        ):
            raise AppException(ErrorMessages.ResourceAlreadyExists(), "schedule")
        if not validate_shift_per_day(shift_per_day=schedule_in.shift_per_day):
            raise AppException(ErrorMessages.InvalidInput(), "shifts per day")

        add_schedule(db_session=db_session, schedule_in=schedule_in)

        added_schedule = retrieve_schedule_by_code(
            db_session=db_session,
            schedule_code=schedule_in.code,
            company_id=schedule_in.company_id,
        )
        schedule_with_details = create_multi_schedule_details(
            db_session=db_session,
            schedule_detail_list_in=schedule_detail_list_in,
            schedule_id=added_schedule.id,
        )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return schedule_with_details


# PUT /schedules/{schedule_id}
def update_schedule(*, db_session, schedule_id: int, schedule_in: ScheduleUpdate):
    """Updates a schedule with the given data."""
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")
    if not validate_shift_per_day(shift_per_day=schedule_in.shift_per_day):
        AppException(ErrorMessages.InvalidInput(), "shifts per day")

    try:
        schedule = modify_schedule(
            db_session=db_session, schedule_id=schedule_id, schedule_in=schedule_in
        )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return schedule


def update_schedule_with_details(
    *,
    db_session,
    schedule_id: int,
    schedule_in: Optional[ScheduleUpdate] = None,
    schedule_detail_list_in: Optional[List[ScheduleDetailsUpdate]] = None,
):
    try:
        if schedule_in:
            update_schedule(
                db_session=db_session, schedule_id=schedule_id, schedule_in=schedule_in
            )

        schedule_with_details = ModuleNotFoundError
        if schedule_detail_list_in:
            schedule_with_details = update_multi_schedule_details(
                db_session=db_session,
                schedule_detail_list_in=schedule_detail_list_in,
                schedule_id=schedule_id,
            )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return schedule_with_details


# DELETE /schedules/{schedule_id}
def delete_schedule(*, db_session, schedule_id: int) -> PayrollSchedule:
    """Deletes a schedule based on the given id."""
    if not check_exist_schedule_by_id(db_session=db_session, schedule_id=schedule_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    try:
        schedule = remove_schedule(db_session=db_session, schedule_id=schedule_id)
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return schedule

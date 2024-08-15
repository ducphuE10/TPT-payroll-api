import logging

from payroll.schedule_details.schemas import (
    ScheduleDetailBase,
    ScheduleDetailCreate,
    ScheduleDetailUpdate,
    ScheduleDetailsCreate,
)
from payroll.models import PayrollScheduleDetail

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /schedule_details
def retrieve_all_schedule_details(*, db_session) -> PayrollScheduleDetail:
    """Returns all schedule_details."""
    query = db_session.query(PayrollScheduleDetail)
    count = query.count()
    schedule_details = query.all()

    return {"count": count, "data": schedule_details}


# GET /schedule_details/{schedule_detail_id}
def retrieve_schedule_detail_by_id(
    *, db_session, schedule_detail_id: int
) -> PayrollScheduleDetail:
    """Returns a schedule_detail based on the given id."""
    return (
        db_session.query(PayrollScheduleDetail)
        .filter(PayrollScheduleDetail.id == schedule_detail_id)
        .first()
    )


def retrieve_schedule_details_by_schedule_id(
    *, db_session, schedule_id: int
) -> PayrollScheduleDetail:
    """Returns all schedule_details of a schedule."""
    query = db_session.query(PayrollScheduleDetail).filter(
        PayrollScheduleDetail.schedule_id == schedule_id,
    )
    count = query.count()
    schedule_details = query.all()

    return {"count": count, "data": schedule_details}


def retrieve_schedule_detail_by_info(
    *, db_session, schedule_detail_in: ScheduleDetailBase
) -> PayrollScheduleDetail:
    """Returns a schedule_detail based on the given information."""
    return (
        db_session.query(PayrollScheduleDetail)
        .filter(
            PayrollScheduleDetail.schedule_id == schedule_detail_in.schedule_id,
            PayrollScheduleDetail.shift_id == schedule_detail_in.shift_id,
            PayrollScheduleDetail.day == schedule_detail_in.day,
        )
        .first()
    )


def retrieve_schedule_detail_by_shift(
    *, db_session, shift_id: int
) -> PayrollScheduleDetail:
    """Returns a schedule_detail based on the given shift_id."""
    return (
        db_session.query(PayrollScheduleDetail)
        .filter(PayrollScheduleDetail.shift_id == shift_id)
        .first()
    )


# POST /schedule_details
def add_schedule_detail(
    *, db_session, schedule_detail_in: ScheduleDetailCreate
) -> PayrollScheduleDetail:
    """Creates a new schedule_detail."""
    schedule_detail = PayrollScheduleDetail(**schedule_detail_in.model_dump())
    schedule_detail.created_by = "admin"
    db_session.add(schedule_detail)

    return schedule_detail


def add_schedule_detail_with_schedule_id(
    *, db_session, schedule_detail_in: ScheduleDetailsCreate, schedule_id: int
) -> PayrollScheduleDetail:
    """Creates a new schedule_detail."""
    schedule_detail = PayrollScheduleDetail(**schedule_detail_in.model_dump())
    schedule_detail.created_by = "admin"
    schedule_detail.schedule_id = schedule_id
    db_session.add(schedule_detail)

    return schedule_detail


# PUT /schedule_details/{schedule_detail_id}
def modify_schedule_detail(
    *, db_session, schedule_detail_id: int, schedule_detail_in: ScheduleDetailUpdate
) -> PayrollScheduleDetail:
    """Updates a schedule_detail with the given data."""
    update_data = schedule_detail_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollScheduleDetail).filter(
        PayrollScheduleDetail.id == schedule_detail_id
    )
    query.update(update_data, synchronize_session=False)
    updated_schedule_detail = query.first()

    return updated_schedule_detail


# DELETE /schedule_details/{schedule_detail_id}
def remove_schedule_detail(*, db_session, schedule_detail_id: int):
    """Deletes a schedule_detail based on the given id."""
    query = db_session.query(PayrollScheduleDetail).filter(
        PayrollScheduleDetail.id == schedule_detail_id
    )
    delete_schedule_detail = query.first()
    query.delete()

    return delete_schedule_detail

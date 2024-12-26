import logging


from app.api.routes.schedules.schemas import (
    ScheduleCreate,
    ScheduleUpdate,
)
from app.db.models import PayrollSchedule

log = logging.getLogger(__name__)


# GET /schedules/{schedule_id}
def retrieve_schedule_by_id(*, db_session, schedule_id: int) -> PayrollSchedule:
    """Returns a schedule based on the given id."""
    return (
        db_session.query(PayrollSchedule)
        .filter(PayrollSchedule.id == schedule_id)
        .first()
    )


def retrieve_schedule_by_code(*, db_session, schedule_code: str) -> PayrollSchedule:
    """Returns a schedule based on the given code."""
    return (
        db_session.query(PayrollSchedule)
        .filter(PayrollSchedule.code == schedule_code)
        .first()
    )


# GET /schedules
def retrieve_all_schedules(*, db_session) -> PayrollSchedule:
    """Returns all schedules."""
    query = db_session.query(PayrollSchedule)
    count = query.count()
    schedules = query.order_by(PayrollSchedule.id.asc()).all()
    return {"count": count, "data": schedules}


# POST /schedules
def add_schedule(*, db_session, schedule_in: ScheduleCreate) -> PayrollSchedule:
    """Creates a new schedule."""
    schedule = PayrollSchedule(**schedule_in.model_dump())
    schedule.created_by = "admin"
    db_session.add(schedule)

    return schedule


# PUT /schedules/{schedule_id}
def modify_schedule(
    *, db_session, schedule_id: int, schedule_in: ScheduleUpdate
) -> PayrollSchedule:
    """Updates a schedule with the given data."""
    query = db_session.query(PayrollSchedule).filter(PayrollSchedule.id == schedule_id)
    update_data = schedule_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_schedule = query.first()

    return updated_schedule


# DELETE /schedules/{schedule_id}
def remove_schedule(*, db_session, schedule_id: int):
    """Deletes a schedule based on the given id."""
    query = db_session.query(PayrollSchedule).filter(PayrollSchedule.id == schedule_id)
    delete_schedule = query.first()
    query.delete()

    return delete_schedule

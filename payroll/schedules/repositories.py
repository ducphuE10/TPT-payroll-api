import logging


from payroll.schedules.schemas import (
    ScheduleCreate,
    SchedulesRead,
    ScheduleUpdate,
)
from payroll.models import PayrollSchedule

log = logging.getLogger(__name__)


# GET /schedules/{schedule_id}
def retrieve_schedule_by_id(*, db_session, schedule_id: int) -> PayrollSchedule:
    """Returns a schedule based on the given id."""
    schedule = (
        db_session.query(PayrollSchedule)
        .filter(PayrollSchedule.id == schedule_id)
        .first()
    )
    return schedule


def retrieve_schedule_by_code(*, db_session, schedule_code: str) -> PayrollSchedule:
    """Returns a schedule based on the given code."""
    schedule = (
        db_session.query(PayrollSchedule)
        .filter(PayrollSchedule.code == schedule_code)
        .first()
    )
    return schedule


# GET /schedules
def retrieve_all_schedules(*, db_session) -> SchedulesRead:
    """Returns all schedules."""
    query = db_session.query(PayrollSchedule)
    count = query.count()
    schedules = query.order_by(PayrollSchedule.id.asc()).all()
    return {"count": count, "data": schedules}


# POST /schedules
def add_schedule(*, db_session, schedule_in: ScheduleCreate) -> PayrollSchedule:
    """Creates a new schedule."""
    schedule = PayrollSchedule(**schedule_in.model_dump())
    db_session.add(schedule)
    db_session.commit()
    return schedule


# PUT /schedules/{schedule_id}
def modify_schedule(
    *, db_session, schedule_id: int, schedule_in: ScheduleUpdate
) -> PayrollSchedule:
    """Updates a schedule with the given data."""
    query = db_session.query(PayrollSchedule).filter(PayrollSchedule.id == schedule_id)
    update_data = schedule_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    db_session.commit()
    updated_schedule = query.first()
    return updated_schedule


# DELETE /schedules/{schedule_id}
def remove_schedule(*, db_session, schedule_id: int):
    """Deletes a schedule based on the given id."""
    db_session.query(PayrollSchedule).filter(PayrollSchedule.id == schedule_id).delete()

    db_session.commit()

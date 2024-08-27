import logging


from payroll.overtime_schedules.schemas import (
    OvertimeScheduleCreate,
    OvertimeScheduleUpdate,
)
from payroll.models import PayrollOvertimeSchedule

log = logging.getLogger(__name__)


# GET /schedules/{schedule_id}
def retrieve_overtime_schedule_by_id(
    *, db_session, overtime_schedule_id: int
) -> PayrollOvertimeSchedule:
    """Returns a schedule based on the given id."""
    return (
        db_session.query(PayrollOvertimeSchedule)
        .filter(PayrollOvertimeSchedule.id == overtime_schedule_id)
        .first()
    )


def retrieve_overtime_schedule_by_code(
    *, db_session, overtime_schedule_code: str
) -> PayrollOvertimeSchedule:
    """Returns a schedule based on the given code."""
    return (
        db_session.query(PayrollOvertimeSchedule)
        .filter(PayrollOvertimeSchedule.code == overtime_schedule_code)
        .first()
    )


# GET /schedules
def retrieve_all_overtime_schedules(*, db_session) -> PayrollOvertimeSchedule:
    """Returns all schedules."""
    query = db_session.query(PayrollOvertimeSchedule)
    count = query.count()
    overtime_schedules = query.order_by(PayrollOvertimeSchedule.id.asc()).all()
    return {"count": count, "data": overtime_schedules}


# POST /schedules
def add_overtime_schedule(
    *, db_session, overtime_schedule_in: OvertimeScheduleCreate
) -> PayrollOvertimeSchedule:
    """Creates a new schedule."""
    overtime_schedule = PayrollOvertimeSchedule(**overtime_schedule_in.model_dump())
    overtime_schedule.created_by = "admin"
    db_session.add(overtime_schedule)

    return overtime_schedule


# PUT /schedules/{schedule_id}
def modify_overtime_schedule(
    *,
    db_session,
    overtime_schedule_id: int,
    overtime_schedule_in: OvertimeScheduleUpdate,
) -> PayrollOvertimeSchedule:
    """Updates a schedule with the given data."""
    query = db_session.query(PayrollOvertimeSchedule).filter(
        PayrollOvertimeSchedule.id == overtime_schedule_id
    )
    update_data = overtime_schedule_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_overtime_schedule = query.first()

    return updated_overtime_schedule


# DELETE /schedules/{schedule_id}
def remove_overtime_schedule(*, db_session, overtime_schedule_id: int):
    """Deletes a schedule based on the given id."""
    query = db_session.query(PayrollOvertimeSchedule).filter(
        PayrollOvertimeSchedule.id == overtime_schedule_id
    )
    delete_overtime_schedule = query.first()
    query.delete()

    return delete_overtime_schedule

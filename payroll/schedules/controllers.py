from fastapi import APIRouter

from payroll.schedules.schemas import (
    ScheduleRead,
    ScheduleCreate,
    SchedulesRead,
    ScheduleUpdate,
)
from payroll.database.core import DbSession
from payroll.schedules.services import (
    create_schedule,
    delete_schedule,
    get_all_schedule,
    get_schedule_by_id,
    update_schedule,
)

schedule_router = APIRouter()


# GET /schedules
@schedule_router.get("", response_model=SchedulesRead)
def retrieve_schedules(
    *,
    db_session: DbSession,
):
    """Retrieve all schedules."""
    return get_all_schedule(db_session=db_session)


# GET /schedules/{schedule_id}
@schedule_router.get("/{schedule_id}", response_model=ScheduleRead)
def retrieve_schedule(*, db_session: DbSession, schedule_id: int):
    """Retrieve a schedule by id."""
    return get_schedule_by_id(db_session=db_session, schedule_id=schedule_id)


# POST /schedules
@schedule_router.post("", response_model=ScheduleRead)
def create(*, schedule_in: ScheduleCreate, db_session: DbSession):
    """Creates a new schedule."""
    schedule = create_schedule(db_session=db_session, schedule_in=schedule_in)
    return schedule


# PUT /schedules/{schedule_id}
@schedule_router.put("/{schedule_id}", response_model=ScheduleRead)
def update(*, db_session: DbSession, schedule_id: int, schedule_in: ScheduleUpdate):
    """Update a schedule by id."""
    return update_schedule(
        db_session=db_session, schedule_id=schedule_id, schedule_in=schedule_in
    )


# DELETE /schedules/{schedule_id}
@schedule_router.delete("/{schedule_id}")
def delete(*, db_session: DbSession, schedule_id: int):
    """Delete a schedule by id."""
    return delete_schedule(db_session=db_session, schedule_id=schedule_id)

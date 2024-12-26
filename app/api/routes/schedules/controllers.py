from typing import List, Optional
from fastapi import APIRouter

from app.api.routes.schedule_details.schemas import (
    ScheduleDetailsCreate,
    ScheduleDetailsRead,
    ScheduleDetailsUpdate,
)
from app.api.routes.schedules.schemas import (
    ScheduleRead,
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleWithDetailsRead,
    SchedulesRead,
)
from app.db.core import DbSession
from app.api.routes.schedules.services import (
    create_schedule,
    create_schedule_with_details,
    delete_schedule,
    get_all_schedule,
    get_schedule_by_id,
    get_schedule_with_details_by_id,
    update_schedule,
    update_schedule_with_details,
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


# GET /schedules/{schedule_id}/details
@schedule_router.get("/{schedule_id}/details", response_model=ScheduleWithDetailsRead)
def retrieve_schedule_with_details(*, db_session: DbSession, schedule_id: int):
    """Retrieve a schedule by id."""
    return get_schedule_with_details_by_id(
        db_session=db_session, schedule_id=schedule_id
    )


# POST /schedules
@schedule_router.post("", response_model=ScheduleRead)
def create(*, db_session: DbSession, schedule_in: ScheduleCreate):
    """Creates a new schedule."""
    return create_schedule(db_session=db_session, schedule_in=schedule_in)


# POST /schedules
@schedule_router.post("/both", response_model=ScheduleDetailsRead)
def create_with_details(
    *,
    db_session: DbSession,
    schedule_in: ScheduleCreate,
    schedule_detail_list_in: List[ScheduleDetailsCreate],
):
    """Creates a new schedule."""
    return create_schedule_with_details(
        db_session=db_session,
        schedule_in=schedule_in,
        schedule_detail_list_in=schedule_detail_list_in,
    )


# PUT /schedules/{schedule_id}
@schedule_router.put("/{schedule_id}", response_model=ScheduleRead)
def update(*, db_session: DbSession, schedule_id: int, schedule_in: ScheduleUpdate):
    """Update a schedule by id."""
    return update_schedule(
        db_session=db_session, schedule_id=schedule_id, schedule_in=schedule_in
    )


# PUT /schedules/{schedule_id}
@schedule_router.put("/{schedule_id}/both", response_model=ScheduleDetailsRead)
def update_with_details(
    *,
    db_session: DbSession,
    schedule_id: int,
    schedule_in: Optional[ScheduleUpdate] = None,
    schedule_detail_list_in: Optional[List[ScheduleDetailsUpdate]] = None,
):
    """Update a schedule by id."""
    return update_schedule_with_details(
        db_session=db_session,
        schedule_id=schedule_id,
        schedule_in=schedule_in,
        schedule_detail_list_in=schedule_detail_list_in,
    )


# DELETE /schedules/{schedule_id}
@schedule_router.delete("/{schedule_id}")
def delete(*, db_session: DbSession, schedule_id: int):
    """Delete a schedule by id."""
    return delete_schedule(db_session=db_session, schedule_id=schedule_id)

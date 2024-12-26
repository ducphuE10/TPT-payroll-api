from fastapi import APIRouter

from app.schedule_details.schemas import (
    ScheduleDetailRead,
    ScheduleDetailsRead,
    ScheduleDetailCreate,
    ScheduleDetailUpdate,
)
from app.db.core import DbSession
from app.schedule_details.services import (
    create_schedule_detail,
    delete_schedule_detail,
    get_all_schedule_details,
    get_schedule_detail_by_id,
    get_schedule_details_by_schedule_id,
    update_schedule_detail,
)

schedule_detail_router = APIRouter()


# GET /schedule_details
@schedule_detail_router.get("", response_model=ScheduleDetailsRead)
def retrieve_schedule_details(
    *,
    db_session: DbSession,
):
    """Returns all schedule_details."""
    return get_all_schedule_details(db_session=db_session)


# GET /schedule_details/{schedule_detail_id}
@schedule_detail_router.get("/{schedule_detail_id}", response_model=ScheduleDetailRead)
def get_schedule_detail(*, db_session: DbSession, schedule_detail_id: int):
    """Returns a schedule_detail based on the given id."""
    return get_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )


# GET /schedule_details/?schedule_id={schedule_id}
@schedule_detail_router.get("/", response_model=ScheduleDetailsRead)
def get_shifts(*, db_session: DbSession, schedule_id: int):
    return get_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )


# POST /schedule_details
@schedule_detail_router.post("", response_model=ScheduleDetailRead)
def create_one(*, schedule_detail_in: ScheduleDetailCreate, db_session: DbSession):
    """Creates a new schedule_detail."""
    return create_schedule_detail(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    )


# PUT /schedule_details/{schedule_detail_id}
@schedule_detail_router.put("/{schedule_detail_id}", response_model=ScheduleDetailRead)
def update(
    *,
    db_session: DbSession,
    schedule_detail_id: int,
    schedule_detail_in: ScheduleDetailUpdate,
):
    """Updates a schedule_detail with the given data."""
    return update_schedule_detail(
        db_session=db_session,
        schedule_detail_id=schedule_detail_id,
        schedule_detail_in=schedule_detail_in,
    )


# DELETE /schedule_details/{schedule_detail_id}
@schedule_detail_router.delete("/{schedule_detail_id}")
def delete(*, db_session: DbSession, schedule_detail_id: int):
    """Deletes a schedule_detail based on the given id."""
    return delete_schedule_detail(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )

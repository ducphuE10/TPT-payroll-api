from fastapi import APIRouter

from payroll.overtime_schedules.schemas import (
    OvertimeScheduleCreate,
    OvertimeScheduleRead,
    OvertimeScheduleUpdate,
    OvertimeSchedulesRead,
)
from payroll.overtime_schedules.services import (
    create_overtime_schedule,
    delete_overtime_schedule,
    get_all_overtime_schedule,
    get_overtime_schedule_by_id,
    update_overtime_schedule,
)
from payroll.database.core import DbSession

overtime_schedule_router = APIRouter()


# GET /schedules
@overtime_schedule_router.get("", response_model=OvertimeSchedulesRead)
def retrieve_overtime_schedules(
    *,
    db_session: DbSession,
):
    """Retrieve all schedules."""
    return get_all_overtime_schedule(db_session=db_session)


# GET /schedules/{schedule_id}
@overtime_schedule_router.get(
    "/{overtime_schedule_id}", response_model=OvertimeScheduleRead
)
def retrieve_overtime_schedule(*, db_session: DbSession, overtime_schedule_id: int):
    """Retrieve a schedule by id."""
    return get_overtime_schedule_by_id(
        db_session=db_session, overtime_schedule_id=overtime_schedule_id
    )


# # GET /schedules/{schedule_id}/details
# @overtime_schedule_router.get("/{overtime_schedule_id}/details", response_model=ScheduleWithDetailsRead)
# def retrieve_schedule_with_details(*, db_session: DbSession, schedule_id: int):
#     """Retrieve a schedule by id."""
#     return get_schedule_with_details_by_id(
#         db_session=db_session, schedule_id=schedule_id
#     )


# POST /schedules
@overtime_schedule_router.post("", response_model=OvertimeScheduleRead)
def create(*, db_session: DbSession, overtime_schedule_in: OvertimeScheduleCreate):
    """Creates a new schedule."""
    return create_overtime_schedule(
        db_session=db_session, overtime_schedule_in=overtime_schedule_in
    )


# # POST /schedules
# @overtime_schedule_router.post("/both", response_model=ScheduleDetailsRead)
# def create_with_details(
#     *,
#     db_session: DbSession,
#     schedule_in: ScheduleCreate,
#     schedule_detail_list_in: List[ScheduleDetailsCreate],
# ):
#     """Creates a new schedule."""
#     return create_schedule_with_details(
#         db_session=db_session,
#         schedule_in=schedule_in,
#         schedule_detail_list_in=schedule_detail_list_in,
#     )


# PUT /schedules/{schedule_id}
@overtime_schedule_router.put(
    "/{overtime_schedule_id}", response_model=OvertimeScheduleRead
)
def update(
    *,
    db_session: DbSession,
    overtime_schedule_id: int,
    overtime_schedule_in: OvertimeScheduleUpdate,
):
    """Update a schedule by id."""
    return update_overtime_schedule(
        db_session=db_session,
        overtime_schedule_id=overtime_schedule_id,
        overtime_schedule_in=overtime_schedule_in,
    )


# # PUT /schedules/{schedule_id}
# @overtime_schedule_router.put("/{schedule_id}/both", response_model=ScheduleDetailsRead)
# def update_with_details(
#     *,
#     db_session: DbSession,
#     schedule_id: int,
#     schedule_in: ScheduleUpdate,
#     schedule_detail_list_in: List[ScheduleDetailsUpdate],
# ):
#     """Update a schedule by id."""
#     return update_schedule_with_details(
#         db_session=db_session,
#         schedule_id=schedule_id,
#         schedule_in=schedule_in,
#         schedule_detail_list_in=schedule_detail_list_in,
#     )


# DELETE /schedules/{schedule_id}
@overtime_schedule_router.delete("/{overtime_schedule_id}")
def delete(*, db_session: DbSession, overtime_schedule_id: int):
    """Delete a schedule by id."""
    return delete_overtime_schedule(
        db_session=db_session, overtime_schedule_id=overtime_schedule_id
    )

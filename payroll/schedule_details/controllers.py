from fastapi import APIRouter

from payroll.schedule_details.schemas import (
    Schedule_detailRead,
    Schedule_detailsRead,
    Schedule_detailCreate,
    Schedule_detailUpdate,
)
from payroll.database.core import DbSession
from payroll.schedule_details.services import (
    create_schedule_detail,
    delete_schedule_detail,
    get_all_schedule_details,
    get_schedule_detail_by_id,
    update_schedule_detail,
    search_schedule_detail_by_name,
)

schedule_detail_router = APIRouter()


# GET /schedule_details
@schedule_detail_router.get("", response_model=Schedule_detailsRead)
def retrieve_schedule_details(
    *,
    db_session: DbSession,
):
    """Returns all schedule_details."""
    return get_all_schedule_details(db_session=db_session)


# GET /schedule_details/{schedule_detail_id}
@schedule_detail_router.get("/{schedule_detail_id}", response_model=Schedule_detailRead)
def get_schedule_detail(*, db_session: DbSession, schedule_detail_id: int):
    """Returns a schedule_detail based on the given id."""
    return get_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )


@schedule_detail_router.get(
    "/{schedule_detail_id}/attendances", response_model=AttendancesRead
)
def retrieve_schedule_detail_attendances(
    *, db_session: DbSession, schedule_detail_id: int
):
    """Returns all attendances of an schedule_detail."""
    return get_schedule_detail_attendances(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )


# POST /schedule_details
@schedule_detail_router.post("", response_model=Schedule_detailRead)
def create(*, schedule_detail_in: Schedule_detailCreate, db_session: DbSession):
    """Creates a new schedule_detail."""
    schedule_detail = create_schedule_detail(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    )
    return schedule_detail


# PUT /schedule_details/{schedule_detail_id}
@schedule_detail_router.put("/{schedule_detail_id}", response_model=Schedule_detailRead)
def update(
    *,
    db_session: DbSession,
    schedule_detail_id: int,
    schedule_detail_in: Schedule_detailUpdate,
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


# POST /schedule_details/import-excel
@schedule_detail_router.post("/import-excel")
def import_excel(
    *, db: DbSession, file: UploadFile = File(...), update_on_exists: bool = Form(False)
):
    return uploadXLSX(db_session=db, file=file, update_on_exists=update_on_exists)


@schedule_detail_router.post("/search", response_model=Schedule_detailsRead)
def search_schedule_detail(*, db_session: DbSession, name: str):
    return search_schedule_detail_by_name(db_session=db_session, name=name)

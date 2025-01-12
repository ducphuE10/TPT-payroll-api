from fastapi import APIRouter, File, UploadFile

# , File, Form, UploadFile

from app.api.routes.overtimes.schemas import (
    OvertimeRead,
    OvertimeCreate,
    OvertimesCreate,
    OvertimesDelete,
    OvertimesRead,
    OvertimeUpdate,
)
from app.db.core import DbSession
from app.api.routes.overtimes.services import (
    create_multi_overtimes,
    create_overtime,
    delete_multi_overtimes,
    delete_overtime,
    get_all_overtimes,
    get_overtime_by_id,
    get_overtimes_by_month,
    update_overtime,
    upload_excel,
)

overtime_router = APIRouter()


# GET /overtimes
@overtime_router.get("", response_model=OvertimesRead)
def retrieve_overtimes(
    *,
    db_session: DbSession,
):
    """Returns all overtimes."""
    return get_all_overtimes(db_session=db_session)


# GET /overtimes/period?m=month&y=year
@overtime_router.get("/period", response_model=OvertimesRead)
def retrieve_overtimes_by_month(
    *, db_session: DbSession, company_id: int, month: int, year: int
):
    """Retrieve all overtimes of employees by month and year"""
    return get_overtimes_by_month(
        db_session=db_session, month=month, year=year, company_id=company_id
    )


# GET /overtimes/{overtime_id}
@overtime_router.get("/{overtime_id}", response_model=OvertimeRead)
def get_overtime(*, db_session: DbSession, overtime_id: int):
    """Returns a overtime based on the given id."""
    return get_overtime_by_id(db_session=db_session, overtime_id=overtime_id)


# POST /overtimes
@overtime_router.post("", response_model=OvertimeRead)
def create(*, overtime_in: OvertimeCreate, db_session: DbSession):
    """Creates a new overtime."""
    return create_overtime(db_session=db_session, overtime_in=overtime_in)


@overtime_router.post("/bulk", response_model=OvertimesRead)
def create_multi(*, db_session: DbSession, overtime_list_in: OvertimesCreate):
    """Creates a new attendance."""
    return create_multi_overtimes(
        db_session=db_session,
        overtime_list_in=overtime_list_in,
        apply_all=overtime_list_in.apply_all,
    )


# PUT /overtimes/{overtime_id}
@overtime_router.put("/{overtime_id}", response_model=OvertimeRead)
def update(*, db_session: DbSession, overtime_id: int, overtime_in: OvertimeUpdate):
    """Updates a overtime with the given data."""
    return update_overtime(
        db_session=db_session, overtime_id=overtime_id, overtime_in=overtime_in
    )


@overtime_router.delete("/bulk")
def delete_multi(*, db_session: DbSession, overtime_list_in: OvertimesDelete):
    """Deletes multiple overtimes."""
    return delete_multi_overtimes(
        db_session=db_session,
        overtime_list_in=overtime_list_in,
    )


# DELETE /overtimes/{overtime_id}
@overtime_router.delete("/{overtime_id}")
def delete(*, db_session: DbSession, overtime_id: int):
    """Deletes a overtime based on the given id."""
    return delete_overtime(db_session=db_session, overtime_id=overtime_id)


# POST /overtimes/import-excel
@overtime_router.post("/import-excel")
def import_excel(*, db: DbSession, file: UploadFile = File(...)):
    return upload_excel(db_session=db, file=file)

from fastapi import APIRouter, File, UploadFile

from payroll.attendances.schemas import (
    AttendanceRead,
    AttendanceCreate,
    AttendancesCreate,
    AttendancesRead,
    AttendanceUpdate,
)
from payroll.database.core import DbSession
from payroll.attendances.services import (
    create_attendance,
    create_multi_attendances,
    delete_attendance,
    get_all_attendances,
    get_attendance_by_id,
    get_multi_attendances_by_month,
    update_attendance,
    upload_excel,
)

attendance_router = APIRouter()


# GET /attendances
@attendance_router.get("", response_model=AttendancesRead)
def get_all(
    *,
    db_session: DbSession,
):
    """Returns all attendances."""
    return get_all_attendances(db_session=db_session)


# GET /attendances/period?m=month&y=year
@attendance_router.get("/period", response_model=AttendancesRead)
def get_multi_by_month(*, db_session: DbSession, month: int, year: int):
    """Returns all attendances based on the given month and year."""
    return get_multi_attendances_by_month(db_session=db_session, month=month, year=year)


# GET /attendances/{attendance_id}
@attendance_router.get("/{attendance_id}", response_model=AttendanceRead)
def get_one(*, db_session: DbSession, attendance_id: int):
    """Returns a attendance based on the given id."""
    return get_attendance_by_id(db_session=db_session, attendance_id=attendance_id)


# POST /attendances
@attendance_router.post("", response_model=AttendanceRead)
def create_one(*, db_session: DbSession, attendance_in: AttendanceCreate):
    """Creates a new attendance."""
    return create_attendance(db_session=db_session, attendance_in=attendance_in)


# POST /attendances/bulk
@attendance_router.post("/bulk", response_model=AttendancesRead)
def create_multi(*, db_session: DbSession, attendance_list_in: AttendancesCreate):
    """Creates multiple attendances."""
    return create_multi_attendances(
        db_session=db_session,
        attendance_list_in=attendance_list_in,
    )


# PUT /attendances/{attendance_id}
@attendance_router.put("/{attendance_id}", response_model=AttendanceRead)
def update_one(
    *, db_session: DbSession, attendance_id: int, attendance_in: AttendanceUpdate
):
    """Updates a attendance based on the given id."""
    return update_attendance(
        db_session=db_session, attendance_id=attendance_id, attendance_in=attendance_in
    )


# DELETE /attendances/{attendance_id}
@attendance_router.delete("/{attendance_id}")
def delete_one(*, db_session: DbSession, attendance_id: int):
    """Deletes a attendance based on the given id."""
    return delete_attendance(db_session=db_session, attendance_id=attendance_id)


# POST /attendances/import-excel
@attendance_router.post("/import-excel")
def import_excel(*, db: DbSession, file: UploadFile = File(...)):
    """Imports attendances from an excel file."""
    return upload_excel(db_session=db, file=file)

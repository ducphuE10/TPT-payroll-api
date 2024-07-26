from fastapi import APIRouter, File, Form, UploadFile

# , File, Form, UploadFile

from payroll.attendances.schemas import (
    AttendanceRead,
    AttendanceCreate,
    AttendancesRead,
    AttendanceUpdate,
)
from payroll.database.core import DbSession
from payroll.attendances.services import (
    create_attendance,
    delete_attendance,
    get_all_attendances,
    get_attendance_by_id,
    get_attendances_by_month,
    update_attendance,
    uploadXLSX,
)

attendance_router = APIRouter()


# GET /attendances
@attendance_router.get("", response_model=AttendancesRead)
def retrieve_attendances(
    *,
    db_session: DbSession,
):
    """Returns all attendances."""
    return get_all_attendances(db_session=db_session)


# GET /attendances/test?m=1&y=2021
@attendance_router.get("/test", response_model=AttendancesRead)
def retrieve_attendances_by_month(*, db_session: DbSession, m: int, y: int):
    """Retrieve all attendances of employees by month and year"""
    return get_attendances_by_month(db_session=db_session, month=m, year=y)


# GET /attendances/{attendance_id}
@attendance_router.get("/{attendance_id}", response_model=AttendanceRead)
def get_attendance(*, db_session: DbSession, attendance_id: int):
    """Returns a attendance based on the given id."""
    return get_attendance_by_id(db_session=db_session, attendance_id=attendance_id)


# POST /attendances
@attendance_router.post("", response_model=AttendanceRead)
def create(*, attendance_in: AttendanceCreate, db_session: DbSession):
    """Creates a new attendance."""
    attendance = create_attendance(db_session=db_session, attendance_in=attendance_in)
    return attendance


# PUT /attendances/{attendance_id}
@attendance_router.put("/{attendance_id}", response_model=AttendanceRead)
def update(
    *, db_session: DbSession, attendance_id: int, attendance_in: AttendanceUpdate
):
    """Updates a attendance with the given data."""
    return update_attendance(
        db_session=db_session, attendance_id=attendance_id, attendance_in=attendance_in
    )


# DELETE /attendances/{attendance_id}
@attendance_router.delete("/{attendance_id}")
def delete(*, db_session: DbSession, attendance_id: int):
    """Deletes a attendance based on the given id."""
    return delete_attendance(db_session=db_session, attendance_id=attendance_id)


# POST /attendances/import-excel
@attendance_router.post("/import-excel")
def import_excel(
    *, db: DbSession, file: UploadFile = File(...), update_on_exists: bool = Form(False)
):
    return uploadXLSX(db_session=db, file=file, update_on_exists=update_on_exists)

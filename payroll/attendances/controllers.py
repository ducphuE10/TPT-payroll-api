from fastapi import APIRouter, File, Form, UploadFile

# , File, Form, UploadFile

from payroll.attendances.schemas import (
    AttendanceRead,
    AttendanceCreate,
    AttendancesRead,
    AttendanceUpdate,
)
from payroll.database.core import DbSession
from payroll.attendances.repositories import (
    get_all,
    get_one_by_id,
    create,
    update,
    delete,
)
from payroll.attendances.services import uploadXLSX

# from payroll.attendances.services import uploadXLSX

attendance_router = APIRouter()


@attendance_router.get("", response_model=AttendancesRead)
def retrieve_attendances(
    *,
    db_session: DbSession,
):
    return get_all(db_session=db_session)


@attendance_router.get("/{id}", response_model=AttendanceRead)
def retrieve_attendance(*, db_session: DbSession, id: int):
    return get_one_by_id(db_session=db_session, id=id)


# @attendance_router.get("/{id}/attendances", response_model=AttendanceRead)
# def retrieve_employee_attendances(*, db_session: DbSession, id: int):
#     return get_employee_attendances(db_session=db_session, id=id)


@attendance_router.post("", response_model=AttendanceRead)
def create_attendance(*, attendance_in: AttendanceCreate, db_session: DbSession):
    """Creates a new attendance."""
    attendance = create(db_session=db_session, attendance_in=attendance_in)
    return attendance


@attendance_router.put("/{id}", response_model=AttendanceRead)
def update_attendance(
    *, db_session: DbSession, id: int, attendance_in: AttendanceUpdate
):
    return update(db_session=db_session, id=id, attendance_in=attendance_in)


@attendance_router.delete("/{id}", response_model=AttendanceRead)
def delete_attendance(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)


@attendance_router.post("/import-excel")
def import_excel(
    *, db: DbSession, file: UploadFile = File(...), update_on_exists: bool = Form(False)
):
    return uploadXLSX(db_session=db, file=file, update_on_exists=update_on_exists)

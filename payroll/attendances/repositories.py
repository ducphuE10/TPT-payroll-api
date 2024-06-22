import logging

from payroll.attendances.schemas import (
    AttendanceCreate,
    AttendancesRead,
    AttendanceUpdate,
)
from payroll.attendances.services import check_exist_attendance, get_attendance_by_id
from payroll.employees.repositories import get_employee_by_id
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollAttendance

log = logging.getLogger(__name__)


# GET /attendances
def get_all(*, db_session) -> PayrollAttendance:
    """Returns all attendances."""
    data = db_session.query(PayrollAttendance).all()
    return AttendancesRead(data=data)


# GET /attendances/{id}
def get_one_by_id(*, db_session, id: int) -> PayrollAttendance:
    """Returns a attendance based on the given id."""
    attendance = get_attendance_by_id(db_session=db_session, id=id)
    if not attendance:
        raise AppException(ErrorMessages.ResourceNotFound())
    return attendance


# GET /employees/{id}/attendances
def get_employee_attendances(*, db_session, id: int) -> PayrollAttendance:
    employee = get_employee_by_id(db_session=db_session, id=id)
    attendances = (
        db_session.query(PayrollAttendance)
        .filter(
            PayrollAttendance.employee_id == employee.id,
        )
        .all()
    )
    return AttendancesRead(data=attendances)


# POST /attendances
def create(*, db_session, attendance_in: AttendanceCreate) -> PayrollAttendance:
    """Creates a new attendance."""
    if check_exist_attendance(
        db_session=db_session,
        attendance_in=attendance_in,
        employee_id=attendance_in.employee_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists())

    if get_employee_by_id(db_session=db_session, id=attendance_in.employee_id) is None:
        raise AppException(ErrorMessages.ResourceNotFound())

    attendance = PayrollAttendance(**attendance_in.model_dump())
    employee = get_employee_by_id(db_session=db_session, id=attendance.employee_id)
    attendance.employee_name = employee.name
    db_session.add(attendance)
    db_session.commit()
    return attendance


# PUT /attendances/{id}
def update(
    *, db_session, id: int, attendance_in: AttendanceUpdate
) -> PayrollAttendance:
    """Updates a attendance with the given data."""
    attendance_db = get_attendance_by_id(db_session=db_session, id=id)

    if not attendance_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = attendance_in.model_dump(exclude_unset=True)

    db_session.query(PayrollAttendance).filter(PayrollAttendance.id == id).update(
        update_data, synchronize_session=False
    )

    db_session.commit()
    return attendance_db


# DELETE /attendances/{id}
def delete(*, db_session, id: int) -> PayrollAttendance:
    """Deletes a attendance based on the given id."""
    query = db_session.query(PayrollAttendance).filter(PayrollAttendance.id == id)
    attendance = query.first()

    if not attendance:
        raise AppException(ErrorMessages.ResourceNotFound())

    db_session.query(PayrollAttendance).filter(PayrollAttendance.id == id).delete()

    db_session.commit()
    return attendance

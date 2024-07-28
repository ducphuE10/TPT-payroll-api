from datetime import date
import logging
from sqlalchemy import extract

from payroll.attendances.schemas import (
    AttendanceCreate,
    AttendanceUpdate,
)
from payroll.models import PayrollAttendance


# add, retrieve, modify, remove
log = logging.getLogger(__name__)


def retrieve_attendances_by_month(
    *, db_session, employee_id: int, month: int, year: int
) -> PayrollAttendance:
    """Returns all attendances."""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.employee_id == employee_id,
        extract("month", PayrollAttendance.day_attendance) == month,
        extract("year", PayrollAttendance.day_attendance) == year,
    )
    count = query.count()
    attendances = query.all()
    return {"count": count, "data": attendances}


# GET /attendances
def retrieve_all_attendances(*, db_session) -> PayrollAttendance:
    """Returns all attendances."""
    query = db_session.query(PayrollAttendance)
    count = query.count()
    attendances = query.all()
    return {"count": count, "data": attendances}


def retrievce_attendance_by_employee(
    *, db_session, day_attendance: date, employee_id: int
):
    """Returns a attendance based on the given day and employee_id."""
    attendance = (
        db_session.query(PayrollAttendance)
        .filter(
            PayrollAttendance.day_attendance == day_attendance,
            PayrollAttendance.employee_id == employee_id,
        )
        .first()
    )
    return attendance


# GET /attendances/{attendance_id}
def retrieve_attendance_by_id(*, db_session, attendance_id: int) -> PayrollAttendance:
    """Returns a attendance based on the given id."""
    attendance = (
        db_session.query(PayrollAttendance)
        .filter(PayrollAttendance.id == attendance_id)
        .first()
    )
    return attendance


# GET /employees/{employee_id}/attendances
def retrieve_employee_attendances(*, db_session, employee_id: int) -> PayrollAttendance:
    """Returns all attendances of an employee."""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.employee_id == employee_id,
    )
    count = query.count()
    attendances = query.all()
    return {"count": count, "data": attendances}


# GET /attendances/test?m=1&y=2021
def retrieve_employee_attendances_by_month(
    *, db_session, month: int, year: int
) -> PayrollAttendance:
    """Retrieve all attendances of employees by month and year"""
    query = db_session.query(PayrollAttendance).filter(
        extract("month", PayrollAttendance.day_attendance) == month,
        extract("year", PayrollAttendance.day_attendance) == year,
    )
    count = query.count()
    attendances = query.all()

    return {"count": count, "data": attendances}


# POST /attendances
def add_attendance(*, db_session, attendance_in: AttendanceCreate) -> PayrollAttendance:
    """Creates a new attendance."""
    attendance = PayrollAttendance(**attendance_in.model_dump())
    db_session.add(attendance)
    db_session.commit()
    return attendance


# PUT /attendances/{attendance_id}
def modify_attendance(
    *, db_session, attendance_id: int, attendance_in: AttendanceUpdate
) -> PayrollAttendance:
    """Updates a attendance with the given data."""
    update_data = attendance_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.id == attendance_id
    )
    query.update(update_data, synchronize_session=False)
    db_session.commit()

    updated_attendance = query.first()
    return updated_attendance


# DELETE /attendances/{attendance_id}
def remove_attendance(*, db_session, attendance_id: int) -> PayrollAttendance:
    """Deletes a attendance based on the given id."""
    db_session.query(PayrollAttendance).filter(
        PayrollAttendance.id == attendance_id
    ).delete()
    db_session.commit()

from datetime import date
import logging
from sqlalchemy import and_, extract

from app.api.routes.attendances.schemas import (
    AttendanceCreate,
    AttendanceUpdate,
)
from app.db.models import PayrollAttendance

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


def retrieve_all_attendances(*, db_session, company_id: int) -> PayrollAttendance:
    """Returns all attendances."""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.company_id == company_id
    )
    count = query.count()
    attendances = query.all()

    return {"count": count, "data": attendances}


def retrieve_attendance_by_employee_and_day(
    *, db_session, day_attendance: date, employee_id: int
):
    """Returns a attendance based on the given day and employee."""
    return (
        db_session.query(PayrollAttendance)
        .filter(
            PayrollAttendance.day_attendance == day_attendance,
            PayrollAttendance.employee_id == employee_id,
        )
        .first()
    )


def retrieve_attendance_by_id(*, db_session, attendance_id: int) -> PayrollAttendance:
    """Returns a attendance based on the given id."""
    return (
        db_session.query(PayrollAttendance)
        .filter(PayrollAttendance.id == attendance_id)
        .first()
    )


def retrieve_employee_attendances(*, db_session, employee_id: int) -> PayrollAttendance:
    """Retrieve all attendances of an employee"""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.employee_id == employee_id,
    )
    count = query.count()
    attendances = query.all()

    return {"count": count, "data": attendances}


def retrieve_employee_attendances_by_month(
    *, db_session, employee_id: int, month: int, year: int
) -> PayrollAttendance:
    """Retrieve all attendances of an employee by month"""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.employee_id == employee_id,
        extract("month", PayrollAttendance.day_attendance) == month,
        extract("year", PayrollAttendance.day_attendance) == year,
    )
    count = query.count()
    attendances = query.all()

    return {"count": count, "data": attendances}


def retrieve_multi_attendances_by_month(
    *, db_session, company_id: int, month: int, year: int
) -> PayrollAttendance:
    """Returns all attendances by month."""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.company_id == company_id,
        extract("month", PayrollAttendance.day_attendance) == month,
        extract("year", PayrollAttendance.day_attendance) == year,
    )
    count = query.count()
    attendances = query.all()

    return {"count": count, "data": attendances}


def add_attendance(*, db_session, attendance_in: AttendanceCreate) -> PayrollAttendance:
    """Creates a new attendance."""
    attendance = PayrollAttendance(**attendance_in.model_dump())
    attendance.created_by = "admin"
    db_session.add(attendance)

    return attendance


def modify_attendance(
    *, db_session, attendance_id: int, attendance_in: AttendanceUpdate
) -> PayrollAttendance:
    """Updates a attendance with the given data."""
    update_data = attendance_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.id == attendance_id
    )
    query.update(update_data, synchronize_session=False)
    updated_attendance = query.first()

    return updated_attendance


def remove_attendance(*, db_session, attendance_id: int) -> PayrollAttendance:
    """Deletes a attendance based on the given id."""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.id == attendance_id
    )
    delete_attendance = query.first()
    query.delete()

    return delete_attendance


def remove_attendances(*, db_session, employee_id: int, from_date: date, to_date: date):
    """Deletes a attendance based on the given id."""
    query = db_session.query(PayrollAttendance).filter(
        PayrollAttendance.employee_id == employee_id,
        and_(
            PayrollAttendance.day_attendance >= from_date,
            PayrollAttendance.day_attendance <= to_date,
        ),
    )
    query.delete()

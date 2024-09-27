from datetime import date
import logging
from sqlalchemy import and_, extract

from payroll.overtimes.schemas import (
    OvertimeCreate,
    OvertimeUpdate,
)
from payroll.models import PayrollOvertime

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /overtimes
def retrieve_all_overtimes(*, db_session) -> PayrollOvertime:
    """Returns all overtimes."""
    query = db_session.query(PayrollOvertime)
    count = query.count()
    overtimes = query.all()

    return {"count": count, "data": overtimes}


def retrieve_overtime_by_employee_and_day(
    *, db_session, day_overtime: date, employee_id: int
):
    """Returns a overtime based on the given day and employee_id."""
    return (
        db_session.query(PayrollOvertime)
        .filter(
            PayrollOvertime.day_overtime == day_overtime,
            PayrollOvertime.employee_id == employee_id,
        )
        .all()
    )


def retrieve_employee_overtime_by_month(
    *, db_session, employee_id: int, month: int, year: int
) -> PayrollOvertime:
    """Returns all attendances of an employee."""
    query = db_session.query(PayrollOvertime).filter(
        PayrollOvertime.employee_id == employee_id,
        extract("month", PayrollOvertime.day_overtime) == month,
        extract("year", PayrollOvertime.day_overtime) == year,
    )
    count = query.count()
    overtimes = query.all()

    return {"count": count, "data": overtimes}


# GET /overtimes/{overtime_id}
def retrieve_overtime_by_id(*, db_session, overtime_id: int) -> PayrollOvertime:
    """Returns a overtime based on the given id."""
    return (
        db_session.query(PayrollOvertime)
        .filter(PayrollOvertime.id == overtime_id)
        .first()
    )


# GET /employees/{employee_id}/overtimes
def retrieve_employee_overtimes(*, db_session, employee_id: int) -> PayrollOvertime:
    """Returns all overtimes of an employee."""
    query = db_session.query(PayrollOvertime).filter(
        PayrollOvertime.employee_id == employee_id,
    )
    count = query.count()
    overtimes = query.all()

    return {"count": count, "data": overtimes}


# GET /overtimes/period?m=month&y=year
def retrieve_employee_overtimes_by_month(
    *, db_session, month: int, year: int
) -> PayrollOvertime:
    """Retrieve all overtimes of employees by month and year"""
    query = db_session.query(PayrollOvertime).filter(
        extract("month", PayrollOvertime.day_overtime) == month,
        extract("year", PayrollOvertime.day_overtime) == year,
    )
    count = query.count()
    overtimes = query.all()

    return {"count": count, "data": overtimes}


# POST /overtimes
def add_overtime(*, db_session, overtime_in: OvertimeCreate) -> PayrollOvertime:
    """Creates a new overtime."""
    overtime = PayrollOvertime(**overtime_in.model_dump())
    overtime.created_by = "admin"
    db_session.add(overtime)

    return overtime


# PUT /overtimes/{overtime_id}
def modify_overtime(
    *, db_session, overtime_id: int, overtime_in: OvertimeUpdate
) -> PayrollOvertime:
    """Updates a overtime with the given data."""
    update_data = overtime_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollOvertime).filter(PayrollOvertime.id == overtime_id)
    query.update(update_data, synchronize_session=False)
    updated_overtime = query.first()

    return updated_overtime


# DELETE /overtimes/{overtime_id}
def remove_overtime(*, db_session, overtime_id: int) -> PayrollOvertime:
    """Deletes a overtime based on the given id."""
    query = db_session.query(PayrollOvertime).filter(PayrollOvertime.id == overtime_id)
    delete_overtime = query.first()
    query.delete()

    return delete_overtime


def remove_overtimes(*, db_session, employee_id: int, from_date: date, to_date: date):
    """Deletes a attendance based on the given id."""
    query = db_session.query(PayrollOvertime).filter(
        PayrollOvertime.employee_id == employee_id,
        and_(
            PayrollOvertime.day_overtime >= from_date,
            PayrollOvertime.day_overtime <= to_date,
        ),
    )
    query.delete()

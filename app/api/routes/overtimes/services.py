import logging
from fastapi import File, UploadFile
from datetime import date, timedelta
import pandas as pd
from io import BytesIO

from app.api.routes.overtimes.repositories import (
    add_overtime,
    modify_overtime,
    remove_overtime,
    remove_overtimes,
    retrieve_all_overtimes,
    retrieve_overtime_by_employee_and_day,
    retrieve_overtime_by_id,
    retrieve_employee_overtimes_by_month,
    retrieve_employee_overtimes,
)
from app.api.routes.overtimes.schemas import (
    OvertimeCreate,
    OvertimeUpdate,
    OvertimesCreate,
    OvertimesDelete,
)
from app.api.routes.employees.repositories import (
    retrieve_all_employees,
    retrieve_employee_by_code,
)
from app.api.routes.employees.services import check_exist_employee_by_id
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_overtime_by_id(*, db_session, overtime_id: int):
    """Check if overtime exists by id"""
    return bool(retrieve_overtime_by_id(db_session=db_session, overtime_id=overtime_id))


def check_exist_overtime_by_employee_and_day(
    *, db_session, day_overtime: date, employee_id: int
):
    """Check if overtime exists by employee_id and day_overtime."""
    return bool(
        retrieve_overtime_by_employee_and_day(
            db_session=db_session,
            day_overtime=day_overtime,
            employee_id=employee_id,
        )
    )


def validate_overtime_hours(overtime_hours: float):
    """Check if overtime hours is valid."""
    if overtime_hours < 0 or overtime_hours > 24:
        raise False
    return True


def validate_create_overtime(*, overtime_in: OvertimeCreate):
    """Check if overtime is valid."""
    if overtime_in.day_overtime > date.today():
        raise AppException(ErrorMessages.InvalidInput(), "day overtime")

    if not validate_overtime_hours(overtime_in.overtime_hours):
        raise AppException(ErrorMessages.InvalidInput(), "overtime hours")

    return True


def validate_update_overtime(*, overtime_in: OvertimeCreate):
    """Check if overtime is valid"""
    if validate_overtime_hours(overtime_in.overtime_hours):
        return True


# GET /overtimes
def get_all_overtimes(*, db_session):
    """Returns all overtimes."""
    list_overtimes = retrieve_all_overtimes(db_session=db_session)
    if not list_overtimes["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "overtime")

    return list_overtimes


# GET /overtimes/{overtime_id}
def get_overtime_by_id(*, db_session, overtime_id: int):
    """Returns a overtime based on the given id."""
    if not check_exist_overtime_by_id(db_session=db_session, overtime_id=overtime_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "overtime")

    return retrieve_overtime_by_id(db_session=db_session, overtime_id=overtime_id)


# GET /employees/{employee_id}/overtimes
def get_employee_overtimes(*, db_session, employee_id: int):
    """Returns all overtimes of an employee."""
    if not check_exist_employee_by_id(db_session=db_session, employee_id=employee_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")
    list_overtimes = retrieve_employee_overtimes(
        db_session=db_session, employee_id=employee_id
    )

    if not list_overtimes["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "overtime")

    return list_overtimes


# GET /overtimes/period?m=month&y=year
def get_overtimes_by_month(*, db_session, month: int, year: int):
    """Returns all overtimes for a given month and year."""
    list_overtimes = retrieve_employee_overtimes_by_month(
        db_session=db_session, month=month, year=year
    )

    if not list_overtimes["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "overtime")

    return list_overtimes


# POST /overtimes
def create_overtime(*, db_session, overtime_in: OvertimeCreate):
    """Creates a new overtime."""
    if not check_exist_employee_by_id(
        db_session=db_session, employee_id=overtime_in.employee_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")
    if check_exist_overtime_by_employee_and_day(
        db_session=db_session,
        day_overtime=overtime_in.day_overtime,
        employee_id=overtime_in.employee_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "overtime")

    if validate_create_overtime(overtime_in=overtime_in):
        try:
            overtime = add_overtime(db_session=db_session, overtime_in=overtime_in)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return overtime


def create_multi_overtimes(
    *, db_session, overtime_list_in: OvertimesCreate, apply_all: bool = False
):
    overtimes = []
    count = 0
    list_id = []

    if apply_all:
        list_id = [
            employee.id
            for employee in retrieve_all_employees(db_session=db_session)["data"]
        ]

    else:
        list_id = [id for id in overtime_list_in.list_emp]

    for employee_id in list_id:
        if not check_exist_employee_by_id(
            db_session=db_session, employee_id=employee_id
        ):
            raise AppException(ErrorMessages.ResourceNotFound(), "employee")

        current_date = overtime_list_in.from_date
        while current_date <= overtime_list_in.to_date:
            overtime_in = OvertimeCreate(
                employee_id=employee_id,
                day_overtime=current_date,
                overtime_hours=overtime_list_in.overtime_hours,
            )
            if check_exist_overtime_by_employee_and_day(
                db_session=db_session,
                day_overtime=current_date,
                employee_id=employee_id,
            ):
                if validate_update_overtime(overtime_in=overtime_in):
                    try:
                        overtime_id = retrieve_overtime_by_employee_and_day(
                            db_session=db_session,
                            day_overtime=current_date,
                            employee_id=employee_id,
                        ).id
                        overtime = update_overtime(
                            db_session=db_session,
                            overtime_id=overtime_id,
                            overtime_in=overtime_in,
                        )
                        overtimes.append(overtime)
                        count += 1
                        db_session.commit()
                    except Exception as e:
                        db_session.rollback()
                        raise AppException(ErrorMessages.ErrSM99999(), str(e))

            else:
                if validate_create_overtime(overtime_in=overtime_in):
                    try:
                        overtime = add_overtime(
                            db_session=db_session,
                            overtime_in=overtime_in,
                        )

                        if overtime:
                            overtimes.append(overtime)
                            count += 1

                        db_session.commit()
                    except Exception as e:
                        db_session.rollback()
                        raise AppException(ErrorMessages.ErrSM99999(), str(e))

            current_date += timedelta(days=1)

    return {"count": count, "data": overtimes}


# PUT /overtimes/{overtime_id}
def update_overtime(*, db_session, overtime_id: int, overtime_in: OvertimeUpdate):
    """Updates a overtime with the given data."""
    if not check_exist_overtime_by_id(db_session=db_session, overtime_id=overtime_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "overtime")

    if validate_update_overtime(overtime_in=overtime_in):
        try:
            overtime = modify_overtime(
                db_session=db_session,
                overtime_id=overtime_id,
                overtime_in=overtime_in,
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return overtime


def delete_multi_overtimes(
    *,
    db_session,
    overtime_list_in: OvertimesDelete,
):
    list_id = []

    if overtime_list_in.to_date > date.today():
        overtime_list_in.to_date = date.today()

    if overtime_list_in.apply_all:
        list_id = [
            employee.id
            for employee in retrieve_all_employees(db_session=db_session)["data"]
        ]

    else:
        list_id = [id for id in overtime_list_in.list_emp]

    for employee_id in list_id:
        if not check_exist_employee_by_id(
            db_session=db_session, employee_id=employee_id
        ):
            raise AppException(ErrorMessages.ResourceNotFound(), "employee")

        current_date = overtime_list_in.from_date
        while current_date <= overtime_list_in.to_date:
            try:
                remove_overtimes(
                    db_session=db_session,
                    employee_id=employee_id,
                    from_date=overtime_list_in.from_date,
                    to_date=overtime_list_in.to_date,
                )
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                raise AppException(ErrorMessages.ErrSM99999(), str(e))

            current_date += timedelta(days=1)

    return {"message": "Deleted successfully"}


# DELETE /overtimes/{overtime_id}
def delete_overtime(*, db_session, overtime_id: int):
    """Deletes a overtime based on the given id."""
    if not check_exist_overtime_by_id(db_session=db_session, overtime_id=overtime_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "overtime")

    try:
        overtime = remove_overtime(db_session=db_session, overtime_id=overtime_id)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return overtime


def upload_excel(
    *,
    db_session,
    file: UploadFile = File(...),
    # update_on_exists: bool = False
):
    file_path = BytesIO(file.file.read())
    df = pd.read_excel(file_path, skiprows=2)
    data = []
    for _, row in df.iterrows():
        employee_code = row["Mã nhân viên"]
        for day_overtime, value in row.items():
            if day_overtime not in ["Mã nhân viên"]:
                try:
                    parsed_date = pd.to_datetime(day_overtime, format="%d/%m/%Y").date()
                except ValueError:
                    continue

                # Check if the value is NaN
                if pd.isna(value):
                    continue

                employee_id = retrieve_employee_by_code(
                    db_session=db_session, employee_code=employee_code
                ).id

                hours = value
                if hours != 0:
                    data.append(
                        {
                            "employee_id": employee_id,
                            "day_overtime": parsed_date,
                            "overtime_hours": hours,
                        }
                    )

    for overtime in data:
        add_overtime(
            db_session=db_session,
            overtime_in=OvertimeCreate(**overtime),
        )

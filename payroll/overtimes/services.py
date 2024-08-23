import logging
from fastapi import File, UploadFile
from datetime import date
import pandas as pd
from io import BytesIO

from payroll.overtimes.repositories import (
    add_overtime,
    modify_overtime,
    remove_overtime,
    retrieve_overtime_by_employee,
    retrieve_all_overtimes,
    retrieve_overtime_by_id,
    retrieve_employee_overtimes_by_month,
    retrieve_employee_overtimes,
)
from payroll.overtimes.schemas import (
    OvertimeCreate,
    OvertimeUpdate,
    TimeOvertimeHandlerBase,
    WorkhoursOvertimeHandlerBase,
)
from payroll.employees.repositories import (
    retrieve_employee_by_code,
    retrieve_employee_by_id,
)
from payroll.employees.services import check_exist_employee_by_id
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.schedule_details.repositories import (
    retrieve_schedule_details_by_schedule_id,
)

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_overtime_by_id(*, db_session, overtime_id: int):
    """Check if overtime exists by id"""
    return bool(retrieve_overtime_by_id(db_session=db_session, overtime_id=overtime_id))


def check_exist_overtime_by_employee(
    *, db_session, day_overtime: date, employee_id: int
):
    """Check if overtime exists by employee_id and day_overtime."""
    return bool(
        retrieve_overtime_by_employee(
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
    if check_exist_overtime_by_employee(
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


def overtime_handler(
    *,
    db_session,
    overtime_in: WorkhoursOvertimeHandlerBase | TimeOvertimeHandlerBase,
    update_on_exists: bool = False,
):
    """Handles overtime based on standard work field or specific times."""
    employee = retrieve_employee_by_id(
        db_session=db_session, employee_id=overtime_in.employee_id
    )
    # schedule = retrieve_schedule_by_id(
    #     db_session=db_session, schedule_id=employee.schedule_id
    # )
    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=employee.schedule_id
    )
    day_name = overtime_in.day_overtime.strftime("%A")

    shifts_list = [
        detail.shift for detail in schedule_details["data"] if detail.day == day_name
    ]

    if not shifts_list:
        return

    overtime_list = retrieve_overtime_by_employee(
        db_session=db_session,
        day_overtime=overtime_in.day_overtime,
        employee_id=employee.id,
    )

    if isinstance(overtime_in, WorkhoursOvertimeHandlerBase):
        try:
            overtime = add_overtime(
                db_session=db_session,
                overtime_in=OvertimeCreate(
                    employee_id=employee.id,
                    day_overtime=overtime_in.day_overtime,
                    overtime_hours=overtime_in.overtime_hours,
                ),
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))
    else:
        overtime_time_list = [overtime.check_time for overtime in overtime_list]

        if (
            overtime_in.checkin in overtime_time_list
            and overtime_in.checkout in overtime_time_list
        ):
            return

        for overtime in overtime_list:
            remove_overtime(db_session=db_session, overtime_id=overtime.id)

        add_overtime(
            db_session=db_session,
            overtime_in=OvertimeCreate(
                employee_id=employee.id,
                day_overtime=overtime_in.day_overtime,
                check_time=overtime_in.checkin,
            ),
        )
        add_overtime(
            db_session=db_session,
            overtime_in=OvertimeCreate(
                employee_id=employee.id,
                day_overtime=overtime_in.day_overtime,
                check_time=overtime_in.checkout,
            ),
        )


def upload_excel(
    *, db_session, file: UploadFile = File(...), update_on_exists: bool = False
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

                # Check if value is a float (overtime hours) or a time range (check-in/check-out)
                if isinstance(value, float | int):
                    hours = value
                    if hours != 0:
                        data.append(
                            {
                                "employee_id": employee_id,
                                "day_overtime": parsed_date,
                                "overtime_hours": hours,
                            }
                        )
                # elif isinstance(value, str) and "-" in value:
                #     checkin_str, checkout_str = value.split("-")
                #     checkin = pd.to_datetime(checkin_str, format="%H:%M").time()
                #     checkout = pd.to_datetime(checkout_str, format="%H:%M").time()
                #     hours = None
                #     data.append(
                #         {
                #             "employee_id": employee_id,
                #             "day_overtime": parsed_date,
                #             "checkin": checkin,
                #             "checkout": checkout,
                #         }
                #     )
                else:
                    continue
    for item in data:
        if item.get("overtime_hours"):
            overtime = WorkhoursOvertimeHandlerBase(**item)
        else:
            overtime = TimeOvertimeHandlerBase(**item)
        overtime_handler(
            db_session=db_session,
            overtime_in=overtime,
            update_on_exists=update_on_exists,
        )

import logging
from fastapi import File, UploadFile
from datetime import date
import pandas as pd
from io import BytesIO

from payroll.attendances.repositories import (
    add_attendance,
    modify_attendance,
    remove_attendance,
    retrievce_attendance_by_employee,
    retrieve_all_attendances,
    retrieve_attendance_by_id,
    retrieve_employee_attendances_by_month,
    retrieve_employee_attendances,
)
from payroll.attendances.schemas import (
    AttendanceCreate,
    AttendanceUpdate,
    TimeAttendanceHandlerBase,
    WorkhoursAttendanceHandlerBase,
)
from payroll.employees.repositories import retrieve_employee_by_id
from payroll.employees.services import check_exist_employee_by_id
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.schedule_details.repositories import retrieve_shifts_by_schedule_id
from payroll.schedules.repositories import retrieve_schedule_by_id

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_attendance_by_id(*, db_session, attendance_id: int) -> bool:
    """Check if attendance exists by id"""
    attendance = retrieve_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    )
    return attendance is not None


def check_exist_attendance_by_employee(
    *, db_session, day_attendance: date, employee_id: int
) -> bool:
    """Check if attendance exists by employee_id and day_attendance."""
    attendance = retrievce_attendance_by_employee(
        db_session=db_session, day_attendance=day_attendance, employee_id=employee_id
    )
    return attendance is not None


# GET /attendances
def get_all_attendances(*, db_session):
    """Returns all attendances."""
    list_attendances = retrieve_all_attendances(db_session=db_session)
    if not list_attendances["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return list_attendances


# GET /attendances/{attendance_id}
def get_attendance_by_id(*, db_session, attendance_id: int):
    """Returns a attendance based on the given id."""
    if not check_exist_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())

    attendance = retrieve_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    )
    return attendance


# GET /employees/{employee_id}/attendances
def get_employee_attendances(*, db_session, employee_id: int):
    """Returns all attendances of an employee."""
    if not check_exist_employee_by_id(db_session=db_session, employee_id=employee_id):
        raise AppException(ErrorMessages.ResourceNotFound())
    list_attendances = retrieve_employee_attendances(
        db_session=db_session, employee_id=employee_id
    )

    if not list_attendances["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return list_attendances


# GET /attendances/test?m=1&y=2021
def get_attendances_by_month(*, db_session, month: int, year: int):
    """Returns all attendances for a given month and year."""
    list_attendances = retrieve_employee_attendances_by_month(
        db_session=db_session, month=month, year=year
    )

    if not list_attendances["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return list_attendances


# POST /attendances
def create_attendance(*, db_session, attendance_in: AttendanceCreate):
    """Creates a new attendance."""
    if not check_exist_employee_by_id(
        db_session=db_session, employee_id=attendance_in.employee_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())

    if check_exist_attendance_by_employee(
        db_session=db_session,
        day_attendance=attendance_in.day_attendance,
        employee_id=attendance_in.employee_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists())

    attendance = add_attendance(db_session=db_session, attendance_in=attendance_in)

    return attendance


# PUT /attendances/{attendance_id}
def update_attendance(
    *, db_session, attendance_id: int, attendance_in: AttendanceUpdate
):
    """Updates a attendance with the given data."""
    if not check_exist_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    updated_attendance = modify_attendance(
        db_session=db_session, attendance_id=attendance_id, attendance_in=attendance_in
    )
    return updated_attendance


# DELETE /attendances/{attendance_id}
def delete_attendance(*, db_session, attendance_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    remove_attendance(db_session=db_session, attendance_id=attendance_id)
    return {"message": "Attendance deleted successfully"}


def attendance_handler(
    *,
    db_session,
    attendance_in: WorkhoursAttendanceHandlerBase | TimeAttendanceHandlerBase,
):
    """Use when input has standard work field"""
    employee = retrieve_employee_by_id(
        db_session=db_session, employee_id=attendance_in.employee_id
    )
    schedule = retrieve_schedule_by_id(
        db_session=db_session, schedule_id=employee.schedule_id
    )
    shift_data = retrieve_shifts_by_schedule_id(
        db_session=db_session, schedule_id=schedule.id
    )
    shifts_list = [
        detail.shift
        for detail in shift_data["data"]
        if detail.day == attendance_in.day_attendance.strftime("%A")
    ]
    if not shifts_list:
        return

    if isinstance(attendance_in, WorkhoursAttendanceHandlerBase):
        standard_checkin = min(shift.checkin for shift in shifts_list)
        standard_checkout = max(shift.checkout for shift in shifts_list)

        add_attendance(
            db_session=db_session,
            attendance_in=AttendanceCreate(
                employee_id=employee.id,
                day_attendance=attendance_in.day_attendance,
                check_time=standard_checkin,
            ),
        )
        add_attendance(
            db_session=db_session,
            attendance_in=AttendanceCreate(
                employee_id=employee.id,
                day_attendance=attendance_in.day_attendance,
                check_time=standard_checkout,
            ),
        )
    else:
        add_attendance(
            db_session=db_session,
            attendance_in=AttendanceCreate(
                employee_id=employee.id,
                day_attendance=attendance_in.day_attendance,
                check_time=attendance_in.checkin,
            ),
        )
        add_attendance(
            db_session=db_session,
            attendance_in=AttendanceCreate(
                employee_id=employee.id,
                day_attendance=attendance_in.day_attendance,
                check_time=attendance_in.checkout,
            ),
        )


def upload_excel(*, db_session, file: UploadFile = File(...)):
    file_path = BytesIO(file.file.read())
    df = pd.read_excel(file_path, skiprows=2)

    data = []
    for _, row in df.iterrows():
        employee_id = row["Employee ID"]
        for day_attendance, value in row.items():
            if day_attendance not in ["Employee ID"]:
                try:
                    parsed_date = pd.to_datetime(
                        day_attendance, format="%d/%m/%Y"
                    ).date()
                except ValueError:
                    continue

                # Check if the value is NaN
                if pd.isna(value):
                    continue

                # Check if value is a float (work hours) or a time range (check-in/check-out)
                if isinstance(value, float | int):
                    hours = value
                    checkin = checkout = None
                    if hours != 0:
                        data.append(
                            {
                                "employee_id": employee_id,
                                "day_attendance": parsed_date,
                                "work_hours": hours,
                            }
                        )
                elif isinstance(value, str) and "-" in value:
                    checkin_str, checkout_str = value.split("-")
                    checkin = pd.to_datetime(checkin_str, format="%H:%M").time()
                    checkout = pd.to_datetime(checkout_str, format="%H:%M").time()
                    hours = None
                    data.append(
                        {
                            "employee_id": employee_id,
                            "day_attendance": parsed_date,
                            "checkin": checkin,
                            "checkout": checkout,
                        }
                    )
                else:
                    continue

    for item in data:
        if item.get("work_hours"):
            attendance = WorkhoursAttendanceHandlerBase(**item)
        else:
            attendance = TimeAttendanceHandlerBase(**item)
        attendance_handler(db_session=db_session, attendance_in=attendance)

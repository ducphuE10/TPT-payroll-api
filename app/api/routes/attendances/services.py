import logging
from fastapi import File, UploadFile
from datetime import date, timedelta
import pandas as pd
from io import BytesIO

from app.api.routes.attendances.repositories import (
    add_attendance,
    modify_attendance,
    remove_attendance,
    remove_attendances,
    retrieve_all_attendances,
    retrieve_attendance_by_employee_and_day,
    retrieve_attendance_by_id,
    retrieve_employee_attendances,
    retrieve_multi_attendances_by_month,
)
from app.api.routes.attendances.schemas import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendancesCreate,
    AttendancesDelete,
    TimeAttendanceHandlerBase,
    WorkhoursAttendanceHandlerBase,
)

# from payroll.contracts.services import get_active_contract
from app.api.routes.employees.repositories import (
    retrieve_all_employees,
    retrieve_employee_by_code,
    retrieve_employee_by_id,
)
from app.api.routes.employees.services import check_exist_employee_by_id
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages
from app.api.routes.schedule_details.repositories import (
    retrieve_schedule_details_by_schedule_id,
)
from app.api.routes.schedules.services import (
    check_exist_schedule_by_employee_id,
)

# create, get, update, delete
log = logging.getLogger(__name__)


def check_exist_attendance_by_id(*, db_session, attendance_id: int):
    """Check if attendance exists by id"""
    return bool(
        retrieve_attendance_by_id(db_session=db_session, attendance_id=attendance_id)
    )


def check_exist_attendance_by_employee_and_day(
    *, db_session, day_attendance: date, employee_id: int
):
    """Check if attendance exists by employee_id and day_attendance."""
    return bool(
        retrieve_attendance_by_employee_and_day(
            db_session=db_session,
            day_attendance=day_attendance,
            employee_id=employee_id,
        )
    )


def validate_work_hours(work_hours: float):
    """Check if work hours is valid."""
    if work_hours < 0 or work_hours > 24:
        raise False
    return True


def validate_create_attendance(*, attendance_in: AttendanceCreate):
    """Check if attendance is valid."""
    if attendance_in.day_attendance > date.today():
        raise AppException(ErrorMessages.InvalidInput(), "day attendance")

    if not validate_work_hours(attendance_in.work_hours):
        raise AppException(ErrorMessages.InvalidInput(), "work hours")

    return True


def validate_update_attendance(*, attendance_in: AttendanceCreate):
    """Check if attendance is valid"""
    if validate_work_hours(attendance_in.work_hours):
        return True


# GET /attendances
def get_all_attendances(*, db_session, company_id: int):
    """Returns all attendances."""
    list_attendances = retrieve_all_attendances(
        db_session=db_session, company_id=company_id
    )
    if not list_attendances["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "attendance")

    return list_attendances


# GET /attendances/{attendance_id}
def get_attendance_by_id(*, db_session, attendance_id: int):
    """Returns a attendance based on the given id."""
    if not check_exist_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "attendance")

    return retrieve_attendance_by_id(db_session=db_session, attendance_id=attendance_id)


# GET /employees/{employee_id}/attendances
def get_employee_attendances(*, db_session, employee_id: int):
    """Returns all attendances of an employee."""
    if not check_exist_employee_by_id(db_session=db_session, employee_id=employee_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")
    list_attendances = retrieve_employee_attendances(
        db_session=db_session, employee_id=employee_id
    )

    if not list_attendances["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "attendance")

    return list_attendances


# GET /attendances/period?m=month&y=year
def get_multi_attendances_by_month(
    *, db_session, company_id: int, month: int, year: int
):
    """Returns all attendances for a given month and year."""
    list_attendances = retrieve_multi_attendances_by_month(
        db_session=db_session, month=month, year=year, company_id=company_id
    )

    if not list_attendances["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "attendance")

    return list_attendances


# POST /attendances
def create_attendance(*, db_session, attendance_in: AttendanceCreate):
    """Creates a new attendance."""
    if not check_exist_employee_by_id(
        db_session=db_session, employee_id=attendance_in.employee_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")
    if check_exist_attendance_by_employee_and_day(
        db_session=db_session,
        day_attendance=attendance_in.day_attendance,
        employee_id=attendance_in.employee_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "attendance")

    if validate_create_attendance(attendance_in=attendance_in):
        try:
            attendance = add_attendance(
                db_session=db_session, attendance_in=attendance_in
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return attendance


# POST /attendances/bulk
def create_multi_attendances(
    *,
    db_session,
    attendance_list_in: AttendancesCreate,
):
    attendances = []
    count = 0
    list_id = []

    if attendance_list_in.to_date > date.today():
        attendance_list_in.to_date = date.today()

    if attendance_list_in.apply_all:
        for employee in retrieve_all_employees(
            db_session=db_session, company_id=attendance_list_in.company_id
        )["data"]:
            if check_exist_schedule_by_employee_id(
                db_session=db_session, employee_id=employee.id
            ):
                list_id.append(employee.id)
    else:
        list_id = [id for id in attendance_list_in.list_emp]

    for employee_id in list_id:
        if not check_exist_employee_by_id(
            db_session=db_session, employee_id=employee_id
        ):
            raise AppException(ErrorMessages.ResourceNotFound(), "employee")

        if not check_exist_schedule_by_employee_id(
            db_session=db_session, employee_id=employee_id
        ):
            raise AppException(
                ErrorMessages.ResourceNotFound(), f"schedule of employee {employee_id}"
            )

        current_date = attendance_list_in.from_date
        while current_date <= attendance_list_in.to_date:
            attendance_in = AttendanceCreate(
                employee_id=employee_id,
                day_attendance=current_date,
                work_hours=attendance_list_in.work_hours,
                is_holiday=attendance_list_in.is_holiday,
                company_id=attendance_list_in.company_id,
            )
            if check_exist_attendance_by_employee_and_day(
                db_session=db_session,
                day_attendance=current_date,
                employee_id=employee_id,
            ):
                if validate_update_attendance(attendance_in=attendance_in):
                    try:
                        attendance_id = retrieve_attendance_by_employee_and_day(
                            db_session=db_session,
                            day_attendance=current_date,
                            employee_id=employee_id,
                        ).id
                        attendance = update_attendance(
                            db_session=db_session,
                            attendance_id=attendance_id,
                            attendance_in=attendance_in,
                        )
                        attendances.append(attendance)
                        count += 1
                        db_session.commit()
                    except Exception as e:
                        db_session.rollback()
                        raise AppException(ErrorMessages.ErrSM99999(), str(e))

            else:
                if validate_create_attendance(attendance_in=attendance_in):
                    try:
                        attendance_in = WorkhoursAttendanceHandlerBase(
                            **attendance_in.model_dump()
                        )
                        attendance = attendance_handler(
                            db_session=db_session,
                            attendance_in=attendance_in,
                        )

                        if attendance:
                            attendances.append(attendance)
                            count += 1

                        db_session.commit()
                    except Exception as e:
                        db_session.rollback()
                        raise AppException(ErrorMessages.ErrSM99999(), str(e))

            current_date += timedelta(days=1)

    return {"count": count, "data": attendances}


# PUT /attendances/{attendance_id}
def update_attendance(
    *, db_session, attendance_id: int, attendance_in: AttendanceUpdate
):
    """Updates a attendance with the given data."""
    if not check_exist_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "attendance")

    if validate_update_attendance(attendance_in=attendance_in):
        try:
            attendance = modify_attendance(
                db_session=db_session,
                attendance_id=attendance_id,
                attendance_in=attendance_in,
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return attendance


def delete_multi_attendances(
    *,
    db_session,
    attendance_list_in: AttendancesDelete,
):
    list_id = []

    if attendance_list_in.to_date > date.today():
        attendance_list_in.to_date = date.today()

    if attendance_list_in.apply_all:
        list_id = [
            employee.id
            for employee in retrieve_all_employees(db_session=db_session)["data"]
        ]

    else:
        list_id = [id for id in attendance_list_in.list_emp]

    for employee_id in list_id:
        if not check_exist_employee_by_id(
            db_session=db_session, employee_id=employee_id
        ):
            raise AppException(ErrorMessages.ResourceNotFound(), "employee")

        current_date = attendance_list_in.from_date
        while current_date <= attendance_list_in.to_date:
            try:
                remove_attendances(
                    db_session=db_session,
                    employee_id=employee_id,
                    from_date=attendance_list_in.from_date,
                    to_date=attendance_list_in.to_date,
                )
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                raise AppException(ErrorMessages.ErrSM99999(), str(e))

            current_date += timedelta(days=1)

    return {"message": "Deleted successfully"}


# DELETE /attendances/{attendance_id}
def delete_attendance(*, db_session, attendance_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "attendance")

    try:
        attendance = remove_attendance(
            db_session=db_session, attendance_id=attendance_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return attendance


def attendance_handler(
    *,
    db_session,
    attendance_in: WorkhoursAttendanceHandlerBase | TimeAttendanceHandlerBase,
):
    """Handles attendance based on standard work field or specific times."""
    employee = retrieve_employee_by_id(
        db_session=db_session, employee_id=attendance_in.employee_id
    )

    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=employee.schedule_id
    )
    day_name = attendance_in.day_attendance.strftime("%A")

    shifts_list = [
        detail.shift for detail in schedule_details["data"] if detail.day == day_name
    ]

    if not shifts_list:
        return

    attendance_list = retrieve_attendance_by_employee_and_day(
        db_session=db_session,
        day_attendance=attendance_in.day_attendance,
        employee_id=employee.id,
    )

    if isinstance(attendance_in, WorkhoursAttendanceHandlerBase):
        try:
            attendance = add_attendance(
                db_session=db_session,
                attendance_in=AttendanceCreate(
                    employee_id=employee.id,
                    day_attendance=attendance_in.day_attendance,
                    work_hours=attendance_in.work_hours,
                    is_holiday=attendance_in.is_holiday,
                    company_id=attendance_in.company_id,
                ),
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

        return attendance
    else:
        attendance_time_list = [attendance.check_time for attendance in attendance_list]

        if (
            attendance_in.checkin in attendance_time_list
            and attendance_in.checkout in attendance_time_list
        ):
            return

        for attendance in attendance_list:
            remove_attendance(db_session=db_session, attendance_id=attendance.id)

        add_attendance(
            db_session=db_session,
            attendance_in=AttendanceCreate(
                employee_id=employee.id,
                day_attendance=attendance_in.day_attendance,
                check_time=attendance_in.checkin,
                company_id=attendance_in.company_id,
            ),
        )
        add_attendance(
            db_session=db_session,
            attendance_in=AttendanceCreate(
                employee_id=employee.id,
                day_attendance=attendance_in.day_attendance,
                check_time=attendance_in.checkout,
                company_id=attendance_in.company_id,
            ),
        )


# POST /attendances/import-excel
def upload_excel(
    *,
    db_session,
    file: UploadFile = File(...),
):
    file_path = BytesIO(file.file.read())
    df = pd.read_excel(file_path, skiprows=3)
    data = []
    for _, row in df.iterrows():
        employee_code = row["Mã nhân viên"]
        for day_attendance, value in row.items():
            if day_attendance not in ["Mã nhân viên"]:
                try:
                    parsed_date = pd.to_datetime(
                        day_attendance, format="%d/%m/%Y"
                    ).date()
                except ValueError:
                    continue

                if pd.isna(value):
                    continue

                employee_id = retrieve_employee_by_code(
                    db_session=db_session, employee_code=employee_code
                ).id

                # Check if value is a float (work hours) or a time range (check-in/check-out)
                if isinstance(value, float | int):
                    hours = value
                    if hours != 0:
                        data.append(
                            {
                                "employee_id": employee_id,
                                "day_attendance": parsed_date,
                                "work_hours": hours,
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
                #             "day_attendance": parsed_date,
                #             "checkin": checkin,
                #             "checkout": checkout,
                #         }
                #     )

                else:
                    continue
    for item in data:
        if item.get("work_hours"):
            attendance = WorkhoursAttendanceHandlerBase(**item)
        else:
            attendance = TimeAttendanceHandlerBase(**item)
        attendance_handler(
            db_session=db_session,
            attendance_in=attendance,
        )

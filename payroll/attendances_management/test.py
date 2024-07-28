from sqlalchemy import extract
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from payroll.config import settings
from payroll.models import (
    PayrollAttendance,
    PayrollEmployee,
    PayrollSchedule,
    PayrollScheduleDetail,
)

# Assuming you have your database URL

# Create a new session
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def get_attendance_records(session: Session, employee_id: int, month: int, year: int):
    return (
        session.query(PayrollAttendance)
        .filter(
            PayrollAttendance.employee_id == employee_id,
            extract("month", PayrollAttendance.day_attendance) == month,
            extract("year", PayrollAttendance.day_attendance) == year,
        )
        .all()
    )


def get_employee_schedule(session: Session, employee_id: int):
    # Assuming there's an association between employee and schedule
    return (
        session.query(PayrollScheduleDetail)
        .join(PayrollSchedule, PayrollSchedule.id == PayrollScheduleDetail.schedule_id)
        .join(PayrollEmployee, PayrollEmployee.schedule_id == PayrollSchedule.id)
        .filter(PayrollEmployee.id == employee_id)
        .all()
    )


def match_attendance_with_shifts(attendance_records, schedule_details):
    # Create a mapping of day to shifts
    schedule_map = {}
    for detail in schedule_details:
        if detail.day not in schedule_map:
            schedule_map[detail.day] = []
        schedule_map[detail.day].append(detail)
    print(schedule_map)

    # Match attendance records with shifts
    attendance_summary = {}
    for record in attendance_records:
        day = record.day_attendance
        if day not in attendance_summary:
            attendance_summary[day] = {}

        for detail in schedule_map.get(day, []):
            shift = detail.shift
            if detail.shift_id not in attendance_summary[day]:
                attendance_summary[day][detail.shift_id] = {
                    "shift": shift,
                    "check_times": [],
                    "total_hours": timedelta(),
                }

            if shift.earliest_checkin <= record.check_time <= shift.latest_checkout:
                attendance_summary[day][detail.shift_id]["check_times"].append(
                    record.check_time
                )

    return attendance_summary


def summarize_attendance(attendance_summary):
    for day, shifts in attendance_summary.items():
        for shift_id, data in shifts.items():
            check_times = sorted(data["check_times"])
            if (
                len(check_times) >= 2
            ):  # Ensure there's at least one check-in and one check-out
                checkin_time = datetime.combine(day, check_times[0])
                checkout_time = datetime.combine(day, check_times[-1])
                data["total_hours"] = checkout_time - checkin_time

    return attendance_summary


def calculate_monthly_summary(attendance_summary):
    total_hours = timedelta()
    days_worked = set()
    shift_hours = {}

    for day, shifts in attendance_summary.items():
        days_worked.add(day)
        for shift_id, data in shifts.items():
            total_hours += data["total_hours"]
            if shift_id not in shift_hours:
                shift_hours[shift_id] = timedelta()
            shift_hours[shift_id] += data["total_hours"]

    return {
        "total_hours": total_hours,
        "days_worked": len(days_worked),
        "shift_hours": shift_hours,
    }


employee_id = 1  # Example employee ID
month = 7  # July
year = 2024

# Fetch attendance records
attendance_records = get_attendance_records(session, employee_id, month, year)

# Fetch employee schedule
employee_schedule = get_employee_schedule(session, employee_id)

# Match attendance with shifts
attendance_summary = match_attendance_with_shifts(attendance_records, employee_schedule)

# Summarize attendance
summarized_attendance = summarize_attendance(attendance_summary)

# Calculate monthly summary
monthly_summary = calculate_monthly_summary(summarized_attendance)

print("Total hours worked:", monthly_summary["total_hours"])
print("Days worked:", monthly_summary["days_worked"])
for shift_id, hours in monthly_summary["shift_hours"].items():
    print(f"Total hours for shift {shift_id}: {hours}")

# Close the session
session.close()

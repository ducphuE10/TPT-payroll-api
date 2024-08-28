from datetime import date, timedelta
from payroll.attendances.repositories import (
    retrieve_attendance_by_id,
    retrieve_employee_attendances_by_month,
)
from payroll.benefits.repositories import retrieve_benefit_by_id
from payroll.contract_benefit_assocs.repositories import (
    retrieve_cbassocs_by_contract_id,
)
from payroll.contract_types.repositories import get_contract_type_by_code
from payroll.contracts.repositories import (
    retrieve_contract_by_employee_id_and_period,
)
from payroll.employees.repositories import retrieve_employee_by_id
from payroll.insurances.repositories import get_insurance_policy_by_id
from payroll.models import PayrollScheduleDetail
from payroll.overtimes.repositories import retrieve_employee_overtime_by_month
from payroll.payroll_managements.repositories import (
    add_payroll_management,
    remove_payroll_management,
    retrieve_all_payroll_managements,
    retrieve_payroll_management_by_id,
    retrieve_payroll_management_by_information,
)
from payroll.payroll_managements.schemas import PayrollManagementCreate
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.schedule_details.repositories import (
    retrieve_schedule_details_by_schedule_id,
)
from payroll.shifts.repositories import retrieve_shift_by_id
from payroll.utils.models import Day


def check_exist_payroll_management_by_id(*, db_session, payroll_management_id: int):
    """Check if payroll_management exists in the database."""
    return bool(
        retrieve_payroll_management_by_id(
            db_session=db_session, payroll_management_id=payroll_management_id
        )
    )


def check_exist_payroll_management_by_information(
    *, db_session, employee_id: int, contract_id: int, month: date
):
    """Check if payroll_management exists in the database."""
    return bool(
        retrieve_payroll_management_by_information(
            db_session=db_session,
            employee_id=employee_id,
            contract_id=contract_id,
            month=month,
        )
    )


# GET /payroll_managements/{payroll_management_id}
def get_payroll_management_by_id(*, db_session, payroll_management_id: int):
    """Returns a payroll_management based on the given id."""
    if not check_exist_payroll_management_by_id(
        db_session=db_session, payroll_management_id=payroll_management_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "payroll")

    return retrieve_payroll_management_by_id(
        db_session=db_session, payroll_management_id=payroll_management_id
    )


# GET /payroll_managements
def get_all_payroll_management(*, db_session):
    """Returns all payroll_managements."""
    payroll_managements = retrieve_all_payroll_managements(db_session=db_session)
    if not payroll_managements["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "payroll")

    return payroll_managements


# # POST /payroll_managements
# def create_payroll_management(
#     *, db_session, payroll_management_in: PayrollManagementCreate
# ):

#     try:
#         payroll_management = add_payroll_management(
#             db_session=db_session, payroll_management_in=payroll_management_in
#         )
#         db_session.commit()
#     except Exception as e:
#         db_session.rollback()
#         raise e

#     return payroll_management
# POST /payroll_managements


def create_payroll_management(
    *, db_session, payroll_management_in: PayrollManagementCreate
):
    value = net_income_handler(
        db_session=db_session,
        employee_id=payroll_management_in.employee_id,
        month=payroll_management_in.month,
    )

    employee_code = retrieve_employee_by_id(
        db_session=db_session, employee_id=payroll_management_in.employee_id
    ).code

    last_day = get_last_day_of_month(date_obj=payroll_management_in.month)

    contract_id = retrieve_contract_by_employee_id_and_period(
        db_session=db_session,
        employee_code=employee_code,
        from_date=payroll_management_in.month,
        to_date=last_day,
    ).id

    try:
        payroll_management = add_payroll_management(
            db_session=db_session,
            payroll_management_in=payroll_management_in,
            value=value,
            contract_id=contract_id,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return payroll_management


# DELETE /payroll_managements/{payroll_management_id}
def delete_payroll_management(*, db_session, payroll_management_id: int):
    """Deletes a payroll_management based on the given id."""
    if not check_exist_payroll_management_by_id(
        db_session=db_session, payroll_management_id=payroll_management_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "payroll_management")

    try:
        payroll_management = remove_payroll_management(
            db_session=db_session, payroll_management_id=payroll_management_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return payroll_management


def work_hours_standard_handler(*, db_session, schedule_details: PayrollScheduleDetail):
    # employee = retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)
    # schedule_id = employee.schedule_id
    # schedule_details = retrieve_schedule_details_by_schedule_id(
    #     db_session=db_session, schedule_id=schedule_id
    # )

    work_hours_standard = 0
    for schedule_detail in schedule_details["data"]:
        shift_work_hours = retrieve_shift_by_id(
            db_session=db_session, shift_id=schedule_detail.shift_id
        ).standard_work_hours

        work_hours_standard = shift_work_hours

    return work_hours_standard


def work_days_standard_handler(*, schedule_details: PayrollScheduleDetail):
    # employee = retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)
    # schedule_id = employee.schedule_id
    # schedule_details = retrieve_schedule_details_by_schedule_id(
    #     db_session=db_session, schedule_id=schedule_id
    # )

    work_days_list = {
        schedule_detail.day for schedule_detail in schedule_details["data"]
    }

    work_days_standard = 0

    if len(work_days_list) == 6:
        work_days_standard = 26
        return work_days_standard

    elif len(work_days_list) == 5:
        work_days_standard = 24
        return work_days_standard


def check_sufficient_work_hours(*, db_session, schedule_id: int, attendance_id: int):
    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )
    attendance = retrieve_attendance_by_id(
        db_session=db_session, attendance_id=attendance_id
    )

    day = attendance.day_attendance.strftime("%A")

    matching_schedule_detail = next(
        (detail for detail in schedule_details["data"] if detail.day == day), None
    )

    shift_work_hours = retrieve_shift_by_id(
        db_session=db_session, shift_id=matching_schedule_detail.shift_id
    ).standard_work_hours

    if attendance.work_hours >= shift_work_hours:
        return {"status": True, "work_hours": shift_work_hours}
    else:
        return {"status": False, "work_hours": attendance.work_hours}


def work_hours_handler(*, db_session, employee_id: int, schedule_id: int, month: date):
    # employee = retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)
    # schedule_id = employee.schedule_id
    attendances = retrieve_employee_attendances_by_month(
        db_session=db_session,
        employee_id=employee_id,
        month=month.month,
        year=month.year,
    )

    adequate_hours = 0
    under_hours = 0

    for attendance in attendances["data"]:
        if check_sufficient_work_hours(
            db_session=db_session, schedule_id=schedule_id, attendance_id=attendance.id
        )["status"]:
            adequate_hours += check_sufficient_work_hours(
                db_session=db_session,
                schedule_id=schedule_id,
                attendance_id=attendance.id,
            )["work_hours"]
        else:
            under_hours += check_sufficient_work_hours(
                db_session=db_session,
                schedule_id=schedule_id,
                attendance_id=attendance.id,
            )["work_hours"]

    return {"adequate_hours": adequate_hours, "under_hours": under_hours}


def overtime_hours_handler(*, db_session, employee_id: int, month: date):
    overtimes = retrieve_employee_overtime_by_month(
        db_session=db_session,
        employee_id=employee_id,
        month=month.month,
        year=month.year,
    )

    overtime_1_5x = 0
    overtime_2_0x = 0

    for overtime in overtimes["data"]:
        if overtime.day_overtime.strftime("%A") == Day.Sun:
            overtime_2_0x += overtime.overtime_hours
        else:
            overtime_1_5x += overtime.overtime_hours

    return {"overtime_1_5x": overtime_1_5x, "overtime_2_0x": overtime_2_0x}


def get_last_day_of_month(date_obj: date) -> date:
    next_month = date_obj.replace(day=28) + timedelta(days=4)  # Move to the next month
    return next_month.replace(day=1) - timedelta(
        days=1
    )  # Subtract one day to get the last day of the current month


def tax_handler(income: float):
    if income > 80000000:
        tax = ((income - 80000000) * 0.35) + 18150000
    elif income > 52000000:
        tax = ((income - 52000000) * 0.3) + 9750000
    elif income > 32000000:
        tax = ((income - 32000000) * 0.25) + 4750000
    elif income > 18000000:
        tax = ((income - 18000000) * 0.2) + 1950000
    elif income > 10000000:
        tax = ((income - 10000000) * 0.15) + 750000
    elif income > 5000000:
        tax = ((income - 5000000) * 0.1) + 250000
    else:
        tax = income * 0.05

    return round(tax, 0)


def net_income_handler(*, db_session, employee_id: int, month: date):
    employee = retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)

    employee_code = retrieve_employee_by_id(
        db_session=db_session, employee_id=employee_id
    ).code
    schedule_id = employee.schedule_id

    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )

    last_day = get_last_day_of_month(date_obj=month)
    contract = retrieve_contract_by_employee_id_and_period(
        db_session=db_session,
        employee_code=employee_code,
        from_date=month,
        to_date=last_day,
    )

    work_days_standard = work_days_standard_handler(schedule_details=schedule_details)

    work_hours_standard = work_hours_standard_handler(
        db_session=db_session, schedule_details=schedule_details
    )

    work_hours = work_hours_handler(
        db_session=db_session,
        employee_id=employee_id,
        schedule_id=schedule_id,
        month=month,
    )

    basic_salary = contract.basic_salary

    # WORK HOURS SALARY
    work_hours_salary = (
        basic_salary
        / work_days_standard
        / work_hours_standard
        * work_hours["adequate_hours"]
    )

    # OVERTIME HOURS SALARY
    overtime_hours = overtime_hours_handler(
        db_session=db_session, employee_id=employee_id, month=month
    )

    overtime_1_5x_salary = (
        basic_salary
        / work_days_standard
        / work_hours_standard
        * 1.5
        * overtime_hours["overtime_1_5x"]
    )

    overtime_2_0x_salary = (
        basic_salary
        / work_days_standard
        / work_hours_standard
        * 2
        * overtime_hours["overtime_2_0x"]
    )

    # BENEFIT
    benefit_salary = 0
    if work_days_standard == work_hours["adequate_hours"] / work_hours_standard:
        benefit_salary += 600000  # PHU CAP CHUYEN CAN

    for cbassoc in retrieve_cbassocs_by_contract_id(
        db_session=db_session, contract_id=contract.id
    )["data"]:
        benefit_value = retrieve_benefit_by_id(
            db_session=db_session, benefit_id=cbassoc.benefit_id
        ).value
        benefit_salary += (
            benefit_value
            / work_days_standard
            / work_hours_standard
            * work_hours["adequate_hours"]
        )

    gross_income = (
        work_hours_salary + overtime_1_5x_salary + overtime_2_0x_salary + benefit_salary
    )

    # DEDUCTION HANDLER

    contract_type = get_contract_type_by_code(
        db_session=db_session, code=contract.type_code
    )

    # INSURANCE HANDLER
    insurance_policy = get_insurance_policy_by_id(
        db_session=db_session, id=contract_type.insurance_policy_id
    )

    employee_insurance = basic_salary * insurance_policy.employee_percentage / 100
    company_insurance = basic_salary * insurance_policy.company_percentage / 100  # noqa

    # NO TAX HANDLER
    no_tax_salary = 650000 + (  # TIEN AN
        overtime_1_5x_salary
        + overtime_2_0x_salary
        - basic_salary
        / work_days_standard
        / work_hours_standard
        * (overtime_hours["overtime_1_5x"] + overtime_hours["overtime_2_0x"])
    )

    # NPT HANDLER
    dependent_pers = 1  # hardcode

    # TAX SALARY HANDLER
    tax_salary = max(
        gross_income
        - employee_insurance
        - no_tax_salary
        - 11000000
        - 4400000 * dependent_pers,
        0,
    )

    # TAX HANDLER
    tax = tax_handler(income=tax_salary)

    total_deduction = employee_insurance + tax

    net_income = round(gross_income - total_deduction, -3)

    return net_income

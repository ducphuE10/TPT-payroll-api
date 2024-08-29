from datetime import date, datetime, timedelta
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
from payroll.dependent_persons.repositories import (
    retrieve_all_dependent_persons_by_employee_id,
)
from payroll.employees.repositories import (
    retrieve_all_employees,
    retrieve_employee_by_id,
)
from payroll.employees.services import check_exist_employee_by_id
from payroll.insurances.repositories import get_insurance_policy_by_id
from payroll.models import PayrollPayrollManagementDetail, PayrollScheduleDetail
from payroll.overtimes.repositories import retrieve_employee_overtime_by_month
from payroll.payroll_management_details.repositories import (
    add_payroll_management_detail,
)
from payroll.payroll_managements.repositories import (
    add_payroll_management,
    remove_payroll_management,
    retrieve_all_payroll_managements,
    retrieve_payroll_management_by_id,
    retrieve_payroll_management_by_information,
)
from payroll.payroll_managements.schemas import (
    PayrollManagementCreate,
    PayrollManagementsCreate,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.schedule_details.repositories import (
    retrieve_schedule_details_by_schedule_id,
)
from payroll.shifts.repositories import retrieve_shift_by_id
from payroll.utils.models import Day, BenefitType


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


def create_payroll_management(
    *, db_session, payroll_management_in: PayrollManagementCreate
):
    value, payroll_management_detail = net_income_handler(
        db_session=db_session,
        employee_id=payroll_management_in.employee_id,
        month=payroll_management_in.month,
        year=payroll_management_in.year,
    )

    employee = retrieve_employee_by_id(
        db_session=db_session, employee_id=payroll_management_in.employee_id
    )

    first_day, last_day = get_month_boundaries(
        month=payroll_management_in.month, year=payroll_management_in.year
    )

    contract_id = retrieve_contract_by_employee_id_and_period(
        db_session=db_session,
        employee_code=employee.code,
        from_date=first_day,
        to_date=last_day,
    ).id

    try:
        payroll_management = add_payroll_management(
            db_session=db_session,
            payroll_management_in=payroll_management_in,
            value=value,
            contract_id=contract_id,
        )

        payroll_management_id = retrieve_payroll_management_by_information(
            db_session=db_session,
            employee_id=employee.id,
            contract_id=contract_id,
            month=payroll_management_in.month,
            year=payroll_management_in.year,
        ).id

        payroll_management_detail.payroll_management_id = payroll_management_id
        add_payroll_management_detail(
            db_session=db_session,
            payroll_management_detail_in=payroll_management_detail,
        )

        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return payroll_management


def create_multi_payroll_managements(
    *,
    db_session,
    payroll_management_list_in: PayrollManagementsCreate,
    # apply_all: bool = False,
):
    payroll_managements = []
    count = 0
    list_id = []

    if payroll_management_list_in.apply_all:
        list_id = [
            employee.id
            for employee in retrieve_all_employees(db_session=db_session)["data"]
        ]

    else:
        list_id = [id for id in payroll_management_list_in.list_emp]
    try:
        for employee_id in list_id:
            if not check_exist_employee_by_id(
                db_session=db_session, employee_id=employee_id
            ):
                raise AppException(ErrorMessages.ResourceNotFound(), "employee")
            try:
                payroll_management_in = PayrollManagementCreate(
                    employee_id=employee_id,
                    month=payroll_management_list_in.month,
                    year=payroll_management_list_in.year,
                )

                payroll_management = create_payroll_management(
                    db_session=db_session, payroll_management_in=payroll_management_in
                )
                payroll_managements.append(payroll_management)
                count += 1

            except Exception as e:
                db_session.rollback()
                raise AppException(ErrorMessages.ErrSM99999(), str(e))
            db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return {"count": count, "data": payroll_managements}


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
    work_hours_standard = 0
    for schedule_detail in schedule_details["data"]:
        shift_work_hours = retrieve_shift_by_id(
            db_session=db_session, shift_id=schedule_detail.shift_id
        ).standard_work_hours

        work_hours_standard = shift_work_hours

    return work_hours_standard


def work_days_standard_handler(*, schedule_details: PayrollScheduleDetail):
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


def work_hours_handler(
    *, db_session, employee_id: int, schedule_id: int, month: int, year: int
):
    attendances = retrieve_employee_attendances_by_month(
        db_session=db_session,
        employee_id=employee_id,
        month=month,
        year=year,
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


def overtime_hours_handler(*, db_session, employee_id: int, month: int, year: int):
    overtimes = retrieve_employee_overtime_by_month(
        db_session=db_session,
        employee_id=employee_id,
        month=month,
        year=year,
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
    return next_month.replace(day=1) - timedelta(days=1)


def get_month_boundaries(month: int, year: int):
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12")

    first_day = datetime(year, month, 1)

    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)

    last_day = next_month - timedelta(days=1)

    return first_day, last_day


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


def benefit_handler(*, db_session, contract_id):
    cbassocs = retrieve_cbassocs_by_contract_id(
        db_session=db_session, contract_id=contract_id
    )["data"]
    benefit_list = {}
    for cbassoc in cbassocs:
        benefit = retrieve_benefit_by_id(
            db_session=db_session, benefit_id=cbassoc.benefit_id
        )
        benefit_list[f"{benefit.type}"] = benefit.value

    return benefit_list


def benefit_salary_handler(
    *,
    benefit_value: float,
    work_days_standard: float,
    work_hours_standard: float,
    work_hours_real: float,
):
    return benefit_value / work_days_standard / work_hours_standard * work_hours_real


def net_income_handler(*, db_session, employee_id: int, month: int, year: int):
    payroll_management_detail = PayrollPayrollManagementDetail()
    employee = retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)
    employee_code = retrieve_employee_by_id(
        db_session=db_session, employee_id=employee_id
    ).code
    schedule_id = employee.schedule_id

    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )

    first_day, last_day = get_month_boundaries(month=month, year=year)

    contract = retrieve_contract_by_employee_id_and_period(
        db_session=db_session,
        employee_code=employee_code,
        from_date=first_day,
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
        year=year,
    )

    basic_salary = contract.salary

    # WORK HOURS SALARY
    work_hours_salary = (
        basic_salary
        / work_days_standard
        / work_hours_standard
        * work_hours["adequate_hours"]
    )

    # OVERTIME HOURS SALARY
    overtime_hours = overtime_hours_handler(
        db_session=db_session, employee_id=employee_id, month=month, year=year
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
    benefit_salary = (
        attendant_benefit
    ) = travel_benefit = phone_benefit = housing_benefit = meal_benefit = 0

    benefits = benefit_handler(db_session=db_session, contract_id=contract.id)
    if f"{BenefitType.ATTENDANT}" in benefits:
        if work_days_standard == work_hours["adequate_hours"] / work_hours_standard:
            attendant_benefit = benefits[f"{BenefitType.ATTENDANT}"]

    if f"{BenefitType.TRAVEL}" in benefits:
        travel_benefit = benefit_salary_handler(
            benefit_value=benefits[f"{BenefitType.TRAVEL}"],
            work_days_standard=work_days_standard,
            work_hours_standard=work_hours_standard,
            work_hours_real=work_hours["adequate_hours"],
        )

    if f"{BenefitType.PHONE}" in benefits:
        phone_benefit = benefit_salary_handler(
            benefit_value=benefits[f"{BenefitType.PHONE}"],
            work_days_standard=work_days_standard,
            work_hours_standard=work_hours_standard,
            work_hours_real=work_hours["adequate_hours"],
        )

    if f"{BenefitType.HOUSING}" in benefits:
        housing_benefit = benefit_salary_handler(
            benefit_value=benefits[f"{BenefitType.HOUSING}"],
            work_days_standard=work_days_standard,
            work_hours_standard=work_hours_standard,
            work_hours_real=work_hours["adequate_hours"],
        )

    if f"{BenefitType.MEAL}" in benefits:
        meal_benefit = benefit_salary_handler(
            benefit_value=benefits[f"{BenefitType.MEAL}"],
            work_days_standard=work_days_standard,
            work_hours_standard=work_hours_standard,
            work_hours_real=work_hours["adequate_hours"],
        )

    benefit_salary = (
        travel_benefit
        + attendant_benefit
        + phone_benefit
        + housing_benefit
        + meal_benefit
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
    if insurance_policy:
        employee_insurance = basic_salary * insurance_policy.employee_percentage / 100
        company_insurance = basic_salary * insurance_policy.company_percentage / 100

    # NO TAX HANDLER
    no_tax_salary = meal_benefit + (  # TIEN AN
        overtime_1_5x_salary
        + overtime_2_0x_salary
        - basic_salary
        / work_days_standard
        / work_hours_standard
        * (overtime_hours["overtime_1_5x"] + overtime_hours["overtime_2_0x"])
    )

    # NPT HANDLER
    dependent_pers = retrieve_all_dependent_persons_by_employee_id(
        db_session=db_session, employee_id=employee_id
    )["count"]

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

    payroll_management_detail.work_days_salary = work_hours_salary
    payroll_management_detail.salary = basic_salary
    payroll_management_detail.work_days = work_days_standard
    payroll_management_detail.overtime_1_5x_hours = overtime_hours["overtime_1_5x"]
    payroll_management_detail.overtime_2_0x_hours = overtime_hours["overtime_2_0x"]
    payroll_management_detail.overtime_1_5x_salary = overtime_1_5x_salary
    payroll_management_detail.overtime_2_0x_salary = overtime_2_0x_salary
    payroll_management_detail.travel_benefit_salary = travel_benefit
    payroll_management_detail.phone_benefit_salary = phone_benefit
    payroll_management_detail.housing_benefit_salary = housing_benefit
    payroll_management_detail.attendant_benefit_salary = attendant_benefit
    payroll_management_detail.meal_benefit_salary = meal_benefit
    payroll_management_detail.gross_income = gross_income
    payroll_management_detail.employee_insurance = employee_insurance
    payroll_management_detail.company_insurance = company_insurance
    payroll_management_detail.no_tax_salary = no_tax_salary
    payroll_management_detail.dependant_people = dependent_pers
    payroll_management_detail.tax_salary = tax_salary
    payroll_management_detail.tax = tax
    payroll_management_detail.total_deduction = total_deduction

    return (net_income, payroll_management_detail)

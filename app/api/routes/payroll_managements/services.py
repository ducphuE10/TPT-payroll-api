import calendar
from datetime import date, timedelta
from typing import List, Optional
from app.api.routes.attendances.repositories import (
    retrieve_attendance_by_id,
    retrieve_employee_attendances_by_month,
)

# from payroll.benefits.repositories import retrieve_benefit_by_id
# from payroll.contract_benefit_assocs.repositories import (
#     retrieve_cbassocs_by_contract_id,
# )

from app.api.routes.contract_histories.services import (
    get_active_contract_history_by_period,
)
from app.api.routes.dependants.repositories import (
    retrieve_all_dependants_by_employee_id,
)
from app.api.routes.employees.repositories import (
    retrieve_all_employees,
    retrieve_employee_by_id,
)
from app.api.routes.employees.services import check_exist_employee_by_id
from app.api.routes.insurances.repositories import get_insurance_policy_by_id
from app.db.models import (
    PayrollPayrollManagement,
    PayrollScheduleDetail,
)
from app.api.routes.overtimes.repositories import retrieve_employee_overtime_by_month

from app.api.routes.payroll_managements.repositories import (
    add_payroll_management,
    remove_payroll_management,
    retrieve_all_payroll_managements,
    retrieve_number_of_payroll,
    retrieve_payroll_management_by_id,
    retrieve_payroll_management_by_information,
    retrieve_total_benefit_salary_by_period,
    retrieve_total_gross_income_by_period,
    retrieve_total_overtime_salary_by_period,
    retrieve_total_tax_by_period,
)
from app.api.routes.payroll_managements.schemas import (
    PayrollManagementCreate,
    PayrollManagementsCreate,
)
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages
from app.api.routes.schedule_details.repositories import (
    retrieve_schedule_details_by_schedule_id,
)
from app.api.routes.schedules.services import check_exist_schedule_by_employee_id
from app.api.routes.shifts.repositories import retrieve_shift_by_id
from app.utils.models import Day


def check_exist_payroll_management_by_id(*, db_session, payroll_management_id: int):
    """Check if payroll_management exists in the database."""
    return bool(
        retrieve_payroll_management_by_id(
            db_session=db_session, payroll_management_id=payroll_management_id
        )
    )


def check_exist_payroll_management_by_information(
    *, db_session, employee_id: int, contract_history_id: int, month: int, year: int
):
    """Check if payroll_management exists in the database."""
    return bool(
        retrieve_payroll_management_by_information(
            db_session=db_session,
            employee_id=employee_id,
            contract_history_id=contract_history_id,
            month=month,
            year=year,
        )
    )


def check_available_employee_create_payroll(
    *, db_session, employee_id: int, month: int, year: int
):
    employee = retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)

    if not employee.schedule_id:
        return False
    first_day, last_day = get_month_boundaries(month=month, year=year)

    # contract = retrieve_contract_by_employee_and_period(
    #     db_session=db_session,
    #     employee_code=employee_code,
    #     from_date=first_day,
    #     to_date=last_day,
    # )
    # if not contract:
    #     return False

    return True


def get_number_payroll_documents(*, db_session, month: int, year: int, company_id: int):
    return round(
        retrieve_number_of_payroll(
            db_session=db_session, month=month, year=year, company_id=company_id
        )
    )


def get_total_payroll_gross_income(
    *, db_session, month: int, year: int, company_id: int
):
    return round(
        retrieve_total_gross_income_by_period(
            db_session=db_session, month=month, year=year, company_id=company_id
        ),
        -3,
    )


def get_total_payroll_tax(*, db_session, month: int, year: int, company_id: int):
    return round(
        retrieve_total_tax_by_period(
            db_session=db_session, month=month, year=year, company_id=company_id
        ),
        -3,
    )


def get_total_payroll_overtime_salary(
    *, db_session, month: int, year: int, company_id: int
):
    return round(
        retrieve_total_overtime_salary_by_period(
            db_session=db_session, month=month, year=year, company_id=company_id
        ),
        -3,
    )


def get_total_benefit_salary(*, db_session, month: int, year: int, company_id: int):
    return round(
        retrieve_total_benefit_salary_by_period(
            db_session=db_session, month=month, year=year, company_id=company_id
        ),
        -3,
    )


def metrics_handler(*, db_session, month: int, year: int, company_id: int):
    if (
        get_number_payroll_documents(
            db_session=db_session, month=month, year=year, company_id=company_id
        )
        != 0
    ):
        return {
            "total_payroll_documents": get_number_payroll_documents(
                db_session=db_session, month=month, year=year, company_id=company_id
            ),
            "total_gross_income": get_total_payroll_gross_income(
                db_session=db_session, month=month, year=year, company_id=company_id
            ),
            "total_tax": get_total_payroll_tax(
                db_session=db_session, month=month, year=year, company_id=company_id
            ),
            "total_overtime_salary": get_total_payroll_overtime_salary(
                db_session=db_session, month=month, year=year, company_id=company_id
            ),
            "total_benefit_salary": get_total_benefit_salary(
                db_session=db_session, month=month, year=year, company_id=company_id
            ),
        }
    else:
        return
        {
            "total_payroll_documents": 0,
            "total_gross_income": 0,
            "total_tax": 0,
            "total_overtime_salary": 0,
            "total_benefit_salary": 0,
        }


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
def get_all_payroll_management(
    *, db_session, company_id: int, month: int = None, year: int = None
):
    """Returns all payroll_managements."""
    payroll_managements = retrieve_all_payroll_managements(
        db_session=db_session, month=month, year=year, company_id=company_id
    )
    if not payroll_managements["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "payroll")

    return payroll_managements


def create_payroll_management(
    *,
    db_session,
    payroll_management_in: PayrollManagementCreate,
):
    payroll_management_create = payroll_handler(
        db_session=db_session,
        employee_id=payroll_management_in.employee_id,
        month=payroll_management_in.month,
        year=payroll_management_in.year,
        work_days_standard=payroll_management_in.work_days_standard,
        apply_insurance=payroll_management_in.apply_insurance,
        insurance_id=payroll_management_in.insurance_id,
        company_id=payroll_management_in.company_id,
    )
    if not payroll_management_create:
        return
    try:
        payroll_management = add_payroll_management(
            db_session=db_session,
            payroll_management_in=payroll_management_create,
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
):
    payroll_managements = []
    count = 0
    list_id = []

    if payroll_management_list_in.apply_all:
        for employee in retrieve_all_employees(
            db_session=db_session, company_id=payroll_management_list_in.company_id
        )["data"]:
            if check_exist_schedule_by_employee_id(
                db_session=db_session, employee_id=employee.id
            ):
                list_id.append(employee.id)
    else:
        list_id = [id for id in payroll_management_list_in.list_emp]

    try:
        for employee_id in list_id:
            if not check_exist_employee_by_id(
                db_session=db_session, employee_id=employee_id
            ):
                raise AppException(ErrorMessages.ResourceNotFound(), "employee")
            try:
                if check_available_employee_create_payroll(
                    db_session=db_session,
                    employee_id=employee_id,
                    month=payroll_management_list_in.month,
                    year=payroll_management_list_in.year,
                ):
                    payroll_management_in = PayrollManagementCreate(
                        employee_id=employee_id,
                        month=payroll_management_list_in.month,
                        year=payroll_management_list_in.year,
                        work_days_standard=payroll_management_list_in.work_days_standard,
                        apply_insurance=payroll_management_list_in.apply_insurance,
                        insurance_id=payroll_management_list_in.insurance_id,
                        company_id=payroll_management_list_in.company_id,
                    )

                    payroll_management = create_payroll_management(
                        db_session=db_session,
                        payroll_management_in=payroll_management_in,
                    )
                    if not payroll_management:
                        continue
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


def delete_payroll_managements(*, db_session, list_id: List):
    """Deletes a payroll_management based on the given id."""
    for payroll_management_id in list_id:
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


def work_days_actual_handler(
    *, schedule_details: PayrollScheduleDetail, month: int, year: int
):
    work_days_list = {
        schedule_detail.day for schedule_detail in schedule_details["data"]
    }
    weekday_map = {
        0: Day.Mon,
        1: Day.Tue,
        2: Day.Wed,
        3: Day.Thu,
        4: Day.Fri,
        5: Day.Sat,
        6: Day.Sun,
    }

    month_days = calendar.monthrange(year, month)[1]

    total_actual_work_days = sum(
        1
        for day in range(1, month_days + 1)
        if weekday_map[date(year, month, day).weekday()] in work_days_list
    )

    return total_actual_work_days


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

    first_day = date(year, month, 1)

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

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

    return tax


# def benefit_handler(*, db_session, contract_id):
#     cbassocs = retrieve_cbassocs_by_contract_id(
#         db_session=db_session, contract_id=contract_id
#     )["data"]
#     benefit_list = {}
#     for cbassoc in cbassocs:
#         benefit = retrieve_benefit_by_id(
#             db_session=db_session, benefit_id=cbassoc.benefit_id
#         )
#         benefit_list[f"{benefit.type}"] = benefit.value

#     return benefit_list


def benefit_salary_handler(
    *,
    benefit_value: float,
    work_days_standard: float,
    work_hours_standard: float,
    work_hours_real: float,
):
    return benefit_value / work_days_standard / work_hours_standard * work_hours_real


def dependant_period_deduction_handler(
    *, month: int, year: int, deduction_from: date, deduction_to: date
):
    first_day, last_day = get_month_boundaries(month=month, year=year)
    if deduction_to >= last_day:
        return True
    return False


def payroll_handler(
    *,
    db_session,
    employee_id: int,
    month: int,
    year: int,
    work_days_standard: float,
    apply_insurance: bool = False,
    insurance_id: Optional[int] = None,
    company_id: int,
):
    employee = retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)

    schedule_id = employee.schedule_id

    schedule_details = retrieve_schedule_details_by_schedule_id(
        db_session=db_session, schedule_id=schedule_id
    )

    first_day, last_day = get_month_boundaries(month=month, year=year)

    try:
        contract_history = get_active_contract_history_by_period(
            db_session=db_session,
            employee_id=employee_id,
            from_date=first_day,
            to_date=last_day,
        )
    except Exception:
        return

    if check_exist_payroll_management_by_information(
        db_session=db_session,
        employee_id=employee_id,
        contract_history_id=contract_history.id,
        month=month,
        year=year,
    ):
        # raise AppException(ErrorMessages.ResourceAlreadyExists(), "payroll management")
        return

    # work_days_standard = work_days_standard_handler(schedule_details=schedule_details)

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
    basic_salary = contract_history.salary

    # WORK HOURS SALARY
    work_days_salary = (
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
        attendant_benefit_salary
    ) = (
        transportation_benefit_salary
    ) = (
        phone_benefit_salary
    ) = housing_benefit_salary = meal_benefit_salary = toxic_benefit_salary = 0

    if (
        work_days_actual_handler(
            schedule_details=schedule_details, month=month, year=year
        )
        == work_hours["adequate_hours"] / work_hours_standard
    ):
        attendant_benefit_salary = contract_history.attendant_benefit

    transportation_benefit_salary = benefit_salary_handler(
        benefit_value=contract_history.transportation_benefit,
        work_days_standard=work_days_standard,
        work_hours_standard=work_hours_standard,
        work_hours_real=work_hours["adequate_hours"],
    )

    phone_benefit_salary = benefit_salary_handler(
        benefit_value=contract_history.phone_benefit,
        work_days_standard=work_days_standard,
        work_hours_standard=work_hours_standard,
        work_hours_real=work_hours["adequate_hours"],
    )

    housing_benefit_salary = benefit_salary_handler(
        benefit_value=contract_history.housing_benefit,
        work_days_standard=work_days_standard,
        work_hours_standard=work_hours_standard,
        work_hours_real=work_hours["adequate_hours"],
    )

    toxic_benefit_salary = benefit_salary_handler(
        benefit_value=contract_history.toxic_benefit,
        work_days_standard=work_days_standard,
        work_hours_standard=work_hours_standard,
        work_hours_real=work_hours["adequate_hours"],
    )

    meal_benefit_salary = benefit_salary_handler(
        benefit_value=contract_history.meal_benefit,
        work_days_standard=work_days_standard,
        work_hours_standard=work_hours_standard,
        work_hours_real=work_hours["adequate_hours"] + overtime_hours["overtime_2_0x"],
    )

    benefit_salary = (
        transportation_benefit_salary
        + attendant_benefit_salary
        + phone_benefit_salary
        + housing_benefit_salary
        + toxic_benefit_salary
        + meal_benefit_salary
    )

    gross_income = (
        work_days_salary + overtime_1_5x_salary + overtime_2_0x_salary + benefit_salary
    )

    # DEDUCTION HANDLER

    # INSURANCE HANDLER
    employee_insurance = company_insurance = 0
    if apply_insurance:
        insurance = get_insurance_policy_by_id(db_session=db_session, id=insurance_id)
        if not insurance:
            raise AppException(ErrorMessages.ResourceNotFound, "insurance")
        employee_insurance = basic_salary * insurance.employee_percentage / 100
        company_insurance = basic_salary * insurance.company_percentage / 100

    # NO TAX HANDLER
    no_tax_salary = meal_benefit_salary + (
        overtime_1_5x_salary
        + overtime_2_0x_salary
        - basic_salary
        / work_days_standard
        / work_hours_standard
        * (overtime_hours["overtime_1_5x"] + overtime_hours["overtime_2_0x"])
    )

    # Handle dependant deduction
    dependants_list = retrieve_all_dependants_by_employee_id(
        db_session=db_session, employee_id=employee_id
    )
    dependant_deduction_count = 0
    for dependant in dependants_list["data"]:
        if dependant_period_deduction_handler(
            month=month,
            year=year,
            deduction_from=dependant.deduction_from,
            deduction_to=dependant.deduction_to,
        ):
            dependant_deduction_count += 1

    # TAX SALARY HANDLER
    tax_salary = max(
        gross_income
        - employee_insurance
        - no_tax_salary
        - 11000000
        - 4400000 * dependant_deduction_count,
        0,
    )
    # TAX HANDLER
    tax = tax_handler(income=tax_salary)

    total_deduction = employee_insurance + tax

    net_income = round(gross_income - total_deduction, -3)

    payroll_management_data = {
        "employee_id": employee_id,
        "company_id": company_id,
        "contract_history_id": contract_history.id,
        "insurance_policy_id": insurance_id,
        "net_income": net_income,
        "month": month,
        "year": year,
        "salary": basic_salary,
        "work_days_standard": work_days_standard,
        "work_days": round(work_hours["adequate_hours"] / 8, 1),
        "work_days_salary": work_days_salary,
        "overtime_1_5x_hours": overtime_hours["overtime_1_5x"],
        "overtime_1_5x_salary": overtime_1_5x_salary,
        "overtime_2_0x_hours": overtime_hours["overtime_2_0x"],
        "overtime_2_0x_salary": overtime_2_0x_salary,
        "transportation_benefit_salary": transportation_benefit_salary,
        "attendant_benefit_salary": attendant_benefit_salary,
        "housing_benefit_salary": housing_benefit_salary,
        "phone_benefit_salary": phone_benefit_salary,
        "meal_benefit_salary": meal_benefit_salary,
        "toxic_benefit_salary": toxic_benefit_salary,
        "gross_income": gross_income,
        "employee_insurance": employee_insurance,
        "company_insurance": company_insurance,
        "no_tax_salary": no_tax_salary,
        "dependant_people": dependant_deduction_count,
        "tax_salary": tax_salary,
        "tax": tax,
        "total_deduction": total_deduction,
    }

    # Create the PayrollPayrollManagement object
    payroll_management = PayrollPayrollManagement(**payroll_management_data)
    return payroll_management

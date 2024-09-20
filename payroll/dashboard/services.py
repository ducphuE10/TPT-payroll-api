from payroll.payroll_managements.repositories import (
    retrieve_total_benefit_salary_by_period,
    retrieve_total_gross_income_by_period,
    retrieve_total_overtime_salary_by_period,
    retrieve_total_tax_by_period,
)
from payroll.payroll_managements.repositories import retrieve_number_of_payroll


def get_number_payroll_documents(*, db_session, month: int, year: int):
    return round(
        retrieve_number_of_payroll(db_session=db_session, month=month, year=year), -3
    )


def get_total_payroll_gross_income(*, db_session, month: int, year: int):
    return round(
        retrieve_total_gross_income_by_period(
            db_session=db_session, month=month, year=year
        ),
        -3,
    )


def get_total_payroll_tax(*, db_session, month: int, year: int):
    return round(
        retrieve_total_tax_by_period(db_session=db_session, month=month, year=year), -3
    )


def get_total_payroll_overtime_salary(*, db_session, month: int, year: int):
    return round(
        retrieve_total_overtime_salary_by_period(
            db_session=db_session, month=month, year=year
        ),
        -3,
    )


def get_total_benefit_salary(*, db_session, month: int, year: int):
    return round(
        retrieve_total_benefit_salary_by_period(
            db_session=db_session, month=month, year=year
        ),
        -3,
    )


def dashboard_handler(*, db_session, month: int, year: int):
    return {
        "total_payroll_documents": get_number_payroll_documents(
            db_session=db_session, month=month, year=year
        ),
        "total_gross_income": get_total_payroll_gross_income(
            db_session=db_session, month=month, year=year
        ),
        "total_tax": get_total_payroll_tax(
            db_session=db_session, month=month, year=year
        ),
        "total_overtime_salary": get_total_payroll_overtime_salary(
            db_session=db_session, month=month, year=year
        ),
        "total_benefit_salary": get_total_benefit_salary(
            db_session=db_session, month=month, year=year
        ),
    }

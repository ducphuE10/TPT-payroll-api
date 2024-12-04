import logging

from sqlalchemy import func

from payroll.models import PayrollPayrollManagement

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /payroll_managements/{payroll_management_id}
def retrieve_payroll_management_by_id(
    *, db_session, payroll_management_id: int
) -> PayrollPayrollManagement:
    """Returns a payroll_management based on the given id."""
    return (
        db_session.query(PayrollPayrollManagement)
        .order_by(PayrollPayrollManagement.id.asc())
        .filter(
            PayrollPayrollManagement.id == payroll_management_id,
        )
        .first()
    )


def retrieve_number_of_payroll(*, db_session, month: int, year: int) -> int:
    return (
        db_session.query(PayrollPayrollManagement)
        .filter(
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
        .count()
    )


def retrieve_payroll_management_by_information(
    *, db_session, employee_id: int, contract_history_id: int, month: int, year: int
) -> PayrollPayrollManagement:
    """Returns a payroll_management based on the given id."""
    return (
        db_session.query(PayrollPayrollManagement)
        .filter(
            PayrollPayrollManagement.employee_id == employee_id,
            PayrollPayrollManagement.contract_history_id == contract_history_id,
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
        .first()
    )


# GET /payroll_managements
def retrieve_all_payroll_managements(
    *, db_session, month: int = None, year: int = None
) -> PayrollPayrollManagement:
    """Returns all payroll_managements."""
    query = db_session.query(PayrollPayrollManagement).order_by(
        PayrollPayrollManagement.id.asc()
    )
    if month and year:
        query = query.filter(
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
    count = query.count()
    payroll_managements = query.all()

    return {"count": count, "data": payroll_managements}


def retrieve_total_gross_income_by_period(
    *, db_session, month: int, year: int
) -> float:
    return (
        db_session.query(func.sum(PayrollPayrollManagement.gross_income))
        .filter(
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
        .scalar()
    )


def retrieve_total_tax_by_period(*, db_session, month: int, year: int) -> float:
    return (
        db_session.query(func.sum(PayrollPayrollManagement.tax))
        .filter(
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
        .scalar()
    )


def retrieve_total_overtime_salary_by_period(
    *, db_session, month: int, year: int
) -> float:
    return (
        db_session.query(
            func.sum(PayrollPayrollManagement.overtime_1_5x_salary)
            + func.sum(PayrollPayrollManagement.overtime_2_0x_salary)
        )
        .filter(
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
        .scalar()
    )


def retrieve_total_benefit_salary_by_period(
    *, db_session, month: int, year: int
) -> float:
    return (
        db_session.query(
            func.sum(PayrollPayrollManagement.meal_benefit_salary)
            + func.sum(PayrollPayrollManagement.attendant_benefit_salary)
            + func.sum(PayrollPayrollManagement.transportation_benefit_salary)
            + func.sum(PayrollPayrollManagement.housing_benefit_salary)
            + func.sum(PayrollPayrollManagement.phone_benefit_salary)
        )
        .filter(
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
        .scalar()
    )


# POST /payroll_managements
def add_payroll_management(
    *,
    db_session,
    payroll_management_in: PayrollPayrollManagement,
) -> PayrollPayrollManagement:
    """Creates a new payroll_management."""
    payroll_management_in.created_by = "admin"
    db_session.add(payroll_management_in)

    return payroll_management_in


# DELETE /payroll_managements/{payroll_management_id}
def remove_payroll_management(*, db_session, payroll_management_id: int):
    """Deletes a payroll_management based on the given id."""
    query = db_session.query(PayrollPayrollManagement).filter(
        PayrollPayrollManagement.id == payroll_management_id
    )
    deleted_payroll_management = query.first()
    query.delete()

    return deleted_payroll_management

import logging

from payroll.payroll_managements.schemas import (
    PayrollManagementCreate,
)
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
        .filter(
            PayrollPayrollManagement.id == payroll_management_id,
        )
        .first()
    )


# def retrieve_payroll_management_by_information(
#     *, db_session, employee_id: int, month: int, year: int
# ) -> PayrollPayrollManagement:
#     """Returns a payroll_management based on the given id."""
#     return (
#         db_session.query(PayrollPayrollManagement)
#         .filter(
#             PayrollPayrollManagement.employee_id == employee_id,
#             PayrollPayrollManagement.month == month,
#             PayrollPayrollManagement.year == year,
#         )
#         .first()
#     )


def retrieve_payroll_management_by_information(
    *, db_session, employee_id: int, contract_id: int, month: int, year: int
) -> PayrollPayrollManagement:
    """Returns a payroll_management based on the given id."""
    return (
        db_session.query(PayrollPayrollManagement)
        .filter(
            PayrollPayrollManagement.employee_id == employee_id,
            PayrollPayrollManagement.contract_id == contract_id,
            PayrollPayrollManagement.month == month,
            PayrollPayrollManagement.year == year,
        )
        .first()
    )


# GET /payroll_managements
def retrieve_all_payroll_managements(*, db_session) -> PayrollPayrollManagement:
    """Returns all payroll_managements."""
    query = db_session.query(PayrollPayrollManagement)
    count = query.count()
    payroll_managements = query.all()

    return {"count": count, "data": payroll_managements}


# POST /payroll_managements
def add_payroll_management(
    *,
    db_session,
    payroll_management_in: PayrollManagementCreate,
    value: float,
    contract_id: int,
) -> PayrollPayrollManagement:
    """Creates a new payroll_management."""
    payroll_management = PayrollPayrollManagement(**payroll_management_in.model_dump())
    payroll_management.created_by = "admin"
    payroll_management.value = value
    payroll_management.contract_id = contract_id
    db_session.add(payroll_management)
    return payroll_management


# DELETE /payroll_managements/{payroll_management_id}
def remove_payroll_management(*, db_session, payroll_management_id: int):
    """Deletes a payroll_management based on the given id."""
    query = db_session.query(PayrollPayrollManagement).filter(
        PayrollPayrollManagement.id == payroll_management_id
    )
    deleted_payroll_management = query.first()
    query.delete()

    return deleted_payroll_management

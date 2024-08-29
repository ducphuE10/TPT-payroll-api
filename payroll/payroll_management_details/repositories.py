import logging

from payroll.models import PayrollPayrollManagementDetail

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /payroll_management_details/{payroll_management_detail_id}
def retrieve_payroll_management_detail_by_id(
    *, db_session, payroll_management_detail_id: int
) -> PayrollPayrollManagementDetail:
    """Returns a payroll_management_detail based on the given id."""
    return (
        db_session.query(PayrollPayrollManagementDetail)
        .filter(
            PayrollPayrollManagementDetail.id == payroll_management_detail_id,
        )
        .first()
    )


# GET /payroll_management_details
def retrieve_all_payroll_management_details(
    *, db_session
) -> PayrollPayrollManagementDetail:
    """Returns all payroll_management_details."""
    query = db_session.query(PayrollPayrollManagementDetail)
    count = query.count()
    payroll_management_details = query.all()

    return {"count": count, "data": payroll_management_details}


# POST /payroll_management_details
def add_payroll_management_detail(
    *, db_session, payroll_management_detail_in: PayrollPayrollManagementDetail
) -> PayrollPayrollManagementDetail:
    """Creates a new payroll_management_detail."""
    # payroll_management_detail = PayrollPayrollManagementDetail(
    #     **payroll_management_detail_in.model_dump()
    # )
    payroll_management_detail_in.created_by = "admin"
    db_session.add(payroll_management_detail_in)

    return payroll_management_detail_in


# DELETE /payroll_management_details/{payroll_management_detail_id}
def remove_payroll_management_detail(*, db_session, payroll_management_detail_id: int):
    """Deletes a payroll_management_detail based on the given id."""
    query = db_session.query(PayrollPayrollManagementDetail).filter(
        PayrollPayrollManagementDetail.id == payroll_management_detail_id
    )
    deleted_payroll_management_detail = query.first()
    query.delete()

    return deleted_payroll_management_detail

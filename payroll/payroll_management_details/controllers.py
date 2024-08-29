from fastapi import APIRouter

from payroll.payroll_management_details.schemas import (
    PayrollManagementDetailRead,
    PayrollManagementDetailsRead,
)
from payroll.database.core import DbSession
from payroll.payroll_management_details.services import (
    delete_payroll_management_detail,
    get_all_payroll_management_details,
    get_payroll_management_detail_by_id,
)

payroll_management_detail_router = APIRouter()


# GET /payroll_management_details
@payroll_management_detail_router.get("", response_model=PayrollManagementDetailsRead)
def retrieve_payroll_management_details(
    *,
    db_session: DbSession,
):
    """Retrieve all payroll_management_details."""
    return get_all_payroll_management_details(db_session=db_session)


# GET /payroll_management_details/{payroll_management_detail_id}
@payroll_management_detail_router.get(
    "/{payroll_management_detail_id}", response_model=PayrollManagementDetailRead
)
def retrieve_payroll_management_detail(
    *, db_session: DbSession, payroll_management_detail_id: int
):
    """Retrieve a payroll_management_detail by id."""
    return get_payroll_management_detail_by_id(
        db_session=db_session, payroll_management_detail_id=payroll_management_detail_id
    )


# DELETE /payroll_management_details/{payroll_management_detail_id}
@payroll_management_detail_router.delete(
    "/{payroll_management_detail_id}", response_model=PayrollManagementDetailRead
)
def delete(*, db_session: DbSession, payroll_management_detail_id: int):
    """Delete a payroll_management_detail by id."""
    return delete_payroll_management_detail(
        db_session=db_session, payroll_management_detail_id=payroll_management_detail_id
    )

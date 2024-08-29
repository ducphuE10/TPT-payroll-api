from fastapi import APIRouter

from payroll.payroll_managements.schemas import (
    PayrollManagementRead,
    PayrollManagementCreate,
    PayrollManagementsCreate,
    PayrollManagementsRead,
)
from payroll.database.core import DbSession
from payroll.payroll_managements.services import (
    create_multi_payroll_managements,
    create_payroll_management,
    delete_payroll_management,
    get_all_payroll_management,
    get_payroll_management_by_id,
)

payroll_management_router = APIRouter()


# GET /payroll_managements
@payroll_management_router.get("", response_model=PayrollManagementsRead)
def retrieve_payroll_managements(
    *,
    db_session: DbSession,
):
    """Retrieve all payroll_managements."""
    return get_all_payroll_management(db_session=db_session)


# GET /payroll_managements/{payroll_management_id}
@payroll_management_router.get(
    "/{payroll_management_id}", response_model=PayrollManagementRead
)
def retrieve_payroll_management(*, db_session: DbSession, payroll_management_id: int):
    """Retrieve a payroll_management by id."""
    return get_payroll_management_by_id(
        db_session=db_session, payroll_management_id=payroll_management_id
    )


@payroll_management_router.post("", response_model=PayrollManagementRead)
def create(*, payroll_management_in: PayrollManagementCreate, db_session: DbSession):
    return create_payroll_management(
        db_session=db_session, payroll_management_in=payroll_management_in
    )


@payroll_management_router.post("/bulk", response_model=PayrollManagementsRead)
def create_multi(
    *, db_session: DbSession, payroll_management_list_in: PayrollManagementsCreate
):
    """Creates a new attendance."""
    return create_multi_payroll_managements(
        db_session=db_session,
        payroll_management_list_in=payroll_management_list_in,
        # apply_all=payroll_management_list_in.apply_all,
    )


# DELETE /payroll_managements/{payroll_management_id}
@payroll_management_router.delete(
    "/{payroll_management_id}", response_model=PayrollManagementRead
)
def delete(*, db_session: DbSession, payroll_management_id: int):
    """Delete a payroll_management by id."""
    return delete_payroll_management(
        db_session=db_session, payroll_management_id=payroll_management_id
    )

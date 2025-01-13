from typing import List
from fastapi import APIRouter, Query

from app.api.routes.payroll_managements.schemas import (
    PayrollManagementBase,
    PayrollManagementRead,
    PayrollManagementCreate,
    PayrollManagementsCreate,
    PayrollManagementsRead,
)
from app.db.core import DbSession
from app.api.routes.payroll_managements.services import (
    create_multi_payroll_managements,
    create_payroll_management,
    delete_payroll_management,
    delete_payroll_managements,
    get_all_payroll_management,
    get_payroll_management_by_id,
    metrics_handler,
)

payroll_management_router = APIRouter()


# GET /payroll_managements
@payroll_management_router.get("", response_model=PayrollManagementsRead)
def retrieve_payroll_managements(
    *, db_session: DbSession, company_id: int, month: int = None, year: int = None
):
    """Retrieve all payroll_managements."""
    return get_all_payroll_management(
        db_session=db_session, month=month, year=year, company_id=company_id
    )


@payroll_management_router.get("/metrics")
def metrics(*, db_session: DbSession, month: int, year: int, company_id: int):
    return metrics_handler(
        db_session=db_session, month=month, year=year, company_id=company_id
    )


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
def create(
    *,
    db_session: DbSession,
    payroll_management_in: PayrollManagementCreate,
):
    return create_payroll_management(
        db_session=db_session,
        payroll_management_in=payroll_management_in,
    )


@payroll_management_router.post("/bulk", response_model=PayrollManagementsRead)
def create_multi(
    *,
    db_session: DbSession,
    payroll_management_list_in: PayrollManagementsCreate,
):
    """Creates a new attendance."""
    return create_multi_payroll_managements(
        db_session=db_session,
        payroll_management_list_in=payroll_management_list_in,
    )


@payroll_management_router.delete("/bulk/")
def delete_contracts(
    *,
    db_session: DbSession,
    list_id: List[int] = Query(),
):
    return delete_payroll_managements(db_session=db_session, list_id=list_id)


# DELETE /payroll_managements/{payroll_management_id}
@payroll_management_router.delete(
    "/{payroll_management_id}", response_model=PayrollManagementBase
)
def delete(*, db_session: DbSession, payroll_management_id: int):
    """Delete a payroll_management by id."""
    return delete_payroll_management(
        db_session=db_session, payroll_management_id=payroll_management_id
    )

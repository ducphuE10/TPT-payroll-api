from fastapi import APIRouter

from app.db.core import DbSession
from app.api.routes.insurances import services as insurance_services
from app.api.routes.insurances.schemas import (
    InsurancePolicyUpdate,
    InsurancePolicyCreate,
    InsurancePolicyRead,
    InsurancePoliciesRead,
)


insurance_router = APIRouter()


@insurance_router.get("", response_model=InsurancePoliciesRead)
def all(
    *,
    db_session: DbSession,
    company_id: int,
):
    return insurance_services.get_all(db_session=db_session, company_id=company_id)


@insurance_router.get("/{id}", response_model=InsurancePolicyRead)
def retrieve(*, db_session: DbSession, id: int):
    return insurance_services.get_one_by_id(db_session=db_session, id=id)


@insurance_router.post("")
def create(*, db_session: DbSession, insurance_policy_in: InsurancePolicyCreate):
    return insurance_services.create(
        db_session=db_session, insurance_policy_in=insurance_policy_in
    )


@insurance_router.put("/{id}")
def update(
    *, db_session: DbSession, id: int, insurance_policy_in: InsurancePolicyUpdate
):
    return insurance_services.update(
        db_session=db_session, id=id, insurance_policy_in=insurance_policy_in
    )


@insurance_router.delete("/{id}")
def delete(*, db_session: DbSession, id: int):
    return insurance_services.delete(db_session=db_session, id=id)

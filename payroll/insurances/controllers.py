from fastapi import APIRouter

from payroll.database.core import DbSession
from payroll.insurances import services as insurance_services
from payroll.insurances.schemas import (
    InsurancePolicyUpdate,
    InsurancePolicyCreate,
    InsurancePolicyRead,
    InsurancePoliciesRead,
)


router = APIRouter()


@router.get("", response_model=InsurancePoliciesRead)
def all(
    *,
    db_session: DbSession,
):
    return insurance_services.get_all(db_session=db_session)


@router.get("/{id}", response_model=InsurancePolicyRead)
def retrieve(*, db_session: DbSession, id: int):
    return insurance_services.get_one_by_id(db_session=db_session, id=id)


@router.post("")
def create(*, db_session: DbSession, insurance_policy_in: InsurancePolicyCreate):
    return insurance_services.create(
        db_session=db_session, insurance_policy_in=insurance_policy_in
    )


@router.put("/{id}")
def update(
    *, db_session: DbSession, id: int, insurance_policy_in: InsurancePolicyUpdate
):
    return insurance_services.update(
        db_session=db_session, id=id, insurance_policy_in=insurance_policy_in
    )


@router.delete("/{id}")
def delete(*, db_session: DbSession, id: int):
    return insurance_services.delete(db_session=db_session, id=id)

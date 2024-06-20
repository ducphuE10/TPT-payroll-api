from fastapi import APIRouter

from payroll.database.core import DbSession
from payroll.taxes import services as tax_services
from payroll.taxes.schemas import (
    TaxPolicyUpdate,
    TaxPolicyCreate,
    TaxPolicyRead,
    TaxpoliciesRead,
)


router = APIRouter()


@router.get("", response_model=TaxpoliciesRead)
def all(
    *,
    db_session: DbSession,
):
    return tax_services.get_all(db_session=db_session)


@router.get("/{id}", response_model=TaxPolicyRead)
def retrieve(*, db_session: DbSession, id: int):
    return tax_services.get_one_by_id(db_session=db_session, id=id)


@router.post("")
def create(*, db_session: DbSession, tax_policy_in: TaxPolicyCreate):
    return tax_services.create(db_session=db_session, tax_policy_in=tax_policy_in)


@router.put("/{id}")
def update(*, db_session: DbSession, id: int, tax_policy_in: TaxPolicyUpdate):
    return tax_services.update(
        db_session=db_session, id=id, tax_policy_in=tax_policy_in
    )


@router.delete("/{id}")
def delete(*, db_session: DbSession, id: int):
    return tax_services.delete(db_session=db_session, id=id)

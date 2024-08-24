from typing import List
from fastapi import APIRouter

from payroll.contract_benefit_assocs.schemas import CBAssocsCreate, CBAssocsRead
from payroll.database.core import DbSession
from payroll.contracts import services as contract_services
from payroll.contracts.schemas import (
    ContractRead,
    ContractCreate,
    ContractUpdate,
    ContractsRead,
)


contract_router = APIRouter()


@contract_router.get("", response_model=ContractsRead)
def all(
    *,
    db_session: DbSession,
):
    return contract_services.get_all(db_session=db_session)


@contract_router.get("/{id}", response_model=ContractRead)
def retrieve(*, db_session: DbSession, id: int):
    return contract_services.get_one_by_id(db_session=db_session, id=id)


@contract_router.post("")
def create(*, db_session: DbSession, contract_in: ContractCreate):
    return contract_services.create(db_session=db_session, contract_in=contract_in)


# POST /schedules
@contract_router.post("/both", response_model=CBAssocsRead)
def create_with_benefits(
    *,
    db_session: DbSession,
    contract_in: ContractCreate,
    benefit_list_in: List[CBAssocsCreate],
):
    """Creates a new schedule."""
    return create_with_benefits(
        db_session=db_session,
        contract_in=contract_in,
        benefit_list_in=benefit_list_in,
    )


@contract_router.put("/{id}")
def update(*, db_session: DbSession, id: int, contract_in: ContractUpdate):
    return contract_services.update(
        db_session=db_session, id=id, contract_in=contract_in
    )


@contract_router.delete("/{id}")
def delete(*, db_session: DbSession, id: int):
    return contract_services.delete(db_session=db_session, id=id)

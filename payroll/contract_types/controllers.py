from fastapi import APIRouter

from payroll.contract_types.schemas import (
    ContractTypeRead,
    ContractTypeCreate,
    ContractTypesRead,
)
from payroll.database.core import DbSession
from payroll.contract_types.repositories import (
    get_all,
    get_one_by_id,
    create,
    delete,
)

contracttype_router = APIRouter()


@contracttype_router.get("", response_model=ContractTypesRead)
def retrieve_contracttypes(
    *,
    db_session: DbSession,
):
    return get_all(db_session=db_session)


@contracttype_router.get("/{id}", response_model=ContractTypeRead)
def retrieve_contracttype(*, db_session: DbSession, id: int):
    return get_one_by_id(db_session=db_session, id=id)


@contracttype_router.post("", response_model=ContractTypeRead)
def create_contracttype(*, contracttype_in: ContractTypeCreate, db_session: DbSession):
    contracttype_in.created_by = "admin"
    contracttype = create(db_session=db_session, contracttype_in=contracttype_in)
    return contracttype


@contracttype_router.delete("/{id}", response_model=ContractTypeRead)
def delete_contracttype(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)

from fastapi import APIRouter

from payroll.contracttype.models import (
    ContractTypeRead,
    ContractTypeCreate,
    ContractTypesRead,
)
from payroll.database.core import DbSession
from payroll.contracttype.service import get_by_id, delete, get, create

contracttype_router = APIRouter()
ContractTypeRead


@contracttype_router.get("", response_model=ContractTypesRead)
def retrieve_contracttypes(
    *,
    db_session: DbSession,
):
    return get(db_session=db_session)


@contracttype_router.get("/{id}", response_model=ContractTypeRead)
def retrieve_contracttype(*, db_session: DbSession, id: int):
    return get_by_id(db_session=db_session, id=id)


@contracttype_router.post("", response_model=ContractTypeRead)
def create_contracttype(*, contracttype_in: ContractTypeCreate, db_session: DbSession):
    """Creates a new contracttpye."""
    contracttype_in.created_by = "admin"
    contracttype = create(db_session=db_session, contracttype_in=contracttype_in)
    return contracttype


# @contracttype_router.put("/{id}", response_model=ContractTypeRead)
# def update_contracttype(*, db_session: DbSession, id: int, contracttype_in: ContractTypeCreate):
#     return update(db_session=db_session, id=id, contracttype_in=contracttype_in)


@contracttype_router.delete("/{id}", response_model=ContractTypeRead)
def delete_contracttype(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)

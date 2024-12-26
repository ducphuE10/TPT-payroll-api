from typing import List, Optional
from fastapi import APIRouter, Query

from app.db.core import DbSession
from app.api.routes.contract_histories.services import (
    create_contract_history,
    delete_contract_history,
    generate_all_contracts_docx,
    generate_contract_docx,
    generate_multi_contracts_docx,
    get_all_contract_histories,
    get_contract_history_by_id,
    update_contract_history,
)
from app.api.routes.contract_histories.schemas import (
    ContractHistoriesRead,
    ContractHistoryCreate,
    ContractHistoryRead,
    ContractHistoryUpdate,
)


contract_history_router = APIRouter()


@contract_history_router.get("", response_model=ContractHistoriesRead)
def get_all(
    *,
    db_session: DbSession,
):
    return get_all_contract_histories(db_session=db_session)


@contract_history_router.get(
    "/{contract_history_id}", response_model=ContractHistoryRead
)
def get_one(*, db_session: DbSession, contract_history_id: int):
    return get_contract_history_by_id(
        db_session=db_session, contract_history_id=contract_history_id
    )


@contract_history_router.post("", response_model=ContractHistoryRead)
def create(*, db_session: DbSession, contract_history_in: ContractHistoryCreate):
    return create_contract_history(
        db_session=db_session, contract_history_in=contract_history_in
    )


@contract_history_router.put(
    "/{contract_history_id}", response_model=ContractHistoryRead
)
def update(
    *,
    db_session: DbSession,
    contract_history_id: int,
    contract_history_in: ContractHistoryUpdate,
):
    return update_contract_history(
        db_session=db_session,
        contract_history_id=contract_history_id,
        contract_history_in=contract_history_in,
    )


@contract_history_router.delete("/{contract_history_id}")
def delete(*, db_session: DbSession, contract_history_id: int):
    return delete_contract_history(
        db_session=db_session, contract_history_id=contract_history_id
    )


@contract_history_router.get("/export/{id}/")
def export_contract(
    *,
    db_session: DbSession,
    contract_ids: List[int],
    detail_benefit: Optional[bool] = None,
    detail_insurance: Optional[bool] = None,
):
    file_stream = generate_contract_docx(
        db_session=db_session,
        contract_ids=contract_ids,
        detail_benefit=detail_benefit,
        detail_insurance=detail_insurance,
    )
    return file_stream


@contract_history_router.get("/export/")
def export_contracts(
    *,
    db_session: DbSession,
    list_id: List[int] = Query(..., description="List of contract IDs to export"),
    detail_benefit: Optional[bool] = None,
    detail_insurance: Optional[bool] = None,
):
    file_stream = generate_multi_contracts_docx(
        db_session=db_session,
        contract_ids=list_id,
        detail_benefit=detail_benefit,
        detail_insurance=detail_insurance,
    )
    return file_stream


@contract_history_router.get("/export/all")
def export_all_contracts(
    *,
    db_session: DbSession,
    detail_benefit: Optional[bool] = True,
    detail_insurance: Optional[bool] = None,
):
    file_stream = generate_all_contracts_docx(
        db_session=db_session,
        detail_benefit=detail_benefit,
        detail_insurance=detail_insurance,
    )
    return file_stream

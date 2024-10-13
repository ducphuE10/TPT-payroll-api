from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from payroll.database.core import DbSession
from payroll.contract_histories.services import (
    create_contract_history,
    delete_contract_history,
    generate_contract_docx,
    get_all_contract_histories,
    get_contract_history_by_id,
    update_contract_history,
)
from payroll.contract_histories.schemas import (
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


# @contract_history_router.get(
#     "/{employee_code}/active-contract", response_model=ContractHistoryRead
# )
# def get_active(*, db_session: DbSession, employee_code: str, current_date: date):
#     return get_employee_active_contract(
#         db_session=db_session, employee_code=employee_code, current_date=current_date
#     )


@contract_history_router.post("", response_model=ContractHistoryRead)
def create(*, db_session: DbSession, contract_history_in: ContractHistoryCreate):
    return create_contract_history(
        db_session=db_session, contract_history_in=contract_history_in
    )


# # POST /schedules
# @contract_router.post("/both", response_model=ContractWithBenefitRead)
# def create_with_benefits(
#     *,
#     db_session: DbSession,
#     contract_in: ContractCreate,
#     benefits_list_in: Optional[List[CBAssocsCreate]] = None,
# ):
#     """Creates a new schedule."""
#     return contract_services.create_contract_with_benefits(
#         db_session=db_session,
#         contract_in=contract_in,
#         benefits_list_in=benefits_list_in,
#     )


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


@contract_history_router.get("/export/{id}")
def export_contract(*, db_session: DbSession, id: int):
    file_stream = generate_contract_docx(db_session=db_session, id=id)

    response = StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response.headers["Content-Disposition"] = f"attachment; filename=contract_{id}.docx"

    return response

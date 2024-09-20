from datetime import date
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from payroll.database.core import DbSession
from payroll.contracts.services import (
    create_contract,
    delete_contract,
    get_active_contract_benefits,
    get_all_contracts,
    get_contract_by_id,
    get_employee_active_contract,
    update_contract,
)
from payroll.contracts.schemas import (
    BenefitsRead,
    ContractRead,
    ContractCreate,
    ContractUpdate,
    ContractsRead,
)


contract_router = APIRouter()


@contract_router.get("", response_model=ContractsRead)
def get_all(
    *,
    db_session: DbSession,
):
    return get_all_contracts(db_session=db_session)


@contract_router.get("/benefits", response_model=BenefitsRead)
def get_active_benefits(*, db_session: DbSession, current_date: date = date.today()):
    return get_active_contract_benefits(
        db_session=db_session, current_date=current_date
    )


@contract_router.get("/{id}", response_model=ContractRead)
def get_one(*, db_session: DbSession, id: int):
    return get_contract_by_id(db_session=db_session, id=id)


@contract_router.get("/{employee_code}/active-contract", response_model=ContractRead)
def get_active(*, db_session: DbSession, employee_code: str, current_date: date):
    return get_employee_active_contract(
        db_session=db_session, employee_code=employee_code, current_date=current_date
    )


@contract_router.post("")
def create(*, db_session: DbSession, contract_in: ContractCreate):
    return create_contract(db_session=db_session, contract_in=contract_in)


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


@contract_router.put("/{id}")
def update(*, db_session: DbSession, contract_id: int, contract_in: ContractUpdate):
    return update_contract(
        db_session=db_session, contract_id=contract_id, contract_in=contract_in
    )


@contract_router.delete("/{id}")
def delete(*, db_session: DbSession, id: int):
    return delete_contract(db_session=db_session, id=id)


@contract_router.get("/export/{id}")
def export_contract(*, db_session: DbSession, id: int):
    file_stream = generate_contract_docx(db_session=db_session, id=id)

    response = StreamingResponse(
        file_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response.headers["Content-Disposition"] = f"attachment; filename=contract_{id}.docx"

    return response

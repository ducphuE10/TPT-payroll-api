from fastapi import APIRouter

from app.addendums.schemas import (
    AddendumCreate,
    AddendumRead,
    AddendumUpdate,
    AddendumsRead,
)
from app.addendums.services import (
    create_addendum,
    delete_addendum,
    get_addendum_by_id,
    get_all_addendums,
    update_addendum,
)
from app.db.core import DbSession


addendum_router = APIRouter()


@addendum_router.get("", response_model=AddendumsRead)
def get_all(
    *,
    db_session: DbSession,
):
    return get_all_addendums(db_session=db_session)


# @addendum_router.get("/benefits", response_model=BenefitsRead)
# def get_active_benefits(*, db_session: DbSession, current_date: date = date.today()):
#     return get_active_contract_benefits(
#         db_session=db_session, current_date=current_date
#     )


@addendum_router.get("/{addendum_id}", response_model=AddendumRead)
def get_one(*, db_session: DbSession, addendum_id: int):
    return get_addendum_by_id(db_session=db_session, addendum_id=addendum_id)


# @addendum_router.get("/{employee_code}/active-contract", response_model=ContractRead)
# def get_active(*, db_session: DbSession, employee_code: str, current_date: date):
#     return get_employee_active_contract(
#         db_session=db_session, employee_code=employee_code, current_date=current_date
#     )


@addendum_router.post("")
def create(*, db_session: DbSession, addendum_in: AddendumCreate):
    return create_addendum(db_session=db_session, addendum_in=addendum_in)


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


@addendum_router.put("/{addendum_id}")
def update(*, db_session: DbSession, addendum_id: int, addendum_in: AddendumUpdate):
    return update_addendum(
        db_session=db_session, addendum_id=addendum_id, addendum_in=addendum_in
    )


@addendum_router.delete("/{addendum_id}")
def delete(*, db_session: DbSession, addendum_id: int):
    return delete_addendum(db_session=db_session, addendum_id=addendum_id)


# @addendum_router.get("/export/{id}")
# def export_contract(*, db_session: DbSession, id: int):
#     file_stream = generate_contract_docx(db_session=db_session, id=id)

#     response = StreamingResponse(
#         file_stream,
#         media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#     )
#     response.headers["Content-Disposition"] = f"attachment; filename=contract_{id}.docx"

#     return response

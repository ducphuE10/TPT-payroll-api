from fastapi import APIRouter

from app.api.routes.companies.schemas import (
    CompanyRead,
    CompanyCreate,
    CompaniesRead,
    CompanyUpdate,
)
from app.db.core import DbSession
from app.api.routes.companies.services import (
    create_company,
    # delete_company,
    get_all_company,
    get_company_by_id,
    update_company,
)

company_router = APIRouter()


# GET /companies
@company_router.get("", response_model=CompaniesRead)
def retrieve_companies(
    *,
    db_session: DbSession,
):
    """Retrieve all companies."""
    return get_all_company(db_session=db_session)


# GET /companies/{company_id}
@company_router.get("/{company_id}", response_model=CompanyRead)
def retrieve_company(*, db_session: DbSession, company_id: int):
    """Retrieve a company by id."""
    return get_company_by_id(db_session=db_session, company_id=company_id)


# POST /companies
@company_router.post("", response_model=CompanyRead)
def create(*, company_in: CompanyCreate, db_session: DbSession):
    """Creates a new company."""
    return create_company(db_session=db_session, company_in=company_in)


# PUT /companies/{company_id}
@company_router.put("/{company_id}", response_model=CompanyRead)
def update(*, db_session: DbSession, company_id: int, company_in: CompanyUpdate):
    """Update a company by id."""
    return update_company(
        db_session=db_session, company_id=company_id, company_in=company_in
    )


# DELETE /companies/{company_id}
# @company_router.delete("/{company_id}", response_model=CompanyRead)
# def delete(*, db_session: DbSession, company_id: int):
#     """Delete a company by id."""
#     return delete_company(db_session=db_session, company_id=company_id)

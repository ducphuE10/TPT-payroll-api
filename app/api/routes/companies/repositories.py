import logging

from app.api.routes.companies.schemas import (
    CompanyCreate,
    CompanyUpdate,
)
from app.db.models import PayrollCompany

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /companies/{company_id}
def retrieve_company_by_id(*, db_session, company_id: int) -> PayrollCompany:
    """Returns a company based on the given id."""
    return (
        db_session.query(PayrollCompany).filter(PayrollCompany.id == company_id).first()
    )


def retrieve_company_by_code(
    *, db_session, company_code: str, owner_id: int
) -> PayrollCompany:
    """Returns a company based on the given code."""
    return (
        db_session.query(PayrollCompany)
        .filter(
            PayrollCompany.code == company_code and PayrollCompany.owner_id == owner_id
        )
        .first()
    )


# GET /companies
def retrieve_all_companies(*, db_session, owner_id: int) -> PayrollCompany:
    """Returns all companies."""
    query = db_session.query(PayrollCompany).filter(PayrollCompany.owner_id == owner_id)
    count = query.count()
    companies = query.order_by(PayrollCompany.id.asc()).all()

    return {"count": count, "data": companies}


# POST /companies
def add_company(*, db_session, company_in: CompanyCreate) -> PayrollCompany:
    """Creates a new company."""
    company = PayrollCompany(**company_in.model_dump())
    company.created_by = "admin"
    db_session.add(company)

    return company


# PUT /companies/{company_id}
def modify_company(
    *, db_session, company_id: int, company_in: CompanyUpdate
) -> PayrollCompany:
    """Updates a company with the given data."""
    query = db_session.query(PayrollCompany).filter(PayrollCompany.id == company_id)
    update_data = company_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_company = query.first()

    return updated_company


# DELETE /companies/{company_id}
# def remove_company(*, db_session, company_id: int):
#     """Deletes a company based on the given id."""
#     query = db_session.query(PayrollCompany).filter(PayrollCompany.id == company_id)
#     deleted_company = query.first()
#     query.delete()

#     return deleted_company

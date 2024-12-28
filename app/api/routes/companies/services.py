from app.api.routes.companies.repositories import (
    add_company,
    modify_company,
    remove_company,
    retrieve_all_companies,
    retrieve_company_by_code,
    retrieve_company_by_id,
)
from app.api.routes.companies.schemas import CompanyCreate, CompanyUpdate

# from app.api.routes.employees.repositories import retrieve_employee_by_company
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages


def check_exist_company_by_id(*, db_session, company_id: int):
    """Check if company exists in the database."""
    return bool(retrieve_company_by_id(db_session=db_session, company_id=company_id))


def check_exist_company_by_code(*, db_session, company_code: str):
    """Check if company exists in the database."""
    return bool(
        retrieve_company_by_code(db_session=db_session, company_code=company_code)
    )


# GET /companies/{company_id}
def get_company_by_id(*, db_session, company_id: int):
    """Returns a company based on the given id."""
    if not check_exist_company_by_id(db_session=db_session, company_id=company_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "company")

    return retrieve_company_by_id(db_session=db_session, company_id=company_id)


def get_company_by_code(*, db_session, company_code: int):
    """Returns a company based on the given code."""
    if not check_exist_company_by_code(
        db_session=db_session, company_code=company_code
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "company")

    return retrieve_company_by_code(db_session=db_session, company_code=company_code)


# GET /companies
def get_all_company(*, db_session):
    """Returns all companies."""
    companies = retrieve_all_companies(db_session=db_session)
    if not companies["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "company")

    return companies


# POST /companies
def create_company(*, db_session, company_in: CompanyCreate):
    """Creates a new company."""
    if check_exist_company_by_code(db_session=db_session, company_code=company_in.code):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "company")

    try:
        company = add_company(db_session=db_session, company_in=company_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return company


# PUT /companies/{company_id}
def update_company(*, db_session, company_id: int, company_in: CompanyUpdate):
    """Updates a company with the given data."""
    if not check_exist_company_by_id(db_session=db_session, company_id=company_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "company")

    try:
        company = modify_company(
            db_session=db_session,
            company_id=company_id,
            company_in=company_in,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return company


# DELETE /companies/{company_id}
# def delete_company(*, db_session, company_id: int):
#     """Deletes a company based on the given id."""
#     if not check_exist_company_by_id(db_session=db_session, company_id=company_id):
#         raise AppException(ErrorMessages.ResourceNotFound(), "company")

#     if retrieve_employee_by_company(db_session=db_session, company_id=company_id):
#         raise AppException(ErrorMessages.ExistDependObject(), ["company", "employee"])

#     try:
#         company = remove_company(db_session=db_session, company_id=company_id)
#         db_session.commit()
#     except Exception as e:
#         db_session.rollback()
#         raise AppException(ErrorMessages.ErrSM99999(), str(e))

#     return company

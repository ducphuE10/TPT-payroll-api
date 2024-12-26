from app.benefits.repositories import (
    add_benefit,
    modify_benefit,
    remove_benefit,
    retrieve_all_benefits,
    retrieve_benefit_by_code,
    retrieve_benefit_by_id,
)
from app.benefits.schemas import BenefitCreate, BenefitUpdate

# from payroll.employees.repositories import retrieve_employee_by_benefit
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages


def check_exist_benefit_by_id(*, db_session, benefit_id: int):
    """Check if benefit exists in the database."""
    return bool(retrieve_benefit_by_id(db_session=db_session, benefit_id=benefit_id))


def check_exist_benefit_by_code(*, db_session, benefit_code: str):
    """Check if benefit exists in the database."""
    return bool(
        retrieve_benefit_by_code(db_session=db_session, benefit_code=benefit_code)
    )


# GET /benefits/{benefit_id}
def get_benefit_by_id(*, db_session, benefit_id: int):
    """Returns a benefit based on the given id."""
    if not check_exist_benefit_by_id(db_session=db_session, benefit_id=benefit_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "benefit")

    return retrieve_benefit_by_id(db_session=db_session, benefit_id=benefit_id)


def get_benefit_by_code(*, db_session, benefit_code: int):
    """Returns a benefit based on the given code."""
    if not check_exist_benefit_by_code(
        db_session=db_session, benefit_code=benefit_code
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "benefit")

    return retrieve_benefit_by_code(db_session=db_session, benefit_code=benefit_code)


# GET /benefits
def get_all_benefit(*, db_session):
    """Returns all benefits."""
    benefits = retrieve_all_benefits(db_session=db_session)
    if not benefits["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "benefit")

    return benefits


# POST /benefits
def create_benefit(*, db_session, benefit_in: BenefitCreate):
    """Creates a new benefit."""
    if check_exist_benefit_by_code(db_session=db_session, benefit_code=benefit_in.code):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "benefit")

    try:
        benefit = add_benefit(db_session=db_session, benefit_in=benefit_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return benefit


# PUT /benefits/{benefit_id}
def update_benefit(*, db_session, benefit_id: int, benefit_in: BenefitUpdate):
    """Updates a benefit with the given data."""
    if not check_exist_benefit_by_id(db_session=db_session, benefit_id=benefit_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "benefit")

    try:
        benefit = modify_benefit(
            db_session=db_session,
            benefit_id=benefit_id,
            benefit_in=benefit_in,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return benefit


# DELETE /benefits/{benefit_id}
def delete_benefit(*, db_session, benefit_id: int):
    """Deletes a benefit based on the given id."""
    if not check_exist_benefit_by_id(db_session=db_session, benefit_id=benefit_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "benefit")

    # if retrieve_employee_by_benefit(
    #     db_session=db_session, benefit_id=benefit_id
    # ):
    #     raise AppException(
    #         ErrorMessages.ExistDependObject(), ["benefit", "employee"]
    #     )

    try:
        benefit = remove_benefit(db_session=db_session, benefit_id=benefit_id)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return benefit

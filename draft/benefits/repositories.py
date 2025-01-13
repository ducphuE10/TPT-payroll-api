import logging

from app.benefits.schemas import (
    BenefitCreate,
    BenefitUpdate,
)
from app.db.models import PayrollBenefit

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /benefits/{benefit_id}
def retrieve_benefit_by_id(*, db_session, benefit_id: int) -> PayrollBenefit:
    """Returns a benefit based on the given id."""
    return (
        db_session.query(PayrollBenefit).filter(PayrollBenefit.id == benefit_id).first()
    )


def retrieve_benefit_by_code(*, db_session, benefit_code: str) -> PayrollBenefit:
    """Returns a benefit based on the given code."""
    return (
        db_session.query(PayrollBenefit)
        .filter(PayrollBenefit.code == benefit_code)
        .first()
    )


# GET /benefits
def retrieve_all_benefits(*, db_session) -> PayrollBenefit:
    """Returns all benefits."""
    query = db_session.query(PayrollBenefit)
    count = query.count()
    benefits = query.all()

    return {"count": count, "data": benefits}


# POST /benefits
def add_benefit(*, db_session, benefit_in: BenefitCreate) -> PayrollBenefit:
    """Creates a new benefit."""
    benefit = PayrollBenefit(**benefit_in.model_dump())
    benefit.created_by = "admin"
    db_session.add(benefit)

    return benefit


# PUT /benefits/{benefit_id}
def modify_benefit(
    *, db_session, benefit_id: int, benefit_in: BenefitUpdate
) -> PayrollBenefit:
    """Updates a benefit with the given data."""
    query = db_session.query(PayrollBenefit).filter(PayrollBenefit.id == benefit_id)
    update_data = benefit_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_benefit = query.first()

    return updated_benefit


# DELETE /benefits/{benefit_id}
def remove_benefit(*, db_session, benefit_id: int):
    """Deletes a benefit based on the given id."""
    query = db_session.query(PayrollBenefit).filter(PayrollBenefit.id == benefit_id)
    deleted_benefit = query.first()
    query.delete()

    return deleted_benefit

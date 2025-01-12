import logging
from app.db.models import InsurancePolicy

log = logging.getLogger(__name__)


def get_insurance_policy_by_id(*, db_session, id: int) -> InsurancePolicy:
    """Returns a insurance policy based on the given id."""
    insurance_policy = (
        db_session.query(InsurancePolicy).filter(InsurancePolicy.id == id).first()
    )
    return insurance_policy


def get_insurance_policy_by_code(
    *, db_session, code: str, company_id: int
) -> InsurancePolicy:
    """Returns a insurance policy based on the given code."""
    insurance_policy = (
        db_session.query(InsurancePolicy)
        .filter(
            InsurancePolicy.code == code and InsurancePolicy.company_id == company_id
        )
        .first()
    )
    return insurance_policy


def get_all(*, db_session, company_id: int):
    """Returns all insurance policies."""
    return (
        db_session.query(InsurancePolicy)
        .filter(InsurancePolicy.company_id == company_id)
        .all()
    )


def create(*, db_session, create_data: dict) -> InsurancePolicy:
    """Creates a new insurance policy."""
    insurance_policy = InsurancePolicy(**create_data)
    insurance_policy.created_by = "admin"
    db_session.add(insurance_policy)
    return insurance_policy


def update(*, db_session, id: int, update_data: dict):
    """Updates a insurance policy with the given data."""
    db_session.query(InsurancePolicy).filter(InsurancePolicy.id == id).update(
        update_data, synchronize_session=False
    )


def delete(*, db_session, id: int) -> None:
    """Deletes a insurance policy based on the given id."""
    db_session.query(InsurancePolicy).filter(InsurancePolicy.id == id).delete()

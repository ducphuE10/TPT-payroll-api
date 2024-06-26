import logging
from payroll.models import TaxPolicy

log = logging.getLogger(__name__)


def get_tax_policy_by_id(*, db_session, id: int) -> TaxPolicy:
    """Returns a tax policy based on the given id."""
    return db_session.query(TaxPolicy).filter(TaxPolicy.id == id).first()


def get_tax_policy_by_code(*, db_session, code: str) -> TaxPolicy:
    """Returns a tax policy based on the given code."""
    return db_session.query(TaxPolicy).filter(TaxPolicy.code == code).first()


def get_all(*, db_session):
    """Returns all tax policies."""
    return db_session.query(TaxPolicy).all()


def create(*, db_session, create_data: dict) -> TaxPolicy:
    """Creates a new tax policy."""
    tax_policy = TaxPolicy(**create_data)
    db_session.add(tax_policy)
    db_session.commit()
    return tax_policy


def update(*, db_session, id: int, update_data: dict):
    """Updates a tax policy with the given data."""
    db_session.query(TaxPolicy).filter(TaxPolicy.id == id).update(
        update_data, synchronize_session=False
    )
    db_session.commit()


def delete(*, db_session, id: int) -> None:
    """Deletes a tax policy based on the given id."""
    db_session.query(TaxPolicy).filter(TaxPolicy.id == id).delete()
    db_session.commit()

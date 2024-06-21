import logging
from payroll.models import PayrollContract

log = logging.getLogger(__name__)


def get_contract_by_id(*, db_session, id: int) -> PayrollContract:
    """Returns a contract based on the given id."""
    contract = (
        db_session.query(PayrollContract).filter(PayrollContract.id == id).first()
    )
    return contract


def get_contract_by_code(*, db_session, code: str) -> PayrollContract:
    """Returns a contract based on the given code."""
    contract = (
        db_session.query(PayrollContract).filter(PayrollContract.code == code).first()
    )
    return contract


def get_all(*, db_session):
    """Returns all tax policies."""
    return db_session.query(PayrollContract).all()


def create(*, db_session, create_data: dict) -> PayrollContract:
    """Creates a new contract."""
    contract = PayrollContract(**create_data)
    db_session.add(contract)
    return contract


def update(*, db_session, id: int, update_data: dict):
    """Updates a contract with the given data."""
    db_session.query(PayrollContract).filter(PayrollContract.id == id).update(
        update_data, synchronize_session=False
    )


def delete(*, db_session, id: int) -> None:
    """Deletes a contract based on the given id."""
    db_session.query(PayrollContract).filter(PayrollContract.id == id).delete()

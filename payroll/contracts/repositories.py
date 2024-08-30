from datetime import date
import logging
from sqlalchemy import and_, or_

from fastapi import HTTPException
from payroll.models import PayrollContract, PayrollContractType

log = logging.getLogger(__name__)


def get_contract_by_id(*, db_session, id: int) -> PayrollContract:
    """Returns a contract based on the given id."""

    return db_session.query(PayrollContract).filter(PayrollContract.id == id).first()


def get_contract_by_code(*, db_session, code: str) -> PayrollContract:
    """Returns a contract based on the given code."""

    return (
        db_session.query(PayrollContract).filter(PayrollContract.code == code).first()
    )


def retrieve_contract_by_code(*, db_session, contract_code: str):
    return (
        db_session.query(PayrollContract).filter(PayrollContract.code == contract_code)
    ).first()


def retrieve_contract_by_employee_id_and_period(
    *, db_session, employee_code: str, from_date: date, to_date: date
):
    return (
        db_session.query(PayrollContract)
        .filter(
            PayrollContract.employee_code == employee_code,
            and_(
                PayrollContract.start_date <= to_date,
                or_(
                    PayrollContract.end_date.is_(None),
                    PayrollContract.end_date >= from_date,
                ),
            ),
        )
        .first()
    )


def get_all(*, db_session):
    """Returns all tax policies."""
    return db_session.query(PayrollContract).all()


def create(*, db_session, create_data: dict) -> PayrollContract:
    """Creates a new contract."""
    contract = PayrollContract(**create_data)
    contract.created_by = "admin"
    db_session.add(contract)
    return contract


def create_with_benefits(*, db_session, create_data: dict) -> PayrollContract:
    """Creates a new contract."""
    contract = PayrollContract(**create_data)
    contract.created_by = "admin"
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
    db_session.commit()


def get_contractType_template(*, db_session, code: str) -> PayrollContract:
    """Returns a contract template based on the given code."""
    contract_type = db_session.query(PayrollContractType).filter_by(code=code).first()
    if not contract_type or not contract_type.template:
        raise HTTPException(
            status_code=404, detail="Contract type or template not found"
        )

    return contract_type.template

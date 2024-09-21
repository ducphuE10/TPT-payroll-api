from datetime import date
import logging
from sqlalchemy import and_, or_

from fastapi import HTTPException
from payroll.models import PayrollContract
from payroll.utils.models import Status

log = logging.getLogger(__name__)


def retrieve_contract_by_id(*, db_session, contract_id: int) -> PayrollContract:
    """Returns a contract based on the given id."""
    return (
        db_session.query(PayrollContract)
        .filter(PayrollContract.id == contract_id)
        .first()
    )


def retrieve_contract_by_code(*, db_session, contract_code: str) -> PayrollContract:
    """Returns a contract based on the given code."""
    return (
        db_session.query(PayrollContract)
        .filter(PayrollContract.code == contract_code)
        .first()
    )


def retrieve_employee_active_contract(
    *, db_session, employee_code: str, current_date: date
):
    return (
        db_session.query(PayrollContract)
        .filter(
            and_(
                PayrollContract.employee_code == employee_code,
                PayrollContract.start_date <= current_date,
                (PayrollContract.end_date >= current_date)
                | (PayrollContract.end_date.is_(None)),
                PayrollContract.status == "ACTIVE",
            )
        )
        .first()
    )


def retrieve_active_contracts(*, db_session, current_date: date):
    return (
        db_session.query(PayrollContract)
        .filter(
            and_(
                PayrollContract.start_date <= current_date,
                (PayrollContract.end_date >= current_date)
                | (PayrollContract.end_date.is_(None)),
                PayrollContract.status == Status.ACTIVE,
            )
        )
        .all()
    )


def retrieve_contract_by_employee_and_period(
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


def retrieve_all_contracts(*, db_session):
    contracts = db_session.query(PayrollContract).all()

    return {"data": contracts}


def add_contract(*, db_session, create_data: dict) -> PayrollContract:
    """Creates a new contract."""
    contract = PayrollContract(**create_data)
    contract.created_by = "admin"
    db_session.add(contract)

    return contract


def modify_contract(*, db_session, contract_id: int, update_data: dict):
    """Updates a contract with the given data."""
    db_session.query(PayrollContract).filter(PayrollContract.id == contract_id).update(
        update_data, synchronize_session=False
    )


def remove_contract(*, db_session, id: int) -> None:
    """Deletes a contract based on the given id."""
    db_session.query(PayrollContract).filter(PayrollContract.id == id).delete()


def get_contract_template(*, db_session, code: str) -> PayrollContract:
    """Returns a contract template based on the given code."""
    template = db_session.query(PayrollContract).filter_by(code=code).first()
    if not template:
        raise HTTPException(
            status_code=404, detail="Contract type or template not found"
        )

    return template

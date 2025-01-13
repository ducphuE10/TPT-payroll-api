from datetime import date
import logging
from typing import Optional

from sqlalchemy import or_

from app.api.routes.contract_histories.schemas import (
    ContractHistoryCreate,
    ContractHistoryUpdate,
)
from app.db.models import PayrollContractHistory
from app.utils.models import ContractHistoryType

log = logging.getLogger(__name__)


def retrieve_contract_history_by_id(
    *, db_session, contract_history_id: int
) -> PayrollContractHistory:
    """Returns a contract based on the given id."""
    return (
        db_session.query(PayrollContractHistory)
        .filter(PayrollContractHistory.id == contract_history_id)
        .first()
    )


def retrieve_contract_histories_by_employee(*, db_session, employee_id: int):
    query = db_session.query(PayrollContractHistory).filter(
        PayrollContractHistory.employee_id == employee_id,
    )
    return query.all()


def retrieve_contract_history_by_employee_and_period(
    *, db_session, employee_id: int, from_date: date, to_date: Optional[date] = None
):
    query = db_session.query(PayrollContractHistory).filter(
        PayrollContractHistory.employee_id == employee_id,
        PayrollContractHistory.contract_type.in_(["CONTRACT"]),
        PayrollContractHistory.start_date <= from_date,
    )

    if to_date is not None:
        query.filter(PayrollContractHistory.end_date >= to_date)

    return query.first()


def retrieve_contract_history_addendum_by_employee_and_period(
    *, db_session, employee_id: int, from_date: date, to_date: Optional[date] = None
):
    query = db_session.query(PayrollContractHistory).filter(
        PayrollContractHistory.employee_id == employee_id,
        PayrollContractHistory.contract_type.in_(["ADDENDUM"]),
        PayrollContractHistory.start_date <= from_date,
    )

    if to_date is not None:
        query.filter(PayrollContractHistory.end_date >= to_date)

    return query.order_by(PayrollContractHistory.id.desc()).first()


def retrieve_contract_history_addendums_by_employee_and_period(
    *, db_session, employee_id: int, from_date: date, to_date: Optional[date] = None
):
    query = db_session.query(PayrollContractHistory).filter(
        PayrollContractHistory.employee_id == employee_id,
        PayrollContractHistory.contract_type == ContractHistoryType.ADDENDUM,
    )

    if to_date is not None:
        query = query.filter(PayrollContractHistory.start_date <= to_date)

    query = query.filter(
        or_(
            PayrollContractHistory.end_date.is_(None),
            PayrollContractHistory.end_date >= from_date,
        )
    )

    return query.all()


def retrieve_all_contract_histories(*, db_session, company_id: int):
    query = db_session.query(PayrollContractHistory)
    count = query.count()
    contract_histories = (
        query.filter(PayrollContractHistory.company_id == company_id)
        .order_by(PayrollContractHistory.id.asc())
        .all()
    )

    return {"count": count, "data": contract_histories}


def add_contract_history(
    *, db_session, contract_history_in: ContractHistoryCreate
) -> PayrollContractHistory:
    """Creates a new contract."""
    contract_history = PayrollContractHistory(**contract_history_in.model_dump())
    contract_history.created_by = "admin"
    db_session.add(contract_history)

    return contract_history


def modify_contract_history(
    *, db_session, contract_history_id: int, contract_history_in: ContractHistoryUpdate
):
    """Updates a contract with the given data."""
    update_data = contract_history_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollContractHistory).filter(
        PayrollContractHistory.id == contract_history_id
    )
    query.update(update_data, synchronize_session=False)
    updated_contract_history = query.first()

    return updated_contract_history


def remove_contract_history(*, db_session, contract_history_id: int) -> None:
    """Deletes a contract based on the given id."""
    db_session.query(PayrollContractHistory).filter(
        PayrollContractHistory.id == contract_history_id
    ).delete()

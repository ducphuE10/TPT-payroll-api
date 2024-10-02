from datetime import date
import logging

from sqlalchemy import and_, or_

from payroll.contract_histories.schemas import (
    ContractHistoryCreate,
    ContractHistoryUpdate,
)
from payroll.models import PayrollContractHistory
from payroll.utils.models import ContractHistoryType

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


# def retrieve_employee_active_contract(
#     *, db_session, employee_code: str, current_date: date
# ):
#     return (
#         db_session.query(PayrollContract)
#         .filter(
#             and_(
#                 PayrollContract.employee_code == employee_code,
#                 PayrollContract.start_date <= current_date,
#                 (PayrollContract.end_date >= current_date)
#                 | (PayrollContract.end_date.is_(None)),
#                 PayrollContract.status == "ACTIVE",
#             )
#         )
#         .first()
#     )


# def retrieve_active_contracts(*, db_session, current_date: date):
#     return (
#         db_session.query(PayrollContract)
#         .filter(
#             and_(
#                 PayrollContract.start_date <= current_date,
#                 (PayrollContract.end_date >= current_date)
#                 | (PayrollContract.end_date.is_(None)),
#                 PayrollContract.status == Status.ACTIVE,
#             )
#         )
#         .all()
#     )


def retrieve_contract_history_by_employee_and_period(
    *, db_session, employee_id: int, from_date: date, to_date: date
):
    return (
        db_session.query(PayrollContractHistory)
        .filter(
            PayrollContractHistory.employee_id == employee_id,
            PayrollContractHistory.contract_type == ContractHistoryType.CONTRACT,
            and_(
                PayrollContractHistory.start_date <= to_date,
                or_(
                    PayrollContractHistory.end_date.is_(None),
                    PayrollContractHistory.end_date >= from_date,
                ),
            ),
        )
        .first()
    )


def retrieve_contract_history_addendum_by_employee_and_period(
    *, db_session, employee_id: int, from_date: date, to_date: date
):
    return (
        db_session.query(PayrollContractHistory)
        .filter(
            PayrollContractHistory.employee_id == employee_id,
            PayrollContractHistory.contract_type == ContractHistoryType.ADDENDUM,
            and_(
                PayrollContractHistory.start_date <= to_date,
                or_(
                    PayrollContractHistory.end_date.is_(None),
                    PayrollContractHistory.end_date >= from_date,
                ),
            ),
        )
        .first()
    )


def retrieve_all_contract_histories(*, db_session):
    query = db_session.query(PayrollContractHistory)
    count = query.count()
    contract_histories = query.order_by(PayrollContractHistory.id.asc()).all()

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


# def get_contract_template(*, db_session, code: str) -> PayrollContract:
#     """Returns a contract template based on the given code."""
#     template = db_session.query(PayrollContract).filter_by(code=code).first()
#     if not template:
#         raise HTTPException(
#             status_code=404, detail="Contract type or template not found"
#         )

#     return template

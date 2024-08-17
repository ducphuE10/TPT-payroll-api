import logging

from payroll.welfares.schemas import (
    WelfareCreate,
    WelfareUpdate,
)
from payroll.models import PayrollWelfare

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /welfares/{welfare_id}
def retrieve_welfare_by_id(*, db_session, welfare_id: int) -> PayrollWelfare:
    """Returns a welfare based on the given id."""
    return (
        db_session.query(PayrollWelfare).filter(PayrollWelfare.id == welfare_id).first()
    )


def retrieve_welfare_by_code(*, db_session, welfare_code: str) -> PayrollWelfare:
    """Returns a welfare based on the given code."""
    return (
        db_session.query(PayrollWelfare)
        .filter(PayrollWelfare.code == welfare_code)
        .first()
    )


# GET /welfares
def retrieve_all_welfares(*, db_session) -> PayrollWelfare:
    """Returns all welfares."""
    query = db_session.query(PayrollWelfare)
    count = query.count()
    welfares = query.all()

    return {"count": count, "data": welfares}


# POST /welfares
def add_welfare(*, db_session, welfare_in: WelfareCreate) -> PayrollWelfare:
    """Creates a new welfare."""
    welfare = PayrollWelfare(**welfare_in.model_dump())
    welfare.created_by = "admin"
    db_session.add(welfare)

    return welfare


# PUT /welfares/{welfare_id}
def modify_welfare(
    *, db_session, welfare_id: int, welfare_in: WelfareUpdate
) -> PayrollWelfare:
    """Updates a welfare with the given data."""
    query = db_session.query(PayrollWelfare).filter(PayrollWelfare.id == welfare_id)
    update_data = welfare_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_welfare = query.first()

    return updated_welfare


# DELETE /welfares/{welfare_id}
def remove_welfare(*, db_session, welfare_id: int):
    """Deletes a welfare based on the given id."""
    query = db_session.query(PayrollWelfare).filter(PayrollWelfare.id == welfare_id)
    deleted_welfare = query.first()
    query.delete()

    return deleted_welfare

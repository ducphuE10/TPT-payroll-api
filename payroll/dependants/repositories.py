import logging

from sqlalchemy import func

from payroll.dependants.schemas import (
    DependantCreate,
    DependantUpdate,
)
from payroll.models import PayrollDependant

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /dependants/{dependant_id}
def retrieve_dependant_by_id(*, db_session, dependant_id: int) -> PayrollDependant:
    """Returns a dependant based on the given id."""
    return (
        db_session.query(PayrollDependant)
        .filter(PayrollDependant.id == dependant_id)
        .first()
    )


def retrieve_dependant_by_code(*, db_session, dependant_code: str) -> PayrollDependant:
    """Returns a dependant based on the given code."""
    return (
        db_session.query(PayrollDependant)
        .filter(PayrollDependant.code == dependant_code)
        .first()
    )


# def retrieve_dependant_by_cccd(
#     *, db_session, dependant_cccd: str, exclude_dependant_id: int = None
# ) -> PayrollDependant:
#     """Returns a dependant based on the given code."""
#     query = db_session.query(PayrollDependant).filter(
#         PayrollDependant.cccd == dependant_cccd
#     )
#     if exclude_dependant_id:
#         query = query.filter(PayrollDependant.id != exclude_dependant_id)

#     return query.first()


def retrieve_dependant_by_mst(
    *, db_session, dependant_mst: str, exclude_dependant_id: int = None
) -> PayrollDependant:
    """Returns a dependant based on the given code."""
    query = db_session.query(PayrollDependant).filter(
        PayrollDependant.mst == dependant_mst
    )
    if exclude_dependant_id:
        query = query.filter(PayrollDependant.id != exclude_dependant_id)

    return query.first()


def retrieve_all_dependants_by_employee_id(
    *, db_session, employee_id: int
) -> PayrollDependant:
    """Returns a dependant based on the given code."""
    query = db_session.query(PayrollDependant).filter(
        PayrollDependant.employee_id == employee_id
    )
    count = query.count()
    dependants = query.all()

    return {"count": count, "data": dependants}


# GET /dependants
def retrieve_all_dependants(*, db_session) -> PayrollDependant:
    """Returns all dependants."""
    query = db_session.query(PayrollDependant)
    count = query.count()
    dependants = query.all()

    return {"count": count, "data": dependants}


def search_dependants_by_partial_name(*, db_session, name: str):
    """Searches for dependants based on a partial name match (case-insensitive)."""
    query = db_session.query(PayrollDependant).filter(
        func.lower(PayrollDependant.name).like(f"%{name.lower()}%")
    )
    count = query.count()
    dependants = query.all()

    return {"count": count, "data": dependants}


# POST /dependants
def add_dependant(*, db_session, dependant_in: DependantCreate) -> PayrollDependant:
    """Creates a new dependant."""
    dependant = PayrollDependant(**dependant_in.model_dump())
    dependant.created_by = "admin"
    db_session.add(dependant)

    return dependant


# PUT /dependants/{dependant_id}
def modify_dependant(
    *, db_session, dependant_id: int, dependant_in: DependantUpdate
) -> PayrollDependant:
    """Updates a dependant with the given data."""
    update_data = dependant_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollDependant).filter(
        PayrollDependant.id == dependant_id
    )
    query.update(update_data, synchronize_session=False)
    updated_dependant = query.first()

    return updated_dependant


# DELETE /dependants/{dependant_id}
def remove_dependant(*, db_session, dependant_id: int):
    """Deletes a dependant based on the given id."""
    query = db_session.query(PayrollDependant).filter(
        PayrollDependant.id == dependant_id
    )
    deleted_dependant = query.first()
    query.delete()

    return deleted_dependant

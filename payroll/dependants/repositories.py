import logging

from sqlalchemy import func

from payroll.dependants.schemas import (
    DependentPersonCreate,
    DependentPersonUpdate,
)
from payroll.models import PayrollDependentPerson

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /dependants/{dependant_id}
def retrieve_dependant_by_id(
    *, db_session, dependant_id: int
) -> PayrollDependentPerson:
    """Returns a dependant based on the given id."""
    return (
        db_session.query(PayrollDependentPerson)
        .filter(PayrollDependentPerson.id == dependant_id)
        .first()
    )


def retrieve_dependant_by_code(
    *, db_session, dependant_code: str
) -> PayrollDependentPerson:
    """Returns a dependant based on the given code."""
    return (
        db_session.query(PayrollDependentPerson)
        .filter(PayrollDependentPerson.code == dependant_code)
        .first()
    )


def retrieve_dependant_by_cccd(
    *, db_session, dependant_cccd: str, exclude_dependant_id: int = None
) -> PayrollDependentPerson:
    """Returns a dependant based on the given code."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.cccd == dependant_cccd
    )
    if exclude_dependant_id:
        query = query.filter(PayrollDependentPerson.id != exclude_dependant_id)

    return query.first()


def retrieve_dependant_by_mst(
    *, db_session, dependant_mst: str, exclude_dependant_id: int = None
) -> PayrollDependentPerson:
    """Returns a dependant based on the given code."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.mst == dependant_mst
    )
    if exclude_dependant_id:
        query = query.filter(PayrollDependentPerson.id != exclude_dependant_id)

    return query.first()


def retrieve_all_dependants_by_employee_id(
    *, db_session, employee_id: int
) -> PayrollDependentPerson:
    """Returns a dependant based on the given code."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.employee_id == employee_id
    )
    count = query.count()
    dependants = query.all()

    return {"count": count, "data": dependants}


# GET /dependants
def retrieve_all_dependants(*, db_session) -> PayrollDependentPerson:
    """Returns all dependants."""
    query = db_session.query(PayrollDependentPerson)
    count = query.count()
    dependants = query.all()

    return {"count": count, "data": dependants}


def search_dependants_by_partial_name(*, db_session, name: str):
    """Searches for dependants based on a partial name match (case-insensitive)."""
    query = db_session.query(PayrollDependentPerson).filter(
        func.lower(PayrollDependentPerson.name).like(f"%{name.lower()}%")
    )
    count = query.count()
    dependants = query.all()

    return {"count": count, "data": dependants}


# POST /dependants
def add_dependant(
    *, db_session, dependant_in: DependentPersonCreate
) -> PayrollDependentPerson:
    """Creates a new dependant."""
    dependant = PayrollDependentPerson(**dependant_in.model_dump())
    dependant.created_by = "admin"
    db_session.add(dependant)

    return dependant


# PUT /dependants/{dependant_id}
def modify_dependant(
    *, db_session, dependant_id: int, dependant_in: DependentPersonUpdate
) -> PayrollDependentPerson:
    """Updates a dependant with the given data."""
    update_data = dependant_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.id == dependant_id
    )
    query.update(update_data, synchronize_session=False)
    updated_dependant = query.first()

    return updated_dependant


# DELETE /dependants/{dependant_id}
def remove_dependant(*, db_session, dependant_id: int):
    """Deletes a dependant based on the given id."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.id == dependant_id
    )
    deleted_dependant = query.first()
    query.delete()

    return deleted_dependant

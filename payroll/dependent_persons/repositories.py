import logging

from sqlalchemy import func

from payroll.dependent_persons.schemas import (
    DependentPersonCreate,
    DependentPersonUpdate,
)
from payroll.models import PayrollDependentPerson

# add, retrieve, modify, remove
log = logging.getLogger(__name__)


# GET /dependent_persons/{dependent_person_id}
def retrieve_dependent_person_by_id(
    *, db_session, dependent_person_id: int
) -> PayrollDependentPerson:
    """Returns a dependent_person based on the given id."""
    return (
        db_session.query(PayrollDependentPerson)
        .filter(PayrollDependentPerson.id == dependent_person_id)
        .first()
    )


def retrieve_dependent_person_by_code(
    *, db_session, dependent_person_code: str
) -> PayrollDependentPerson:
    """Returns a dependent_person based on the given code."""
    return (
        db_session.query(PayrollDependentPerson)
        .filter(PayrollDependentPerson.code == dependent_person_code)
        .first()
    )


def retrieve_dependent_person_by_cccd(
    *, db_session, dependent_person_cccd: str, exclude_dependent_person_id: int = None
) -> PayrollDependentPerson:
    """Returns a dependent_person based on the given code."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.cccd == dependent_person_cccd
    )
    if exclude_dependent_person_id:
        query = query.filter(PayrollDependentPerson.id != exclude_dependent_person_id)

    return query.first()


def retrieve_dependent_person_by_mst(
    *, db_session, dependent_person_mst: str, exclude_dependent_person_id: int = None
) -> PayrollDependentPerson:
    """Returns a dependent_person based on the given code."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.mst == dependent_person_mst
    )
    if exclude_dependent_person_id:
        query = query.filter(PayrollDependentPerson.id != exclude_dependent_person_id)

    return query.first()


def retrieve_all_dependent_persons_by_employee_id(
    *, db_session, employee_id: int
) -> PayrollDependentPerson:
    """Returns a dependent_person based on the given code."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.employee_id == employee_id
    )
    count = query.count()
    dependent_persons = query.all()

    return {"count": count, "data": dependent_persons}


# GET /dependent_persons
def retrieve_all_dependent_persons(*, db_session) -> PayrollDependentPerson:
    """Returns all dependent_persons."""
    query = db_session.query(PayrollDependentPerson)
    count = query.count()
    dependent_persons = query.all()

    return {"count": count, "data": dependent_persons}


def search_dependent_persons_by_partial_name(*, db_session, name: str):
    """Searches for dependent_persons based on a partial name match (case-insensitive)."""
    query = db_session.query(PayrollDependentPerson).filter(
        func.lower(PayrollDependentPerson.name).like(f"%{name.lower()}%")
    )
    count = query.count()
    dependent_persons = query.all()

    return {"count": count, "data": dependent_persons}


# POST /dependent_persons
def add_dependent_person(
    *, db_session, dependent_person_in: DependentPersonCreate
) -> PayrollDependentPerson:
    """Creates a new dependent_person."""
    dependent_person = PayrollDependentPerson(**dependent_person_in.model_dump())
    dependent_person.created_by = "admin"
    db_session.add(dependent_person)

    return dependent_person


# PUT /dependent_persons/{dependent_person_id}
def modify_dependent_person(
    *, db_session, dependent_person_id: int, dependent_person_in: DependentPersonUpdate
) -> PayrollDependentPerson:
    """Updates a dependent_person with the given data."""
    update_data = dependent_person_in.model_dump(exclude_unset=True)
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.id == dependent_person_id
    )
    query.update(update_data, synchronize_session=False)
    updated_dependent_person = query.first()

    return updated_dependent_person


# DELETE /dependent_persons/{dependent_person_id}
def remove_dependent_person(*, db_session, dependent_person_id: int):
    """Deletes a dependent_person based on the given id."""
    query = db_session.query(PayrollDependentPerson).filter(
        PayrollDependentPerson.id == dependent_person_id
    )
    deleted_dependent_person = query.first()
    query.delete()

    return deleted_dependent_person

from fastapi import APIRouter

from payroll.dependent_persons.schemas import (
    DependentPersonRead,
    DependentPersonCreate,
    DependentPersonsRead,
    DependentPersonUpdate,
)
from payroll.database.core import DbSession
from payroll.dependent_persons.services import (
    create_dependent_person,
    delete_dependent_person,
    get_all_dependent_persons,
    get_dependent_person_by_id,
    update_dependent_person,
    search_dependent_person_by_name,
)

dependent_person_router = APIRouter()


# GET /dependent_persons
@dependent_person_router.get("", response_model=DependentPersonsRead)
def retrieve_dependent_persons(*, db_session: DbSession, name: str = None):
    """Returns all dependent_persons."""
    if name:
        return search_dependent_person_by_name(db_session=db_session, name=name)
    return get_all_dependent_persons(db_session=db_session)


# GET /dependent_persons/{dependent_person_id}
@dependent_person_router.get(
    "/{dependent_person_id}", response_model=DependentPersonRead
)
def get_dependent_person(*, db_session: DbSession, dependent_person_id: int):
    """Returns a dependent_person based on the given id."""
    return get_dependent_person_by_id(
        db_session=db_session, dependent_person_id=dependent_person_id
    )


# POST /dependent_persons
@dependent_person_router.post("", response_model=DependentPersonRead)
def create(*, dependent_person_in: DependentPersonCreate, db_session: DbSession):
    """Creates a new dependent_person."""
    return create_dependent_person(
        db_session=db_session, dependent_person_in=dependent_person_in
    )


# PUT /dependent_persons/{dependent_person_id}
@dependent_person_router.put(
    "/{dependent_person_id}", response_model=DependentPersonRead
)
def update(
    *,
    db_session: DbSession,
    dependent_person_id: int,
    dependent_person_in: DependentPersonUpdate,
):
    """Updates a dependent_person with the given data."""
    return update_dependent_person(
        db_session=db_session,
        dependent_person_id=dependent_person_id,
        dependent_person_in=dependent_person_in,
    )


# DELETE /dependent_persons/{dependent_person_id}
@dependent_person_router.delete(
    "/{dependent_person_id}", response_model=DependentPersonRead
)
def delete(*, db_session: DbSession, dependent_person_id: int):
    """Deletes a dependent_person based on the given id."""
    return delete_dependent_person(
        db_session=db_session, dependent_person_id=dependent_person_id
    )

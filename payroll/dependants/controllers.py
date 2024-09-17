from fastapi import APIRouter

from payroll.dependants.schemas import (
    DependantRead,
    DependantCreate,
    DependantsRead,
    DependantUpdate,
)
from payroll.database.core import DbSession
from payroll.dependants.services import (
    create_dependant,
    delete_dependant,
    get_all_dependants,
    get_dependant_by_id,
    update_dependant,
    search_dependant_by_name,
)

dependant_router = APIRouter()


# GET /dependants
@dependant_router.get("", response_model=DependantsRead)
def retrieve_dependants(*, db_session: DbSession, name: str = None):
    """Returns all dependants."""
    if name:
        return search_dependant_by_name(db_session=db_session, name=name)
    return get_all_dependants(db_session=db_session)


# GET /dependants/{dependant_id}
@dependant_router.get("/{dependant_id}", response_model=DependantRead)
def get_dependant(*, db_session: DbSession, dependant_id: int):
    """Returns a dependant based on the given id."""
    return get_dependant_by_id(db_session=db_session, dependant_id=dependant_id)


# POST /dependants
@dependant_router.post("", response_model=DependantRead)
def create(*, dependant_in: DependantCreate, db_session: DbSession):
    """Creates a new dependant."""
    return create_dependant(db_session=db_session, dependant_in=dependant_in)


# PUT /dependants/{dependant_id}
@dependant_router.put("/{dependant_id}", response_model=DependantRead)
def update(
    *,
    db_session: DbSession,
    dependant_id: int,
    dependant_in: DependantUpdate,
):
    """Updates a dependant with the given data."""
    return update_dependant(
        db_session=db_session,
        dependant_id=dependant_id,
        dependant_in=dependant_in,
    )


# DELETE /dependants/{dependant_id}
@dependant_router.delete("/{dependant_id}", response_model=DependantRead)
def delete(*, db_session: DbSession, dependant_id: int):
    """Deletes a dependant based on the given id."""
    return delete_dependant(db_session=db_session, dependant_id=dependant_id)

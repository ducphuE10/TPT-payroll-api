from fastapi import APIRouter

from app.contract_benefit_assocs.schemas import (
    CBAssocRead,
    CBAssocCreate,
    CBAssocsRead,
    CBAssocUpdate,
)
from app.db.core import DbSession
from app.contract_benefit_assocs.services import (
    create_cbassoc,
    delete_cbassoc,
    get_all_cbassoc,
    get_cbassoc_by_id,
    update_cbassoc,
)

cbassoc_router = APIRouter()


# GET /cbassocs
@cbassoc_router.get("", response_model=CBAssocsRead)
def retrieve_cbassocs(
    *,
    db_session: DbSession,
):
    """Retrieve all cbassocs."""
    return get_all_cbassoc(db_session=db_session)


# GET /cbassocs/{cbassoc_id}
@cbassoc_router.get("/{cbassoc_id}", response_model=CBAssocRead)
def retrieve_cbassoc(*, db_session: DbSession, cbassoc_id: int):
    """Retrieve a cbassoc by id."""
    return get_cbassoc_by_id(db_session=db_session, cbassoc_id=cbassoc_id)


# POST /cbassocs
@cbassoc_router.post("", response_model=CBAssocRead)
def create(*, cbassoc_in: CBAssocCreate, db_session: DbSession):
    """Creates a new cbassoc."""
    return create_cbassoc(db_session=db_session, cbassoc_in=cbassoc_in)


# PUT /cbassocs/{cbassoc_id}
@cbassoc_router.put("/{cbassoc_id}", response_model=CBAssocRead)
def update(*, db_session: DbSession, cbassoc_id: int, cbassoc_in: CBAssocUpdate):
    """Update a cbassoc by id."""
    return update_cbassoc(
        db_session=db_session, cbassoc_id=cbassoc_id, cbassoc_in=cbassoc_in
    )


# DELETE /cbassocs/{cbassoc_id}
@cbassoc_router.delete("/{cbassoc_id}", response_model=CBAssocRead)
def delete(*, db_session: DbSession, cbassoc_id: int):
    """Delete a cbassoc by id."""
    return delete_cbassoc(db_session=db_session, cbassoc_id=cbassoc_id)

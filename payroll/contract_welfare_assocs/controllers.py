from fastapi import APIRouter

from payroll.contract_welfare_assocs.schemas import (
    CWAssocRead,
    CWAssocCreate,
    CWAssocsRead,
    CWAssocUpdate,
)
from payroll.database.core import DbSession
from payroll.contract_welfare_assocs.services import (
    create_cwassoc,
    delete_cwassoc,
    get_all_cwassoc,
    get_cwassoc_by_id,
    update_cwassoc,
)

cwassoc_router = APIRouter()


# GET /cwassocs
@cwassoc_router.get("", response_model=CWAssocsRead)
def retrieve_cwassocs(
    *,
    db_session: DbSession,
):
    """Retrieve all cwassocs."""
    return get_all_cwassoc(db_session=db_session)


# GET /cwassocs/{cwassoc_id}
@cwassoc_router.get("/{cwassoc_id}", response_model=CWAssocRead)
def retrieve_cwassoc(*, db_session: DbSession, cwassoc_id: int):
    """Retrieve a cwassoc by id."""
    return get_cwassoc_by_id(db_session=db_session, cwassoc_id=cwassoc_id)


# POST /cwassocs
@cwassoc_router.post("", response_model=CWAssocRead)
def create(*, cwassoc_in: CWAssocCreate, db_session: DbSession):
    """Creates a new cwassoc."""
    return create_cwassoc(db_session=db_session, cwassoc_in=cwassoc_in)


# PUT /cwassocs/{cwassoc_id}
@cwassoc_router.put("/{cwassoc_id}", response_model=CWAssocRead)
def update(*, db_session: DbSession, cwassoc_id: int, cwassoc_in: CWAssocUpdate):
    """Update a cwassoc by id."""
    return update_cwassoc(
        db_session=db_session, cwassoc_id=cwassoc_id, cwassoc_in=cwassoc_in
    )


# DELETE /cwassocs/{cwassoc_id}
@cwassoc_router.delete("/{cwassoc_id}", response_model=CWAssocRead)
def delete(*, db_session: DbSession, cwassoc_id: int):
    """Delete a cwassoc by id."""
    return delete_cwassoc(db_session=db_session, cwassoc_id=cwassoc_id)

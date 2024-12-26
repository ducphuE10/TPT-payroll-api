from fastapi import APIRouter, File, Form, UploadFile

from app.api.routes.dependants.schemas import (
    DependantRead,
    DependantCreate,
    DependantsRead,
    DependantUpdate,
)
from app.db.core import DbSession
from app.api.routes.dependants.services import (
    create_dependant,
    delete_dependant,
    get_all_dependants,
    get_dependant_by_id,
    update_dependant,
    search_dependant_by_name,
    upload_dependants_XLSX,
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


# POST /employees/import-excel
@dependant_router.post("/import-excel")
def import_excel(
    *, db: DbSession, file: UploadFile = File(...), update_on_exists: bool = Form(False)
):
    return upload_dependants_XLSX(
        db_session=db, file=file, update_on_exists=update_on_exists
    )

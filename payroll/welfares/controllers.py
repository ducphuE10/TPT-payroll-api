from fastapi import APIRouter

from payroll.welfares.schemas import (
    WelfareRead,
    WelfareCreate,
    WelfaresRead,
    WelfareUpdate,
)
from payroll.database.core import DbSession
from payroll.welfares.services import (
    create_welfare,
    delete_welfare,
    get_all_welfare,
    get_welfare_by_id,
    update_welfare,
)

welfare_router = APIRouter()


# GET /welfares
@welfare_router.get("", response_model=WelfaresRead)
def retrieve_welfares(
    *,
    db_session: DbSession,
):
    """Retrieve all welfares."""
    return get_all_welfare(db_session=db_session)


# GET /welfares/{welfare_id}
@welfare_router.get("/{welfare_id}", response_model=WelfareRead)
def retrieve_welfare(*, db_session: DbSession, welfare_id: int):
    """Retrieve a welfare by id."""
    return get_welfare_by_id(db_session=db_session, welfare_id=welfare_id)


# POST /welfares
@welfare_router.post("", response_model=WelfareRead)
def create(*, welfare_in: WelfareCreate, db_session: DbSession):
    """Creates a new welfare."""
    return create_welfare(db_session=db_session, welfare_in=welfare_in)


# PUT /welfares/{welfare_id}
@welfare_router.put("/{welfare_id}", response_model=WelfareRead)
def update(*, db_session: DbSession, welfare_id: int, welfare_in: WelfareUpdate):
    """Update a welfare by id."""
    return update_welfare(
        db_session=db_session, welfare_id=welfare_id, welfare_in=welfare_in
    )


# DELETE /welfares/{welfare_id}
@welfare_router.delete("/{welfare_id}", response_model=WelfareRead)
def delete(*, db_session: DbSession, welfare_id: int):
    """Delete a welfare by id."""
    return delete_welfare(db_session=db_session, welfare_id=welfare_id)

from fastapi import APIRouter

from payroll.position.models import (
    PositionRead,
    PositionCreate,
    PositionsRead,
    PositionUpdate,
)
from payroll.database.core import DbSession
from payroll.position.service import get_by_id, delete, get, create, update

position_router = APIRouter()


@position_router.get("/", response_model=PositionsRead)
def retrieve_positions(
    *,
    db_session: DbSession,
):
    return get(db_session=db_session)


@position_router.get("/{id}", response_model=PositionRead)
def retrieve_position(*, db_session: DbSession, id: int):
    return get_by_id(db_session=db_session, id=id)


@position_router.post("/", response_model=PositionRead)
def create_position(*, position_in: PositionCreate, db_session: DbSession):
    """Creates a new user."""
    position_in.created_by = "admin"
    position = create(db_session=db_session, position_in=position_in)
    return position


@position_router.put("/{id}", response_model=PositionRead)
def update_position(*, db_session: DbSession, id: int, position_in: PositionUpdate):
    return update(db_session=db_session, id=id, position_in=position_in)


@position_router.delete("/{id}", response_model=PositionRead)
def delete_position(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)

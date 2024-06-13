from fastapi import APIRouter

from payroll.positions.schemas import (
    PositionRead,
    PositionCreate,
    PositionsRead,
    PositionUpdate,
)
from payroll.database.core import DbSession
from payroll.positions.repositories import (
    get_all,
    get_one_by_id,
    create,
    update,
    delete,
)

position_router = APIRouter()


@position_router.get("", response_model=PositionsRead)
def retrieve_positions(
    *,
    db_session: DbSession,
):
    return get_all(db_session=db_session)


@position_router.get("/{id}", response_model=PositionRead)
def retrieve_position(*, db_session: DbSession, id: int):
    return get_one_by_id(db_session=db_session, id=id)


@position_router.post("", response_model=PositionRead)
def create_position(*, position_in: PositionCreate, db_session: DbSession):
    """Creates a new user."""
    position = create(db_session=db_session, position_in=position_in)
    return position


@position_router.put("/{id}", response_model=PositionRead)
def update_position(*, db_session: DbSession, id: int, position_in: PositionUpdate):
    return update(db_session=db_session, id=id, position_in=position_in)


@position_router.delete("/{id}", response_model=PositionRead)
def delete_position(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)

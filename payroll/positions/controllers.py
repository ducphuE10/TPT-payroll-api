from fastapi import APIRouter

from payroll.positions.schemas import (
    PositionRead,
    PositionCreate,
    PositionsRead,
    PositionUpdate,
)
from payroll.database.core import DbSession
from payroll.positions.services import (
    create_position,
    delete_position,
    get_all_position,
    get_position_by_id,
    update_position,
)

position_router = APIRouter()


# GET /positions
@position_router.get("", response_model=PositionsRead)
def retrieve_positions(
    *,
    db_session: DbSession,
):
    """Retrieve all positions."""
    return get_all_position(db_session=db_session)


# GET /positions/{position_id}
@position_router.get("/{position_id}", response_model=PositionRead)
def retrieve_position(*, db_session: DbSession, position_id: int):
    """Retrieve a position by id."""
    return get_position_by_id(db_session=db_session, position_id=position_id)


# POST /positions
@position_router.post("", response_model=PositionRead)
def create(*, position_in: PositionCreate, db_session: DbSession):
    """Creates a new position."""
    position = create_position(db_session=db_session, position_in=position_in)
    return position


# PUT /positions/{position_id}
@position_router.put("/{position_id}", response_model=PositionRead)
def update(*, db_session: DbSession, position_id: int, position_in: PositionUpdate):
    """Update a position by id."""
    return update_position(
        db_session=db_session, position_id=position_id, position_in=position_in
    )


# DELETE /positions/{position_id}
@position_router.delete("/{position_id}")
def delete(*, db_session: DbSession, position_id: int):
    """Delete a position by id."""
    return delete_position(db_session=db_session, position_id=position_id)

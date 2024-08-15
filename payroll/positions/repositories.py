import logging

from payroll.positions.schemas import (
    PositionCreate,
    PositionsRead,
    PositionUpdate,
)
from payroll.models import PayrollPosition

log = logging.getLogger(__name__)


# GET /positions/{position_id}
def retrieve_position_by_id(*, db_session, position_id: int) -> PayrollPosition:
    """Returns a position based on the given id."""
    return (
        db_session.query(PayrollPosition)
        .filter(PayrollPosition.id == position_id)
        .first()
    )


def retrieve_position_by_code(*, db_session, position_code: str) -> PayrollPosition:
    """Returns a position based on the given code."""
    return (
        db_session.query(PayrollPosition)
        .filter(PayrollPosition.code == position_code)
        .first()
    )


# GET /positions
def retrieve_all_positions(*, db_session) -> PositionsRead:
    """Returns all positions."""
    query = db_session.query(PayrollPosition)
    count = query.count()
    positions = query.all()

    return {"count": count, "data": positions}


# POST /positions
def add_position(*, db_session, position_in: PositionCreate) -> PayrollPosition:
    """Creates a new position."""
    position = PayrollPosition(**position_in.model_dump())
    position.created_by = "admin"
    db_session.add(position)

    return position


# PUT /positions/{position_id}
def modify_position(
    *, db_session, position_id: int, position_in: PositionUpdate
) -> PayrollPosition:
    """Updates a position with the given data."""
    query = db_session.query(PayrollPosition).filter(PayrollPosition.id == position_id)
    update_data = position_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_position = query.first()

    return updated_position


# DELETE /positions/{position_id}
def remove_position(*, db_session, position_id: int):
    """Deletes a position based on the given id."""
    query = db_session.query(PayrollPosition).filter(PayrollPosition.id == position_id)
    deleted_position = query.first()
    query.delete()

    return deleted_position

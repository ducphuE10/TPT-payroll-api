import logging
from fastapi import HTTPException, status
from payroll.models import PayrollPosition
from payroll.positions.schemas import (
    PositionRead,
    PositionCreate,
    PositionsRead,
    PositionUpdate,
)

log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)


def get_position_by_id(*, db_session, id: int) -> PositionRead:
    """Returns a position based on the given id."""
    position = (
        db_session.query(PayrollPosition).filter(PayrollPosition.id == id).first()
    )
    return position


def get_position_by_code(*, db_session, code: str) -> PositionRead:
    """Returns a position based on the given code."""
    position = (
        db_session.query(PayrollPosition).filter(PayrollPosition.code == code).first()
    )
    return position


def get_all(*, db_session) -> PositionsRead:
    """Returns all positions."""
    data = db_session.query(PayrollPosition).all()
    return PositionsRead(data=data)


def get_one_by_id(*, db_session, id: int) -> PositionRead:
    """Returns a position based on the given id."""
    position = get_position_by_id(db_session=db_session, id=id)

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found",
        )
    return position


def create(*, db_session, position_in: PositionCreate) -> PositionRead:
    """Creates a new position."""
    position = PayrollPosition(**position_in.model_dump())
    position_db = get_position_by_code(db_session=db_session, code=position.code)
    if position_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position already exists",
        )
    db_session.add(position)
    db_session.commit()
    return position


def update(*, db_session, id: int, position_in: PositionUpdate) -> PositionRead:
    """Updates a position with the given data."""
    position_db = get_position_by_id(db_session=db_session, id=id)

    if not position_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found",
        )

    update_data = position_in.model_dump(exclude_unset=True)

    db_session.query(PayrollPosition).filter(PayrollPosition.id == id).update(
        update_data, synchronize_session=False
    )

    db_session.commit()
    return position_db


def delete(*, db_session, id: int) -> PositionRead:
    """Deletes a position based on the given id."""
    query = db_session.query(PayrollPosition).filter(PayrollPosition.id == id)
    position = query.first()

    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found",
        )

    db_session.query(PayrollPosition).filter(PayrollPosition.id == id).delete()

    db_session.commit()
    return position

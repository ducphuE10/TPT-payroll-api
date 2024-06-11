import logging

from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollPosition
from payroll.positions.schemas import (
    PositionCreate,
    PositionsRead,
    PositionUpdate,
)

log = logging.getLogger(__name__)


def get_position_by_id(*, db_session, id: int) -> PayrollPosition:
    """Returns a position based on the given id."""
    position = (
        db_session.query(PayrollPosition).filter(PayrollPosition.id == id).first()
    )
    return position


def get_position_by_code(*, db_session, code: str) -> PayrollPosition:
    """Returns a position based on the given code."""
    position = (
        db_session.query(PayrollPosition).filter(PayrollPosition.code == code).first()
    )
    return position


def get_all(*, db_session) -> PayrollPosition:
    """Returns all positions."""
    data = db_session.query(PayrollPosition).all()
    return PositionsRead(data=data)


def get_one_by_id(*, db_session, id: int) -> PayrollPosition:
    """Returns a position based on the given id."""
    position = get_position_by_id(db_session=db_session, id=id)

    if not position:
        raise AppException(ErrorMessages.ResourceNotFound())
    return position


def create(*, db_session, position_in: PositionCreate) -> PayrollPosition:
    """Creates a new position."""
    position = PayrollPosition(**position_in.model_dump())
    position_db = get_position_by_code(db_session=db_session, code=position.code)
    if position_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    db_session.add(position)
    db_session.commit()
    return position


def update(*, db_session, id: int, position_in: PositionUpdate) -> PayrollPosition:
    """Updates a position with the given data."""
    position_db = get_position_by_id(db_session=db_session, id=id)

    if not position_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = position_in.model_dump(exclude_unset=True)

    db_session.query(PayrollPosition).filter(PayrollPosition.id == id).update(
        update_data, synchronize_session=False
    )

    db_session.commit()
    return position_db


def delete(*, db_session, id: int) -> PayrollPosition:
    """Deletes a position based on the given id."""
    query = db_session.query(PayrollPosition).filter(PayrollPosition.id == id)
    position = query.first()

    if not position:
        raise AppException(ErrorMessages.ResourceNotFound())

    db_session.query(PayrollPosition).filter(PayrollPosition.id == id).delete()

    db_session.commit()
    return position

import logging


from app.api.routes.shifts.schemas import (
    ShiftCreate,
    ShiftsRead,
    ShiftUpdate,
)
from app.db.models import PayrollShift

log = logging.getLogger(__name__)


# GET /shifts/{shift_id}
def retrieve_shift_by_id(*, db_session, shift_id: int) -> PayrollShift:
    """Returns a shift based on the given id."""
    return db_session.query(PayrollShift).filter(PayrollShift.id == shift_id).first()


def retrieve_shift_by_code(
    *, db_session, shift_code: str, company_id: int
) -> PayrollShift:
    """Returns a shift based on the given code."""
    return (
        db_session.query(PayrollShift)
        .filter(
            PayrollShift.code == shift_code and PayrollShift.company_id == company_id
        )
        .first()
    )


# GET /shifts
def retrieve_all_shifts(*, db_session, company_id: int) -> ShiftsRead:
    """Returns all shifts."""
    query = db_session.query(PayrollShift).filter(PayrollShift.company_id == company_id)
    count = query.count()
    shifts = query.order_by(PayrollShift.id.asc()).all()

    return {"count": count, "data": shifts}


# POST /shifts
def add_shift(*, db_session, shift_in: ShiftCreate) -> PayrollShift:
    """Creates a new shift."""
    shift = PayrollShift(**shift_in.model_dump())
    shift.created_by = "admin"
    db_session.add(shift)

    return shift


# PUT /shifts/{shift_id}
def modify_shift(*, db_session, shift_id: int, shift_in: ShiftUpdate) -> PayrollShift:
    """Updates a shift with the given data."""
    query = db_session.query(PayrollShift).filter(PayrollShift.id == shift_id)
    update_data = shift_in.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    updated_shift = query.first()

    return updated_shift


# DELETE /shifts/{shift_id}
def remove_shift(*, db_session, shift_id: int):
    """Deletes a shift based on the given id."""
    query = db_session.query(PayrollShift).filter(PayrollShift.id == shift_id)
    delete_shift = query.first()
    query.delete()

    return delete_shift

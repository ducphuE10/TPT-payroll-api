from fastapi import APIRouter

from payroll.shifts.schemas import (
    ShiftRead,
    ShiftCreate,
    ShiftsRead,
    ShiftUpdate,
)
from payroll.database.core import DbSession
from payroll.shifts.services import (
    create_shift,
    delete_shift,
    get_all_shift,
    get_shift_by_id,
    update_shift,
)

shift_router = APIRouter()


# GET /shifts
@shift_router.get("", response_model=ShiftsRead)
def retrieve_shifts(
    *,
    db_session: DbSession,
):
    """Retrieve all shifts."""
    return get_all_shift(db_session=db_session)


# GET /shifts/{shift_id}
@shift_router.get("/{shift_id}", response_model=ShiftRead)
def retrieve_shift(*, db_session: DbSession, shift_id: int):
    """Retrieve a shift by id."""
    return get_shift_by_id(db_session=db_session, shift_id=shift_id)


# POST /shifts
@shift_router.post("", response_model=ShiftRead)
def create(*, shift_in: ShiftCreate, db_session: DbSession):
    """Creates a new shift."""
    shift = create_shift(db_session=db_session, shift_in=shift_in)
    return shift


# PUT /shifts/{shift_id}
@shift_router.put("/{shift_id}", response_model=ShiftRead)
def update(*, db_session: DbSession, shift_id: int, shift_in: ShiftUpdate):
    """Update a shift by id."""
    return update_shift(db_session=db_session, shift_id=shift_id, shift_in=shift_in)


# DELETE /shifts/{shift_id}
@shift_router.delete("/{shift_id}")
def delete(*, db_session: DbSession, shift_id: int):
    """Delete a shift by id."""
    return delete_shift(db_session=db_session, shift_id=shift_id)

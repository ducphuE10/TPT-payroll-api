from fastapi import APIRouter

from app.benefits.schemas import (
    BenefitRead,
    BenefitCreate,
    BenefitsRead,
    BenefitUpdate,
)
from app.db.core import DbSession
from app.benefits.services import (
    create_benefit,
    delete_benefit,
    get_all_benefit,
    get_benefit_by_id,
    update_benefit,
)

benefit_router = APIRouter()


# GET /benefits
@benefit_router.get("", response_model=BenefitsRead)
def retrieve_benefits(
    *,
    db_session: DbSession,
):
    """Retrieve all benefits."""
    return get_all_benefit(db_session=db_session)


# GET /benefits/{benefit_id}
@benefit_router.get("/{benefit_id}", response_model=BenefitRead)
def retrieve_benefit(*, db_session: DbSession, benefit_id: int):
    """Retrieve a benefit by id."""
    return get_benefit_by_id(db_session=db_session, benefit_id=benefit_id)


# POST /benefits
@benefit_router.post("", response_model=BenefitRead)
def create(*, benefit_in: BenefitCreate, db_session: DbSession):
    """Creates a new benefit."""
    return create_benefit(db_session=db_session, benefit_in=benefit_in)


# PUT /benefits/{benefit_id}
@benefit_router.put("/{benefit_id}", response_model=BenefitRead)
def update(*, db_session: DbSession, benefit_id: int, benefit_in: BenefitUpdate):
    """Update a benefit by id."""
    return update_benefit(
        db_session=db_session, benefit_id=benefit_id, benefit_in=benefit_in
    )


# DELETE /benefits/{benefit_id}
@benefit_router.delete("/{benefit_id}", response_model=BenefitRead)
def delete(*, db_session: DbSession, benefit_id: int):
    """Delete a benefit by id."""
    return delete_benefit(db_session=db_session, benefit_id=benefit_id)

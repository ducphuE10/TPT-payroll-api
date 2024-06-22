from payroll.exception import AppException, ErrorMessages
from payroll.models import InsurancePolicy
from payroll.insurances import repositories as insurance_repo
from payroll.insurances.repositories import (
    get_insurance_policy_by_id,
    get_insurance_policy_by_code,
)
from payroll.insurances.schemas import (
    InsurancePolicyRead,
    InsurancePolicyCreate,
    InsurancePolicyUpdate,
    InsurancePoliciesRead,
)


def get_one_by_id(*, db_session, id: int) -> InsurancePolicyRead:
    """Returns a position based on the given id."""
    insurance_policy = get_insurance_policy_by_id(db_session=db_session, id=id)

    if not insurance_policy:
        raise AppException(ErrorMessages.ResourceNotFound())

    return InsurancePolicyRead.from_orm(insurance_policy)


def create(
    *, db_session, insurance_policy_in: InsurancePolicyCreate
) -> InsurancePolicy:
    """Creates a new insurance policy."""
    insurance_policy = InsurancePolicy(**insurance_policy_in.model_dump())
    insurance_policy_db = get_insurance_policy_by_code(
        db_session=db_session, code=insurance_policy.code
    )
    if insurance_policy_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    insurance_repo.create(
        db_session=db_session, create_data=insurance_policy_in.model_dump()
    )
    db_session.commit()
    return insurance_policy


def update(
    *, db_session, id: int, insurance_policy_in: InsurancePolicyUpdate
) -> InsurancePolicyRead:
    """Updates a insurance policy with the given data."""
    insurance_policy_db = get_insurance_policy_by_id(db_session=db_session, id=id)

    if not insurance_policy_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = insurance_policy_in.model_dump(exclude_unset=True)

    insurance_repo.update(db_session=db_session, id=id, update_data=update_data)
    db_session.commit()
    return InsurancePolicyRead.from_orm(insurance_policy_db)


def delete(*, db_session, id: int) -> None:
    """Deletes a insurance policy based on the given id."""
    insurance_policy = get_insurance_policy_by_id(db_session=db_session, id=id)
    if not insurance_policy:
        raise AppException(ErrorMessages.ResourceNotFound())
    insurance_repo.delete(db_session=db_session, id=id)
    db_session.commit()


def get_all(*, db_session) -> InsurancePoliciesRead:
    """Returns all insurance policies."""
    data = insurance_repo.get_all(db_session=db_session)
    return InsurancePoliciesRead(data=data)

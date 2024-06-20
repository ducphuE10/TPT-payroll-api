from payroll.exception import AppException, ErrorMessages
from payroll.models import TaxPolicy
from payroll.taxes import repositories as tax_repo
from payroll.taxes.repositories import get_tax_policy_by_id, get_tax_policy_by_code
from payroll.taxes.schemas import (
    TaxPolicyRead,
    TaxPolicyCreate,
    TaxPolicyUpdate,
    TaxpoliciesRead,
)


def get_one_by_id(*, db_session, id: int) -> TaxPolicyRead:
    """Returns a position based on the given id."""
    tax_policy = get_tax_policy_by_id(db_session=db_session, id=id)

    if not tax_policy:
        raise AppException(ErrorMessages.ResourceNotFound())

    return TaxPolicyRead.from_orm(tax_policy)


def create(*, db_session, tax_policy_in: TaxPolicyCreate) -> TaxPolicy:
    """Creates a new tax policy."""
    tax_policy = TaxPolicy(**tax_policy_in.model_dump())
    tax_policy_db = get_tax_policy_by_code(db_session=db_session, code=tax_policy.code)
    if tax_policy_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    tax_repo.create(db_session=db_session, create_data=tax_policy_in.model_dump())
    db_session.commit()
    return tax_policy
    # return TaxPolicyRead.from_orm(tax_policy)


def update(*, db_session, id: int, tax_policy_in: TaxPolicyUpdate) -> TaxPolicyRead:
    """Updates a tax policy with the given data."""
    tax_policy_db = get_tax_policy_by_id(db_session=db_session, id=id)

    if not tax_policy_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = tax_policy_in.model_dump(exclude_unset=True)

    tax_repo.update(db_session=db_session, id=id, update_data=update_data)
    db_session.commit()
    return TaxPolicyRead.from_orm(tax_policy_db)


def delete(*, db_session, id: int) -> None:
    """Deletes a tax policy based on the given id."""
    tax_policy = get_tax_policy_by_id(db_session=db_session, id=id)
    if not tax_policy:
        raise AppException(ErrorMessages.ResourceNotFound())
    tax_repo.delete(db_session=db_session, id=id)
    db_session.commit()


def get_all(*, db_session) -> TaxPolicyRead:
    """Returns all tax policies."""
    data = tax_repo.get_all(db_session=db_session)
    return TaxpoliciesRead(data=data)

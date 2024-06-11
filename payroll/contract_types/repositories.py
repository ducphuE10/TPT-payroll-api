import logging

from payroll.contract_types.schemas import (
    ContractTypeRead,
    ContractTypeCreate,
    ContractTypesRead,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollContractType

log = logging.getLogger(__name__)


def get_contract_type_by_id(*, db_session, id: int) -> ContractTypeRead:
    """Returns a contract type based on the given id."""
    contracttype = (
        db_session.query(PayrollContractType)
        .filter(PayrollContractType.id == id)
        .first()
    )
    return contracttype


def get_contract_type_code(*, db_session, code: str) -> ContractTypeRead:
    """Returns a contract based on the given code."""
    department = (
        db_session.query(PayrollContractType)
        .filter(PayrollContractType.code == code)
        .first()
    )
    return department


def get_all(*, db_session) -> ContractTypesRead:
    """Returns all contract types."""
    data = db_session.query(PayrollContractType).all()
    return ContractTypesRead(data=data)


def get_one_by_id(*, db_session, id: int) -> ContractTypeRead:
    """Returns a contract type based on the given id."""
    contracttype = get_contract_type_by_id(db_session=db_session, id=id)

    if not contracttype:
        raise AppException(ErrorMessages.ResourceNotFound())
    return contracttype


def create(*, db_session, contracttype_in: ContractTypeCreate) -> ContractTypeRead:
    """Creates a new contract type."""
    contracttype = PayrollContractType(**contracttype_in.model_dump())
    contracttype_db = get_contract_type_code(
        db_session=db_session, code=contracttype.code
    )
    if contracttype_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    db_session.add(contracttype)
    db_session.commit()
    return contracttype


def delete(*, db_session, id: int) -> ContractTypeRead:
    """Deletes a contract type based on the given id."""
    query = db_session.query(PayrollContractType).filter(PayrollContractType.id == id)
    contracttype = query.first()

    if not contracttype:
        raise AppException(ErrorMessages.ResourceNotFound())

    db_session.query(PayrollContractType).filter(PayrollContractType.id == id).delete()

    db_session.commit()
    return contracttype

import logging
from fastapi import HTTPException, status

from payroll.contract_types.schemas import (
    ContractTypeRead,
    ContractTypeCreate,
    ContractTypesRead,
)
from payroll.models import PayrollContractType

log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract type not found",
        )
    return contracttype


def create(*, db_session, contracttype_in: ContractTypeCreate) -> ContractTypeRead:
    """Creates a new contract type."""
    contracttype = PayrollContractType(**contracttype_in.model_dump())
    contracttype_db = get_contract_type_code(
        db_session=db_session, code=contracttype.code
    )
    if contracttype_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract type already exists",
        )
    db_session.add(contracttype)
    db_session.commit()
    return contracttype


def delete(*, db_session, id: int) -> ContractTypeRead:
    """Deletes a contract type based on the given id."""
    query = db_session.query(PayrollContractType).filter(PayrollContractType.id == id)
    contracttype = query.first()

    if not contracttype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract type not found",
        )

    db_session.query(PayrollContractType).filter(PayrollContractType.id == id).delete()

    db_session.commit()
    return contracttype

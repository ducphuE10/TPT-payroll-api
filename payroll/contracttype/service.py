import logging
from fastapi import HTTPException, status
from payroll.contracttype.models import (
    PayrollContractType,
    ContractTypeRead,
    ContractTypeCreate,
    ContractTypesRead,
)

log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)


def get_contracttype_by_id(*, db_session, id: int) -> ContractTypeRead:
    """Returns a contracttype based on the given id."""
    contracttype = (
        db_session.query(PayrollContractType)
        .filter(PayrollContractType.id == id)
        .first()
    )
    return contracttype


# def get_by_name(*, db_session, name: str) -> ContractTypeRead:
#     """Returns a contracttype based on the given name."""
#     contracttype = db_session.query(PayrollContractType).filter(PayrollContractType.name == name).first()
#     return contracttype


def get(*, db_session) -> ContractTypesRead:
    """Returns all contracttypes."""
    data = db_session.query(PayrollContractType).all()
    return ContractTypesRead(data=data)


def get_by_id(*, db_session, id: int) -> ContractTypeRead:
    """Returns a contracttype based on the given id."""
    contracttype = get_contracttype_by_id(db_session=db_session, id=id)

    if not contracttype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ContractType not found",
        )
    return contracttype


def get_by_code(*, db_session, code: str) -> ContractTypeRead:
    """Returns a department based on the given code."""
    department = (
        db_session.query(PayrollContractType)
        .filter(PayrollContractType.code == code)
        .first()
    )
    return department


def create(*, db_session, contracttype_in: ContractTypeCreate) -> ContractTypeRead:
    """Creates a new contracttype."""
    contracttype = PayrollContractType(**contracttype_in.model_dump())
    contracttype_db = get_by_code(db_session=db_session, code=contracttype.code)
    if contracttype_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ContractType already exists",
        )
    db_session.add(contracttype)
    db_session.commit()
    return contracttype


# def update(*, db_session, id: int, contracttype_in: ContractTypeUpdate) -> ContractTypeRead:
#     """Updates a contracttype with the given data."""
#     contracttype_db = get_contracttype_by_id(db_session=db_session, id=id)

#     if not contracttype_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ContractType not found",
#         )

#     update_data = contracttype_in.model_dump(exclude_unset=True)

#     db_session.query(PayrollContractType).filter(PayrollContractType.id == id).update(update_data, synchronize_session=False)

#     db_session.commit()
#     return contracttype_db


def delete(*, db_session, id: int) -> ContractTypeRead:
    """Deletes a contracttype based on the given id."""
    query = db_session.query(PayrollContractType).filter(PayrollContractType.id == id)
    contracttype = query.first()

    if not contracttype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ContractType not found",
        )

    db_session.query(PayrollContractType).filter(PayrollContractType.id == id).delete()

    db_session.commit()
    return contracttype

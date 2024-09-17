# from docx import Document
from datetime import date
from payroll.contract_benefit_assocs.schemas import CBAssocsUpdate
from payroll.contracts.repositories import (
    get_contract_by_code,
    get_contract_by_id,
    retrieve_active_contract,
    retrieve_contract_by_code,
)
from typing import List, Optional
from payroll.benefits.schemas import BenefitCreate
from payroll.contracts.schemas import (
    ContractCreate,
    ContractRead,
    ContractUpdate,
    ContractsRead,
)
from payroll.exception import AppException, ErrorMessages
from payroll.models import PayrollContract
from payroll.contracts import repositories as contract_repo

# from payroll.storage.services import read_file_from_minio


def get_one_by_id(*, db_session, id: int) -> ContractRead:
    """Returns a contract based on the given id."""
    contract = get_contract_by_id(db_session=db_session, id=id)

    if not contract:
        raise AppException(ErrorMessages.ResourceNotFound())

    return ContractRead.from_orm(contract)


def get_active_contract(
    *,
    db_session,
    employee_code: str,
    current_date: date,
) -> Optional[PayrollContract]:
    active_contract = retrieve_active_contract(
        db_session=db_session, employee_code=employee_code, current_date=current_date
    )

    return active_contract


def create(*, db_session, contract_in: ContractCreate) -> PayrollContract:
    """Creates a new contract."""
    contract = PayrollContract(**contract_in.model_dump())
    contract_db = get_contract_by_code(db_session=db_session, code=contract.code)
    if contract_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    contract_repo.create(db_session=db_session, create_data=contract_in.model_dump())

    return contract


def create_contract_with_benefits(
    *,
    db_session,
    contract_in: ContractCreate,
    benefits_list_in: Optional[List[BenefitCreate]] = None,
):
    """Creates a new contract with benefits."""
    if bool(get_contract_by_code(db_session=db_session, code=contract_in.code)):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "contract")
    # def create(*, db_session, create_data: dict)
    try:
        contract = create(db_session=db_session, contract_in=contract_in)

        contract = retrieve_contract_by_code(
            db_session=db_session, contract_code=contract_in.code
        )
        contract_with_benefits = None
        if benefits_list_in:
            from payroll.contract_benefit_assocs.services import create_multi_cbassocs

            contract_with_benefits = create_multi_cbassocs(
                db_session=db_session,
                contract_id=contract.id,
                cbassoc_list_in=benefits_list_in,
            )
            return {"contract_in": contract, "benefits_list_in": contract_with_benefits}
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))
    return {"contract_in": contract}


def update(*, db_session, id: int, contract_in: ContractUpdate) -> ContractRead:
    """Updates a contract with the given data."""
    contract_db = get_contract_by_id(db_session=db_session, id=id)

    if not contract_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = contract_in.model_dump(exclude_unset=True)

    try:
        contract_repo.update(db_session=db_session, id=id, update_data=update_data)
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return ContractRead.from_orm(contract_db)


def update_contract_with_benefits(
    *,
    db_session,
    contract_id: int,
    contract_in: Optional[ContractUpdate] = None,
    cbassoc_list_in: Optional[List[CBAssocsUpdate]] = None,
):
    try:
        if contract_in:
            contract = update(
                db_session=db_session, id=contract_id, contract_in=contract_in
            )

        if cbassoc_list_in:
            from payroll.contract_benefit_assocs.services import update_multi_cbassocs

            contract_with_benefits = update_multi_cbassocs(
                db_session=db_session,
                cbassoc_list_in=cbassoc_list_in,
                contract_id=contract.id,
            )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return contract_with_benefits


def delete(*, db_session, id: int) -> None:
    """Deletes a contract based on the given id."""
    contract = get_contract_by_id(db_session=db_session, id=id)
    if not contract:
        raise AppException(ErrorMessages.ResourceNotFound())
    contract_repo.delete(db_session=db_session, id=id)


def get_all(*, db_session) -> ContractsRead:
    """Returns all contracts."""
    data = contract_repo.get_all(db_session=db_session)
    return ContractsRead(data=data)


# def generate_contract_docx(*, db_session, id: int) -> io.BytesIO:
#     """Generate a contract docx file based on the given data and template."""

#     contract_data = get_contract_by_id(db_session=db_session, id=id)

#     if not contract_data:
#         raise AppException(ErrorMessages.ResourceNotFound())

#     template_path = get_contractType_template(
#         db_session=db_session, code=contract_data.type_code
#     )
#     template_stream = read_file_from_minio(template_path)

#     doc = Document(template_stream)

#     # Create a temporary directory to store the generated contract
#     for paragraph in doc.paragraphs:
#         paragraph.text = paragraph.text.replace("{{contract_name}}", contract_data.name)
#         paragraph.text = paragraph.text.replace(
#             "{{employee_name}}", contract_data.employee.name
#         )

#     # Load the template
#     file_stream = io.BytesIO()
#     doc.save(file_stream)
#     file_stream.seek(0)  # Move the pointer to the beginning of the stream

#     return file_stream

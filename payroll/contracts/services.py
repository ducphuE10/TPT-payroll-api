import io
from docx import Document
from payroll.contracts.repositories import (
    get_contract_by_code,
    get_contract_by_id,
    get_contractType_template,
)
from payroll.contracts.schemas import (
    ContractCreate,
    ContractRead,
    ContractUpdate,
    ContractsRead,
)
from payroll.exception import AppException, ErrorMessages
from payroll.models import PayrollContract
from payroll.contracts import repositories as contract_repo
from payroll.storage.services import read_file_from_minio


def get_one_by_id(*, db_session, id: int) -> ContractRead:
    """Returns a contract based on the given id."""
    contract = get_contract_by_id(db_session=db_session, id=id)

    if not contract:
        raise AppException(ErrorMessages.ResourceNotFound())

    return ContractRead.from_orm(contract)


def create(*, db_session, contract_in: ContractCreate) -> PayrollContract:
    """Creates a new contract."""
    contract = PayrollContract(**contract_in.model_dump())
    contract_db = get_contract_by_code(db_session=db_session, code=contract.code)
    if contract_db:
        raise AppException(ErrorMessages.ResourceAlreadyExists())
    contract_repo.create(db_session=db_session, create_data=contract_in.model_dump())
    db_session.commit()
    return contract


def update(*, db_session, id: int, contract_in: ContractUpdate) -> ContractRead:
    """Updates a contract with the given data."""
    contract_db = get_contract_by_id(db_session=db_session, id=id)

    if not contract_db:
        raise AppException(ErrorMessages.ResourceNotFound())

    update_data = contract_in.model_dump(exclude_unset=True)

    contract_repo.update(db_session=db_session, id=id, update_data=update_data)
    return ContractRead.from_orm(contract_db)


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


def generate_contract_docx(*, db_session, id: int) -> io.BytesIO:
    """Generate a contract docx file based on the given data and template."""

    contract_data = get_contract_by_id(db_session=db_session, id=id)

    if not contract_data:
        raise AppException(ErrorMessages.ResourceNotFound())

    template_path = get_contractType_template(
        db_session=db_session, code=contract_data.type_code
    )
    template_stream = read_file_from_minio(template_path)

    doc = Document(template_stream)

    # Create a temporary directory to store the generated contract
    for paragraph in doc.paragraphs:
        paragraph.text = paragraph.text.replace("{{contract_name}}", contract_data.name)
        paragraph.text = paragraph.text.replace(
            "{{employee_name}}", contract_data.employee.name
        )

    # Load the template
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)  # Move the pointer to the beginning of the stream

    return file_stream

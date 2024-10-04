# from docx import Document
from datetime import date

from payroll.contract_histories.repositories import (
    add_contract_history,
    modify_contract_history,
    remove_contract_history,
    retrieve_all_contract_histories,
    retrieve_contract_history_addendum_by_employee_and_period,
    retrieve_contract_history_by_employee_and_period,
    retrieve_contract_history_by_id,
)
from payroll.contract_histories.schemas import (
    ContractHistoryCreate,
    ContractHistoryUpdate,
)
from payroll.exception import AppException, ErrorMessages

# from payroll.storage.services import read_file_from_minio


def check_exist_contract_history_by_id(*, db_session, contract_history_id: int):
    return bool(
        retrieve_contract_history_by_id(
            db_session=db_session, contract_history_id=contract_history_id
        )
    )


def check_exist_contract_history_addendum(
    *, db_session, employee_id: int, from_date: date, to_date: date
):
    return bool(
        retrieve_contract_history_addendum_by_employee_and_period(
            db_session=db_session,
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
        )
    )


def get_contract_history_by_id(*, db_session, contract_history_id: int):
    """Returns a contract based on the given id."""
    if not check_exist_contract_history_by_id(
        db_session=db_session, contract_history_id=contract_history_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "contract history")

    return retrieve_contract_history_by_id(
        db_session=db_session, contract_history_id=contract_history_id
    )


def get_all_contract_histories(*, db_session):
    list_contracts = retrieve_all_contract_histories(db_session=db_session)
    if not list_contracts:
        raise AppException(ErrorMessages.ResourceNotFound(), "contract history")

    return list_contracts


def get_active_contract_history_by_period(
    *, db_session, employee_id: int, from_date: date, to_date: date
):
    active_contract_history = retrieve_contract_history_by_employee_and_period(
        db_session=db_session,
        employee_id=employee_id,
        from_date=from_date,
        to_date=to_date,
    )
    active_contract_history_addendum = (
        retrieve_contract_history_addendum_by_employee_and_period(
            db_session=db_session,
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
        )
    )

    if not (active_contract_history or active_contract_history_addendum):
        raise AppException(ErrorMessages.ResourceNotFound(), "contract history")

    if active_contract_history_addendum:
        return active_contract_history_addendum
    else:
        return active_contract_history


def create_contract_history(*, db_session, contract_history_in: ContractHistoryCreate):
    """Creates a new contract."""
    try:
        contract_history = add_contract_history(
            db_session=db_session, contract_history_in=contract_history_in
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return contract_history


def update_contract_history(
    *, db_session, contract_history_id: int, contract_history_in: ContractHistoryUpdate
):
    """Updates a contract with the given data."""
    if not check_exist_contract_history_by_id(
        db_session=db_session, contract_history_id=contract_history_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "contract history")

    try:
        contract_history = modify_contract_history(
            db_session=db_session,
            contract_history_id=contract_history_id,
            contract_history_in=contract_history_in,
        )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return contract_history


# def update_contract_with_benefits(
#     *,
#     db_session,
#     contract_id: int,
#     contract_in: Optional[ContractUpdate] = None,
#     cbassoc_list_in: Optional[List[CBAssocsUpdate]] = None,
# ):
#     try:
#         if contract_in:
#             contract = update(
#                 db_session=db_session, id=contract_id, contract_in=contract_in
#             )

#         if cbassoc_list_in:
#             from payroll.contract_benefit_assocs.services import update_multi_cbassocs

#             contract_with_benefits = update_multi_cbassocs(
#                 db_session=db_session,
#                 cbassoc_list_in=cbassoc_list_in,
#                 contract_id=contract.id,
#             )
#         db_session.commit()
#     except AppException as e:
#         db_session.rollback()
#         raise AppException(ErrorMessages.ErrSM99999(), str(e))

#     return contract_with_benefits


def delete_contract_history(*, db_session, contract_history_id: int):
    """Deletes a contract based on the given id."""
    if not check_exist_contract_history_by_id(
        db_session=db_session, contract_history_id=contract_history_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "contract history")

    try:
        remove_contract_history(
            db_session=db_session,
            contract_history_id=contract_history_id,
        )
        db_session.commit()
    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return {"message": "Deleted successfully"}


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

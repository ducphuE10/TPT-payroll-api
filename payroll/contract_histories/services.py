# from docx import Document
from datetime import date

from fastapi.responses import StreamingResponse

from payroll.contract_histories.repositories import (
    add_contract_history,
    modify_contract_history,
    remove_contract_history,
    retrieve_all_contract_histories,
    retrieve_contract_history_addendum_by_employee_and_period,
    retrieve_contract_history_addendums_by_employee_and_period,
    retrieve_contract_history_by_employee_and_period,
    retrieve_contract_history_by_id,
)
from payroll.contract_histories.schemas import (
    ContractHistoryCreate,
    ContractHistoryUpdate,
)

from payroll.departments.repositories import retrieve_department_by_id
from payroll.employees.repositories import retrieve_employee_by_id
from payroll.exception import AppException, ErrorMessages
from payroll.utils.functions import fill_template
from payroll.utils.models import ContractHistoryType

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


def get_active_contract_history_detail_by_period(
    *, db_session, employee_id: int, from_date: date, to_date: date
):
    active_contract_history = retrieve_contract_history_by_employee_and_period(
        db_session=db_session,
        employee_id=employee_id,
        from_date=from_date,
        to_date=to_date,
    )
    active_contract_history_addendums = (
        retrieve_contract_history_addendums_by_employee_and_period(
            db_session=db_session,
            employee_id=employee_id,
            from_date=from_date,
            to_date=to_date,
        )
    )

    if not (active_contract_history or active_contract_history_addendums):
        raise AppException(ErrorMessages.ResourceNotFound(), "contract history")

    if active_contract_history_addendums:
        return {
            "contract": active_contract_history,
            "addendums": active_contract_history_addendums,
        }
    else:
        return {"contract": active_contract_history}


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


def generate_contract_docx(*, db_session, id: int):
    """Generate a contract docx file based on the given data and template."""

    contract_data = get_contract_history_by_id(
        db_session=db_session, contract_history_id=id
    )
    employee = retrieve_employee_by_id(
        db_session=db_session, employee_id=contract_data.employee_id
    )

    if not contract_data:
        raise AppException(ErrorMessages.ResourceNotFound())
    if contract_data.contract_type == ContractHistoryType.ADDENDUM:
        template_path = "payroll/utils/file/addendum.docx"

        try:
            data = {
                "contract_id": f"CT_{contract_data.id}_{contract_data.employee_id}",
                "department": retrieve_department_by_id(
                    db_session=db_session, department_id=employee.department_id
                ).name
                or "N/A",  # Handle missing data
                "employee_name": employee.name or "N/A",
                "date_of_birth": (
                    employee.date_of_birth.strftime("%Y-%m-%d")
                    if employee.date_of_birth
                    else "N/A"
                ),
                "gender": employee.gender or "N/A",
                "permenant_addr": employee.permanent_addr or "N/A",
                "cccd": employee.cccd or "N/A",
                "cccd_date": (
                    employee.cccd_date.strftime("%Y-%m-%d")
                    if employee.cccd_date
                    else "N/A"
                ),
                "cccd_place": employee.cccd_place or "N/A",
            }
            # Create a temporary directory to store the generated contract
            file_buffer = fill_template(template_path=template_path, data=data)

        except Exception as e:
            raise Exception(f"Error loading template file: {e}")

        # Load the template
        headers = {
            "Content-Disposition": 'attachment; filename="filled_template.docx"',
            "Content-Encoding": "UTF-8",
        }
    else:
        print("123")
    return StreamingResponse(
        file_buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )

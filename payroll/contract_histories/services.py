# from docx import Document
from datetime import date
import io
import zipfile
from typing import List, Optional

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
from payroll.positions.repositories import retrieve_position_by_id
from payroll.utils.functions import fill_template, format_with_dot
from payroll.utils.models import ContractHistoryType, Gender

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


def retrieve_addendum_data(*, db_session, addendum_id: int):
    contract_data = get_contract_history_by_id(
        db_session=db_session, contract_history_id=addendum_id
    )
    employee = retrieve_employee_by_id(
        db_session=db_session, employee_id=contract_data.employee_id
    )
    data = {
        "contract_id": f"CT_{contract_data.id}_{contract_data.employee_id}",
        "department": retrieve_department_by_id(
            db_session=db_session, department_id=contract_data.department_id
        ).name,
        "position": retrieve_position_by_id(
            db_session=db_session, position_id=contract_data.position_id
        ).name,
        "employee_name": employee.name,
        "date_of_birth": (employee.date_of_birth.strftime("%d-%m-%Y")),
        "gender": "Nam" if employee.gender == Gender.Male else "Nữ",
        "permenant_addr": employee.permanent_addr
        or "........................................",
        "cccd": employee.cccd,
        "cccd_date": (
            employee.cccd_date.strftime("%Y-%m-%d")
            if employee.cccd_date
            else "...................."
        ),
        "cccd_place": employee.cccd_place or "........................................",
        "salary": str(format_with_dot(contract_data.salary)),
        "attendant_benefit": str(format_with_dot(contract_data.attendant_benefit)),
        "transportation_benefit": str(
            format_with_dot(contract_data.transportation_benefit)
        ),
        "housing_benefit": str(format_with_dot(contract_data.housing_benefit)),
        "phone_benefit": str(format_with_dot(contract_data.phone_benefit)),
        "meal_benefit": str(format_with_dot(contract_data.meal_benefit)),
        "toxic_benefit": str(format_with_dot(contract_data.toxic_benefit)),
    }
    return data


def retrieve_contract_data(
    *,
    db_session,
    contract_id: int,
    detail_benefit: Optional[bool] = None,
    detail_insurance: Optional[bool] = None,
):
    contract_data = get_contract_history_by_id(
        db_session=db_session, contract_history_id=contract_id
    )
    employee = retrieve_employee_by_id(
        db_session=db_session, employee_id=contract_data.employee_id
    )
    if detail_benefit:
        benefit = {
            "benefit": f"\n+ Phụ cấp chuyên cần/ Attendant allowance: {str(format_with_dot(contract_data.attendant_benefit))} đ\n+ Phụ cấp đi lại/ Transportation allowance: {str(format_with_dot(contract_data.transportation_benefit))} đ\n+ Phụ cấp nhà ở/ Housing allowance: {str(format_with_dot(contract_data.housing_benefit))} đ\n+ Phụ cấp điện thoại/ Phone allowance: {str(format_with_dot(contract_data.phone_benefit))} đ\n+ Phụ cấp tiền ăn/ Meal allowance: {str(format_with_dot(contract_data.meal_benefit))} đ\n+ Phụ cấp độc hại/ Toxic allowance: {str(format_with_dot(contract_data.toxic_benefit))} đ"
        }
    elif not detail_benefit:
        benefit = {
            "benefit": "theo chính sách chung của Công ty tại từng thời điểm\nAllowance: In accordance with the policy of the Company from time to time."
        }

    data = {
        "contract_id": f"CT_{contract_data.id}_{contract_data.employee_id}",
        "employee_name": employee.name,
        "date_of_birth": (employee.date_of_birth.strftime("%d-%m-%Y")),
        "cccd": employee.cccd,
        "cccd_date": (
            employee.cccd_date.strftime("%Y-%m-%d")
            if employee.cccd_date
            else "...................."
        ),
        "cccd_place": employee.cccd_place or "........................................",
        "permenant_addr": employee.permanent_addr
        or "........................................",
        "mst": employee.mst,
        "position": retrieve_position_by_id(
            db_session=db_session, position_id=contract_data.position_id
        ).name,
        "department": retrieve_department_by_id(
            db_session=db_session, department_id=contract_data.department_id
        ).name,
        "salary": str(format_with_dot(contract_data.salary)),
    }
    data.update(benefit)

    return data


def generate_contract_docx(
    *,
    db_session,
    contract_ids: List[int],
    detail_benefit: Optional[bool] = None,
    detail_insurance: Optional[bool] = None,
):
    """Generate a contract docx file based on the given data and template."""
    generated_contracts = []

    for contract_id in contract_ids:
        try:
            contract_data = get_contract_history_by_id(
                db_session=db_session, contract_history_id=contract_id
            )

            if not contract_data:
                raise AppException(ErrorMessages.ResourceNotFound())

            if contract_data.contract_type == ContractHistoryType.ADDENDUM:
                template_path = "payroll/utils/file/addendum.docx"
                try:
                    data = retrieve_addendum_data(
                        db_session=db_session, addendum_id=contract_id
                    )
                    filename = f"addendum_{data['contract_id']}.docx"
                except Exception as e:
                    raise Exception(f"Error retrieve addendum data: {e}")

            else:
                template_path = "payroll/utils/file/contract.docx"
                try:
                    data = retrieve_contract_data(
                        db_session=db_session,
                        contract_id=contract_id,
                        detail_benefit=detail_benefit,
                        detail_insurance=detail_insurance,
                    )
                    filename = f"contract_{data['contract_id']}.docx"
                except Exception as e:
                    raise Exception(f"Error retrieve contract data: {e}")

            file_buffer = fill_template(template_path=template_path, data=data)

            generated_contracts.append({"buffer": file_buffer, "filename": filename})

        except Exception as e:
            # Log the error or handle it as needed
            print(f"Error generating contract {contract_id}: {e}")

    return generated_contracts


def generate_multi_contracts_docx(
    *,
    db_session,
    contract_ids: List[int],
    detail_benefit: Optional[bool] = None,
    detail_insurance: Optional[bool] = None,
    archive_format: str = "zip",
):
    archive_buffer = io.BytesIO()

    generated_contracts = generate_contract_docx(
        db_session=db_session,
        contract_ids=contract_ids,
        detail_benefit=detail_benefit,
        detail_insurance=detail_insurance,
    )
    if archive_format == "zip":
        with zipfile.ZipFile(archive_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            for contract in generated_contracts:
                archive.writestr(contract["filename"], contract["buffer"].getvalue())

        content_type = "application/zip"
        file_extension = "zip"
    else:
        raise ValueError("Only 'zip' format is supported currently")

    archive_buffer.seek(0)

    headers = {
        "Content-Disposition": f'attachment; filename="contracts.{file_extension}"',
        "Content-Type": content_type,
    }

    return StreamingResponse(
        archive_buffer,
        media_type=content_type,
        headers=headers,
    )

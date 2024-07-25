import logging
from fastapi import File, HTTPException, UploadFile, status
import pandas as pd
from io import BytesIO
from pydantic import ValidationError

from payroll.departments.services import (
    get_department_by_code,
)
from payroll.positions.services import get_position_by_code
from payroll.schedule_details.repositories import (
    add_schedule_detail,
    modify_schedule_detail,
    remove_schedule_detail,
    retrieve_all_schedule_details,
    retrieve_schedule_detail_by_code,
    retrieve_schedule_detail_by_id,
    search_schedule_details_by_partial_name,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.schedule_details.schemas import (
    ScheduleDetailCreate,
)

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_schedule_detail_by_id(*, db_session, schedule_detail_id: int) -> bool:
    """Check if schedule_detail exists in the database."""
    schedule_detail = retrieve_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )
    return schedule_detail is not None


# GET /schedule_details
def get_all_schedule_details(*, db_session):
    """Returns all schedule_details."""
    list_schedule_details = retrieve_all_schedule_details(db_session=db_session)
    if not list_schedule_details["count"]:
        raise AppException(ErrorMessages.ResourceNotFound())
    return list_schedule_details


# GET /schedule_details/{schedule_detail_id}
def get_schedule_detail_by_id(*, db_session, schedule_detail_id: int):
    """Returns a schedule_detail based on the given id."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    schedule_detail = retrieve_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    )
    return schedule_detail


# POST /schedule_details
def create_schedule_detail(*, db_session, schedule_detail_in: ScheduleDetailCreate):
    """Creates a new schedule_detail."""
    # if not check_exist_department_by_id(
    #     db_session=db_session, department_id=schedule_detail_in.department_id
    # ):
    #     raise AppException(ErrorMessages.ResourceNotFound())

    # if not check_exist_position_by_id(
    #     db_session=db_session, position_id=schedule_detail_in.position_id
    # ):
    #     raise AppException(ErrorMessages.ResourceNotFound())

    if check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_in.id
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists())

    schedule_detail = add_schedule_detail(
        db_session=db_session, schedule_detail_in=schedule_detail_in
    )

    return schedule_detail


# PUT /schedule_details/{schedule_detail_id}
def update_schedule_detail(
    *, db_session, schedule_detail_id: int, schedule_detail_in: Schedule_detailUpdate
):
    """Updates a schedule_detail with the given data."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    updated_schedule_detail = modify_schedule_detail(
        db_session=db_session,
        schedule_detail_id=schedule_detail_id,
        schedule_detail_in=schedule_detail_in,
    )
    return updated_schedule_detail


# DELETE /schedule_details/{schedule_detail_id}
def delete_schedule_detail(*, db_session, schedule_detail_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_schedule_detail_by_id(
        db_session=db_session, schedule_detail_id=schedule_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound())
    remove_schedule_detail(db_session=db_session, schedule_detail_id=schedule_detail_id)
    return {"message": "Schedule_detail deleted successfully"}


def create_schedule_detail_by_xlsx(
    *, db_session, schedule_detail_in: Schedule_detailImport
) -> PayrollSchedule_detail:
    """Creates a new schedule_detail."""
    schedule_detail = PayrollSchedule_detail(
        **schedule_detail_in.model_dump(exclude={"department_code", "position_code"})
    )
    schedule_detail_db = retrieve_schedule_detail_by_code(
        db_session=db_session, code=schedule_detail.code
    )
    if schedule_detail_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schedule_detail already exists",
        )
    if schedule_detail_in.department_code:
        department = get_department_by_code(
            db_session=db_session, code=schedule_detail_in.department_code
        )
        schedule_detail.department_id = department.id
    if schedule_detail_in.position_code:
        position = get_position_by_code(
            db_session=db_session, code=schedule_detail_in.position_code
        )
        schedule_detail.position_id = position.id
    db_session.add(schedule_detail)
    db_session.commit()
    return schedule_detail


def update_schedule_detail_by_xlsx(
    *,
    db_session,
    schedule_detail_db: PayrollSchedule_detail,
    schedule_detail_in: Schedule_detailImport,
) -> PayrollSchedule_detail:
    """Updates a schedule_detail with the given data."""

    schedule_detail_data = schedule_detail_db.dict()
    update_data = schedule_detail_in.model_dump(exclude_unset=True)

    for field in schedule_detail_data:
        if field in update_data:
            setattr(schedule_detail_db, field, update_data[field])
    if schedule_detail_in.department_code:
        department = get_department_by_code(
            db_session=db_session, code=schedule_detail_in.department_code
        )
        schedule_detail_db.department = department
    if schedule_detail_in.position_code:
        position = get_position_by_code(
            db_session=db_session, code=schedule_detail_in.position_code
        )
        schedule_detail_db.position = position

    db_session.commit()
    return schedule_detail_db


def upsert_schedule_detail(
    db_session, schedule_detail_in: Schedule_detailImport, update_on_exists: bool
) -> PayrollSchedule_detail:
    """Creates or updates an schedule_detail based on the code."""
    schedule_detail_db = retrieve_schedule_detail_by_code(
        db_session=db_session, code=schedule_detail_in.code
    )
    if schedule_detail_db:
        if not update_on_exists:
            return schedule_detail_db
        # Convert Schedule_detailCreate to Schedule_detailUpdate
        schedule_detail_update = Schedule_detailImport(
            **schedule_detail_in.model_dump(exclude_unset=True)
        )
        # Update existing schedule_detail
        update_schedule_detail_by_xlsx(
            db_session=db_session,
            schedule_detail_db=schedule_detail_db,
            schedule_detail_in=schedule_detail_update,
        )
    else:
        # Create new schedule_detail
        create_schedule_detail_by_xlsx(
            db_session=db_session, schedule_detail_in=schedule_detail_in
        )
    return schedule_detail_db


def uploadXLSX(
    *, db_session, file: UploadFile = File(...), update_on_exists: bool = False
):
    data = BytesIO(file.file.read())
    _data = pd.read_excel(data)

    df = pd.DataFrame(
        _data,
        columns=[
            "Code",
            "Tên",
            "Ngày sinh",
            "Giới tính",
            "Quốc tịch",
            "Dân tộc",
            "Tôn giáo",
            "CCCD",
            "Ngày cấp CCCD",
            "Nơi cấp CCCD",
            "Hộ khẩu thường trú",
            "Địa chỉ thường trú",
            "Địa chỉ tạm trú",
            "Số điện thoại",
            "Trình độ học vấn",
            "Số tài khoản",
            "Tên chủ tài khoản",
            "Tên ngân hàng",
            "Mã số thuế",
            "Số sổ BHXH",
            "Thông tin bảo hiểm y tế",
            "Ngày vào làm",
            "Ghi chú",
            "Mã Phòng ban",
            "Mã Chức vụ",
            "Email",
            "CV",
        ],
    )

    # rename columns
    df.dropna(subset=["Code"], inplace=True)
    df = df.rename(columns={v: k for k, v in IMPORT_EMPLOYEES_EXCEL_MAP.items()})
    df = df.astype(DTYPES_MAP)
    # convert date columns to datetime
    try:
        df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")
        df["cccd_date"] = pd.to_datetime(df["cccd_date"], errors="coerce")
        df["start_work"] = pd.to_datetime(df["start_work"], errors="coerce")
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": [{"msg": str(e)}]},
        )

    # Validate all rows before inserting
    schedule_details_data = []
    errors = []

    for index, row in df.iterrows():
        try:
            if pd.isna(row["code"]):
                log.warn(f"Skipping row {index + 2} due to NaN in 'Code'")
                continue
            schedule_detail_data = row.to_dict()
            schedule_detail = Schedule_detailImport.model_validate(schedule_detail_data)
            schedule_details_data.append(schedule_detail)
        except ValidationError as e:
            errors.append(
                {"row": index + 2, "errors": e.errors()}
            )  # +2 to account for header and 0-indexing
        except TypeError as e:
            errors.append({"row": index + 2, "errors": [{"msg": str(e)}]})

    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors},
        )

    # Insert all valid records into the database
    for schedule_detail_data in schedule_details_data:
        upsert_schedule_detail(
            db_session=db_session,
            schedule_detail_in=schedule_detail_data,
            update_on_exists=update_on_exists,
        )

    return {"message": "Nhân viên đã được thêm thành công từ tệp Excel"}


def search_schedule_detail_by_name(*, db_session, name: str) -> Schedule_detailsRead:
    data = search_schedule_details_by_partial_name(db_session=db_session, name=name)
    return Schedule_detailsRead(data=data)

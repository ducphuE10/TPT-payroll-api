import logging
from fastapi import File, UploadFile
import pandas as pd
from io import BytesIO

# from payroll.attendances.repositories import get_attendance_by_code
from payroll.attendances.repositories import check_exist_attendance
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollAttendance

# from .constant import IMPORT_EMPLOYEES_EXCEL_MAP, DTYPES_MAP

# from pydantic import ValidationError

from payroll.attendances.schemas import (
    AttendanceImport,
)
from payroll.departments.repositories import (
    get_department_by_code,
)

from payroll.positions.repositories import (
    get_position_by_code,
)

log = logging.getLogger(__name__)


def create_attendance_by_xlsx(
    *, db_session, attendance_in: AttendanceImport
) -> PayrollAttendance:
    """Creates a new attendance."""
    attendance = PayrollAttendance(**attendance_in.model_dump())

    attendance_db = check_exist_attendance(
        db_session=db_session, attendance_in=attendance_in
    )

    if attendance_db:
        # raise AppException(ErrorMessages.ResourceNotFound())
        raise AppException(ErrorMessages.ResourceAlreadyExists())

    db_session.add(attendance)
    db_session.commit()
    return attendance


def update_attendance_by_xlsx(
    *, db_session, attendance_db: PayrollAttendance, attendance_in: AttendanceImport
) -> PayrollAttendance:
    """Updates a attendance with the given data."""

    attendance_data = attendance_db.dict()
    update_data = attendance_in.model_dump(exclude_unset=True)

    for field in attendance_data:
        if field in update_data:
            setattr(attendance_db, field, update_data[field])
    if attendance_in.department_code:
        department = get_department_by_code(
            db_session=db_session, code=attendance_in.department_code
        )
        attendance_db.department = department
    if attendance_in.position_code:
        position = get_position_by_code(
            db_session=db_session, code=attendance_in.position_code
        )
        attendance_db.position = position

    db_session.commit()
    return attendance_db


def upsert_attendance(
    db_session, attendance_in: AttendanceImport, update_on_exists: bool
) -> PayrollAttendance:
    """Creates or updates an attendance based on the code."""
    attendance_db = get_attendance_by_code(
        db_session=db_session, code=attendance_in.code
    )
    if attendance_db:
        if not update_on_exists:
            return attendance_db
        # Convert AttendanceCreate to AttendanceUpdate
        attendance_update = AttendanceImport(
            **attendance_in.model_dump(exclude_unset=True)
        )
        # Update existing attendance
        update_attendance_by_xlsx(
            db_session=db_session,
            attendance_db=attendance_db,
            attendance_in=attendance_update,
        )
    else:
        # Create new attendance
        create_attendance_by_xlsx(db_session=db_session, attendance_in=attendance_in)
    return attendance_db


def uploadXLSX(
    *, db_session, file: UploadFile = File(...), update_on_exists: bool = False
):
    _data = BytesIO(file.file.read())
    # _data = pd.read_excel(data)
    # file_path = "/home/minhbn/Workspace/tpt-software-api/payroll/attendances/BẢNG CHẤM CÔNG.xlsx"

    data = pd.read_excel(
        _data, sheet_name="Sheet1", usecols="A:BK", skiprows=2, engine="openpyxl"
    )
    data.fillna(0, inplace=True)
    # for num in range(3, 64, 2):
    #     values = data.iloc[0, num]
    #     data.iloc[0, num + 1] = values

    list_df = [row.tolist() for index, row in data.iterrows()]
    # list_df = list_df[:-2]
    #     return list_df

    # a = import_attendances_data()
    lst = []
    for i in range(3, len(list_df)):
        for j in range(3, len(list_df[i]), 2):
            item = (
                f"{list_df[i][1]} - {list_df[i][2]} - "
                f"{list_df[0][j]} - {list_df[1][j]} - {list_df[2][j]} : "
                f"{list_df[i][j]} - {list_df[1][j + 1]} : {list_df[i][j + 1]}"
            )
            lst.append(item)
            # print(
            #     list_df[i][1],
            #     "-",
            #     list_df[i][2],
            #     "-",
            #     list_df[0][j],
            #     "-",
            #     list_df[1][j],
            #     "-",
            #     list_df[2][j],
            #     ":",
            #     list_df[i][j],
            #     "-",
            #     list_df[1][j + 1],
            #     ":",
            #     list_df[i][j + 1],
            # )
    # df = pd.DataFrame(
    #     _data,
    #     columns=[
    #         "Code",
    #         "Tên",
    #         "Ngày sinh",
    #         "Giới tính",
    #         "Quốc tịch",
    #         "Dân tộc",
    #         "Tôn giáo",
    #         "CCCD",
    #         "Ngày cấp CCCD",
    #         "Nơi cấp CCCD",
    #         "Hộ khẩu thường trú",
    #         "Địa chỉ thường trú",
    #         "Địa chỉ tạm trú",
    #         "Số điện thoại",
    #         "Trình độ học vấn",
    #         "Số tài khoản",
    #         "Tên chủ tài khoản",
    #         "Tên ngân hàng",
    #         "Mã số thuế",
    #         "Số sổ BHXH",
    #         "Thông tin bảo hiểm y tế",
    #         "Ngày vào làm",
    #         "Ghi chú",
    #         "Mã Phòng ban",
    #         "Mã Chức vụ",
    #         "Email",
    #         "CV",
    #     ],
    # )

    # # rename columns
    # df.dropna(subset=["Code"], inplace=True)
    # df = df.rename(columns={v: k for k, v in IMPORT_EMPLOYEES_EXCEL_MAP.items()})
    # df = df.astype(DTYPES_MAP)
    # # convert date columns to datetime
    # try:
    #     df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")
    #     df["cccd_date"] = pd.to_datetime(df["cccd_date"], errors="coerce")
    #     df["start_work"] = pd.to_datetime(df["start_work"], errors="coerce")
    # except (ValueError, TypeError) as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail={"errors": [{"msg": str(e)}]},
    #     )

    # # Validate all rows before inserting
    # attendances_data = []
    # errors = []

    # for index, row in df.iterrows():
    #     try:
    #         if pd.isna(row["code"]):
    #             log.warn(f"Skipping row {index + 2} due to NaN in 'Code'")
    #             continue
    #         attendance_data = row.to_dict()
    #         attendance = AttendanceImport.model_validate(attendance_data)
    #         attendances_data.append(attendance)
    #     except ValidationError as e:
    #         errors.append(
    #             {"row": index + 2, "errors": e.errors()}
    #         )  # +2 to account for header and 0-indexing
    #     except TypeError as e:
    #         errors.append({"row": index + 2, "errors": [{"msg": str(e)}]})

    # if errors:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail={"errors": errors},
    #     )

    # # Insert all valid records into the database
    # for attendance_data in attendances_data:
    #     upsert_attendance(
    #         db_session=db_session,
    #         attendance_in=attendance_data,
    #         update_on_exists=update_on_exists,
    #     )

    # return {"message": "Nhân viên đã được thêm thành công từ tệp Excel"}
    return {"message": lst}

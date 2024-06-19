# import logging
# from fastapi import File, HTTPException, UploadFile, status
# import pandas as pd
# from io import BytesIO

# from payroll.employees.repositories import get_employee_by_code
# from payroll.models import PayrollEmployee
# from .constant import IMPORT_EMPLOYEES_EXCEL_MAP, DTYPES_MAP

# from pydantic import ValidationError

# from payroll.employees.schemas import (
#     EmployeeImport,
# )
# from payroll.departments.repositories import (
#     get_department_by_code,
# )

# from payroll.positions.repositories import (
#     get_position_by_code,
# )

# log = logging.getLogger(__name__)

# InvalidCredentialException = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail=[{"msg": "Could not validate credentials"}],
# )


# def create_employee_by_xlsx(
#     *, db_session, employee_in: EmployeeImport
# ) -> PayrollEmployee:
#     """Creates a new employee."""
#     employee = PayrollEmployee(
#         **employee_in.model_dump(exclude={"department_code", "position_code"})
#     )
#     employee_db = get_employee_by_code(db_session=db_session, code=employee.code)
#     if employee_db:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Employee already exists",
#         )
#     if employee_in.department_code:
#         department = get_department_by_code(
#             db_session=db_session, code=employee_in.department_code
#         )
#         employee.department_id = department.id
#     if employee_in.position_code:
#         position = get_position_by_code(
#             db_session=db_session, code=employee_in.position_code
#         )
#         employee.position_id = position.id
#     db_session.add(employee)
#     db_session.commit()
#     return employee


# def update_employee_by_xlsx(
#     *, db_session, employee_db: PayrollEmployee, employee_in: EmployeeImport
# ) -> PayrollEmployee:
#     """Updates a employee with the given data."""

#     employee_data = employee_db.dict()
#     update_data = employee_in.model_dump(exclude_unset=True)

#     for field in employee_data:
#         if field in update_data:
#             setattr(employee_db, field, update_data[field])
#     if employee_in.department_code:
#         department = get_department_by_code(
#             db_session=db_session, code=employee_in.department_code
#         )
#         employee_db.department = department
#     if employee_in.position_code:
#         position = get_position_by_code(
#             db_session=db_session, code=employee_in.position_code
#         )
#         employee_db.position = position

#     db_session.commit()
#     return employee_db


# def upsert_employee(
#     db_session, employee_in: EmployeeImport, update_on_exists: bool
# ) -> PayrollEmployee:
#     """Creates or updates an employee based on the code."""
#     employee_db = get_employee_by_code(db_session=db_session, code=employee_in.code)
#     if employee_db:
#         if not update_on_exists:
#             return employee_db
#         # Convert EmployeeCreate to EmployeeUpdate
#         employee_update = EmployeeImport(**employee_in.model_dump(exclude_unset=True))
#         # Update existing employee
#         update_employee_by_xlsx(
#             db_session=db_session, employee_db=employee_db, employee_in=employee_update
#         )
#     else:
#         # Create new employee
#         create_employee_by_xlsx(db_session=db_session, employee_in=employee_in)
#     return employee_db


# def uploadXLSX(
#     *, db_session, file: UploadFile = File(...), update_on_exists: bool = False
# ):
#     data = BytesIO(file.file.read())
#     _data = pd.read_excel(data)

#     df = pd.DataFrame(
#         _data,
#         columns=[
#             "Code",
#             "Tên",
#             "Ngày sinh",
#             "Giới tính",
#             "Quốc tịch",
#             "Dân tộc",
#             "Tôn giáo",
#             "CCCD",
#             "Ngày cấp CCCD",
#             "Nơi cấp CCCD",
#             "Hộ khẩu thường trú",
#             "Địa chỉ thường trú",
#             "Địa chỉ tạm trú",
#             "Số điện thoại",
#             "Trình độ học vấn",
#             "Số tài khoản",
#             "Tên chủ tài khoản",
#             "Tên ngân hàng",
#             "Mã số thuế",
#             "Số sổ BHXH",
#             "Thông tin bảo hiểm y tế",
#             "Ngày vào làm",
#             "Ghi chú",
#             "Mã Phòng ban",
#             "Mã Chức vụ",
#             "Email",
#             "CV",
#         ],
#     )

#     # rename columns
#     df.dropna(subset=["Code"], inplace=True)
#     df = df.rename(columns={v: k for k, v in IMPORT_EMPLOYEES_EXCEL_MAP.items()})
#     df = df.astype(DTYPES_MAP)
#     # convert date columns to datetime
#     try:
#         df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")
#         df["cccd_date"] = pd.to_datetime(df["cccd_date"], errors="coerce")
#         df["start_work"] = pd.to_datetime(df["start_work"], errors="coerce")
#     except (ValueError, TypeError) as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail={"errors": [{"msg": str(e)}]},
#         )

#     # Validate all rows before inserting
#     employees_data = []
#     errors = []

#     for index, row in df.iterrows():
#         try:
#             if pd.isna(row["code"]):
#                 log.warn(f"Skipping row {index + 2} due to NaN in 'Code'")
#                 continue
#             employee_data = row.to_dict()
#             employee = EmployeeImport.model_validate(employee_data)
#             employees_data.append(employee)
#         except ValidationError as e:
#             errors.append(
#                 {"row": index + 2, "errors": e.errors()}
#             )  # +2 to account for header and 0-indexing
#         except TypeError as e:
#             errors.append({"row": index + 2, "errors": [{"msg": str(e)}]})

#     if errors:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail={"errors": errors},
#         )

#     # Insert all valid records into the database
#     for employee_data in employees_data:
#         upsert_employee(
#             db_session=db_session,
#             employee_in=employee_data,
#             update_on_exists=update_on_exists,
#         )

#     return {"message": "Nhân viên đã được thêm thành công từ tệp Excel"}

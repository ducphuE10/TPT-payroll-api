import logging
from fastapi import File, HTTPException, UploadFile, status
import pandas as pd
from io import BytesIO

from pydantic import ValidationError

from payroll.employee.models import (
    PayrollEmployee,
    EmployeeRead,
    EmployeeCreate,
    EmployeesRead,
    EmployeeUpdate,
)

log = logging.getLogger(__name__)

InvalidCredentialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
)


def get_employee_by_id(*, db_session, id: int) -> EmployeeRead:
    """Returns a employee based on the given id."""
    employee = (
        db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id).first()
    )
    return employee


def get_by_code(*, db_session, code: str) -> EmployeeRead:
    """Returns a employee based on the given code."""
    employee = (
        db_session.query(PayrollEmployee).filter(PayrollEmployee.code == code).first()
    )
    return employee


def get(*, db_session) -> EmployeesRead:
    """Returns all employees."""
    data = db_session.query(PayrollEmployee).all()
    return EmployeesRead(data=data)


def get_by_id(*, db_session, id: int) -> EmployeeRead:
    """Returns a employee based on the given id."""
    employee = get_employee_by_id(db_session=db_session, id=id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


def create(*, db_session, employee_in: EmployeeCreate) -> EmployeeRead:
    """Creates a new employee."""
    employee = PayrollEmployee(**employee_in.model_dump())
    employee_db = get_by_code(db_session=db_session, code=employee.code)
    if employee_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee already exists",
        )
    db_session.add(employee)
    db_session.commit()
    return employee


def update(*, db_session, id: int, employee_in: EmployeeUpdate) -> EmployeeRead:
    """Updates a employee with the given data."""
    employee_db = get_employee_by_id(db_session=db_session, id=id)

    if not employee_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    update_data = employee_in.model_dump(exclude_unset=True)

    existing_employee = (
        db_session.query(PayrollEmployee)
        .filter(
            PayrollEmployee.code == update_data.get("code"), PayrollEmployee.id != id
        )
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee name already exists",
        )
    db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id).update(
        update_data, synchronize_session=False
    )

    db_session.commit()
    return employee_db


def delete(*, db_session, id: int) -> EmployeeRead:
    """Deletes a employee based on the given id."""
    query = db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id)
    employee = query.first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    db_session.query(PayrollEmployee).filter(PayrollEmployee.id == id).delete()

    db_session.commit()
    return employee


def upsert_employee(db_session, employee_in: EmployeeCreate) -> PayrollEmployee:
    """Creates or updates an employee based on the code."""
    employee_db = get_by_code(db_session=db_session, code=employee_in.code)
    if employee_db:
        # Convert EmployeeCreate to EmployeeUpdate
        employee_update = EmployeeUpdate(**employee_in.model_dump(exclude_unset=True))
        # Update existing employee
        update(db_session=db_session, id=employee_db.id, employee_in=employee_update)
    else:
        # Create new employee
        create(db_session=db_session, employee_in=employee_in)
    return employee_db


def uploadXLSX(*, db_session, file: UploadFile = File(...)):
    try:
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
                "ID Phòng ban",
                "ID Chức vụ",
                "Email",
                "CV",
            ],
        )

        df.dropna(how="all", inplace=True)

        # Validate all rows before inserting
        employees_data = []
        errors = []

        for index, row in df.iterrows():
            try:
                if pd.isna(row["Code"]):
                    print(f"Skipping row {index + 2} due to NaN in 'Code'")
                    continue
                employee_data = {
                    "code": row["Code"],
                    "name": row["Tên"],
                    "date_of_birth": pd.to_datetime(
                        row["Ngày sinh"], errors="coerce"
                    ).date()
                    if pd.notna(row["Ngày sinh"])
                    else None,
                    "gender": row["Giới tính"]
                    if pd.notna(row.get("Giới tính"))
                    else None,
                    "nationality": row["Quốc tịch"]
                    if pd.notna(row.get("Quốc tịch"))
                    else None,
                    "ethnic": row["Dân tộc"] if pd.notna(row.get("Dân tộc")) else None,
                    "religion": row["Tôn giáo"]
                    if pd.notna(row.get("Tôn giáo"))
                    else None,
                    "cccd": str(row["CCCD"]).split(".")[0],
                    "cccd_date": pd.to_datetime(
                        row["Ngày cấp CCCD"], errors="coerce"
                    ).date()
                    if pd.notna(row["Ngày cấp CCCD"])
                    else None,
                    "cccd_place": row["Nơi cấp CCCD"]
                    if pd.notna(row.get("Nơi cấp CCCD"))
                    else None,
                    "domicile": row["Hộ khẩu thường trú"]
                    if pd.notna(row.get("Hộ khẩu thường trú"))
                    else None,
                    "permanent_addr": row.get("Địa chỉ thường trú")
                    if pd.notna(row.get("Địa chỉ thường trú"))
                    else None,
                    "temp_addr": row.get("Địa chỉ tạm trú")
                    if pd.notna(row.get("Địa chỉ tạm trú"))
                    else None,
                    "phone": row["Số điện thoại"]
                    if pd.notna(row.get("Số điện thoại"))
                    else None,
                    "academic_level": row.get("Trình độ học vấn")
                    if pd.notna(row.get("Trình độ học vấn"))
                    else None,
                    "bank_account": str(row["Số tài khoản"]).split(".")[0]
                    if pd.notna(row.get("Số tài khoản"))
                    else None,
                    "bank_holder_name": row["Tên chủ tài khoản"]
                    if pd.notna(row.get("Tên chủ tài khoản"))
                    else None,
                    "bank_name": row["Tên ngân hàng"]
                    if pd.notna(row.get("Tên ngân hàng"))
                    else None,
                    "mst": str(row["Mã số thuế"]).split(".")[0]
                    if pd.notna(row.get("Mã số thuế"))
                    else None,
                    "kcb_number": row.get("Số sổ BHXH")
                    if pd.notna(row.get("Số sổ BHXH"))
                    else None,
                    "hospital_info": row.get("Thông tin bảo hiểm y tế")
                    if pd.notna(row.get("Thông tin bảo hiểm y tế"))
                    else None,
                    "start_work": pd.to_datetime(
                        row.get("Ngày vào làm"), errors="coerce"
                    ).date()
                    if pd.notna(row.get("Ngày vào làm"))
                    else None,
                    "note": row.get("Ghi chú")
                    if pd.notna(row.get("Ghi chú"))
                    else None,
                    "department_id": int(row["ID Phòng ban"])
                    if pd.notna(row["ID Phòng ban"])
                    else None,
                    "position_id": int(row["ID Chức vụ"])
                    if pd.notna(row["ID Chức vụ"])
                    else None,
                    "email": row.get("Email") if pd.notna(row.get("Email")) else None,
                    "cv": row["CV"] if pd.notna(row.get("CV")) else None,
                }
                print(f"Employee data: {employee_data.get('position_id')}")
                employees_data.append(employee_data)
            except ValidationError as e:
                errors.append(
                    {"row": index + 2, "errors": e.errors()}
                )  # +2 to account for header and 0-indexing

        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"errors": errors},
            )

        # Insert all valid records into the database
        for employee_data in employees_data:
            try:
                employee = EmployeeCreate(**employee_data)
                upsert_employee(db_session=db_session, employee_in=employee)
            except ValidationError as e:
                print(f"Validation error during upsert: {e.errors()}")
            except Exception as e:
                print(f"Error during upsert: {str(e)}")

        return {"message": "Employees successfully added from the Excel file"}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file",
        )

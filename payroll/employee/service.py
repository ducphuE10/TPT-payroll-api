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
        # Update existing employee
        update(db_session=db_session, id=employee_db.id, employee_in=employee_in)
    else:
        # Create new employee
        create(db_session=db_session, employee_in=employee_in)
    return employee_db


def uploadXLSX(*, db_session, file: UploadFile = File(...)):
    try:
        data = BytesIO(file.file.read())
        df = pd.read_excel(data)

        # Validate all rows before inserting
        employees_data = []
        errors = []
        for index, row in df.iterrows():
            try:
                employee = PayrollEmployee(
                    code=row["Code"],
                    name=row["Tên"],
                    date_of_birth=pd.to_datetime(
                        row["Ngày sinh"], errors="coerce"
                    ).date()
                    if pd.notna(row["Ngày sinh"])
                    else None,
                    gender=row["Giới tính"],
                    nationality=row["Quốc tịch"],
                    ethnic=row.get("Dân tộc"),
                    religion=row.get("Tôn giáo"),
                    cccd=str(row["CCCD"]).split(".")[0],
                    cccd_date=pd.to_datetime(
                        row["Ngày cấp CCCD"], errors="coerce"
                    ).date()
                    if pd.notna(row["Ngày cấp CCCD"])
                    else None,
                    cccd_place=row["Nơi cấp CCCD"],
                    domicile=row["Hộ khẩu thường trú"],
                    permanent_addr=row.get("Địa chỉ thường trú"),
                    temp_addr=row.get("Địa chỉ tạm trú"),
                    phone=row["Số điện thoại"],
                    academic_level=row.get("Trình độ học vấn"),
                    bank_account=str(row["Số tài khoản"]).split(".")[0],
                    bank_holder_name=row["Tên chủ tài khoản"],
                    bank_name=row["Tên ngân hàng"],
                    mst=str(row["Mã số thuế"]).split(".")[0],
                    kcb_number=row.get("Số sổ BHXH"),
                    hospital_info=row.get("Thông tin bảo hiểm y tế"),
                    start_work=pd.to_datetime(
                        row.get("Ngày vào làm"), errors="coerce"
                    ).date()
                    if pd.notna(row.get("Ngày vào làm"))
                    else None,
                    note=row.get("Ghi chú"),
                    department_id=int(row["ID Phòng ban"])
                    if pd.notna(row["ID Phòng ban"])
                    else None,
                    position_id=int(row["ID Chức vụ"])
                    if pd.notna(row["ID Chức vụ"])
                    else None,
                    email=row.get("Email"),
                    cv=row.get("CV", None),
                )
                employees_data.append(employee)
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
            upsert_employee(db_session, employee_in=employee_data)

        return {"message": "Employees successfully added from the Excel file"}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file",
        )

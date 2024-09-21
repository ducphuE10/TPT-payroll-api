import logging
from fastapi import File, HTTPException, UploadFile, status
import pandas as pd
from io import BytesIO
from pydantic import ValidationError

from payroll.departments.services import (
    check_exist_department_by_id,
    get_department_by_code,
)
from payroll.positions.services import check_exist_position_by_id, get_position_by_code
from payroll.employees.repositories import (
    add_employee,
    modify_employee,
    remove_employee,
    retrieve_all_employees,
    retrieve_employee_by_code,
    retrieve_employee_by_id,
    search_employees_by_partial_name,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollEmployee
from payroll.employees.constant import DTYPES_MAP, IMPORT_EMPLOYEES_EXCEL_MAP
from payroll.employees.schemas import (
    EmployeeCreate,
    EmployeeImport,
    EmployeeUpdate,
    EmployeesRead,
    EmployeesScheduleUpdate,
)
from payroll.schedules.services import check_exist_schedule_by_id
from payroll.utils.functions import (
    check_exist_person_by_cccd,
    check_exist_person_by_mst,
)

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_employee_by_id(*, db_session, employee_id: int):
    """Check if employee exists in the database."""
    return bool(retrieve_employee_by_id(db_session=db_session, employee_id=employee_id))


def check_exist_employee_by_code(*, db_session, employee_code: str):
    """Check if employee exists in the database."""
    return bool(
        retrieve_employee_by_code(db_session=db_session, employee_code=employee_code)
    )


# def check_exist_employee_by_cccd(
#     *, db_session, employee_cccd: str, exclude_employee_id: int = None
# ):
#     """Check if employee exists in the database."""
#     return bool(
#         retrieve_employee_by_cccd(
#             db_session=db_session,
#             employee_cccd=employee_cccd,
#             exclude_employee_id=exclude_employee_id,
#         )
#     )


# def check_exist_employee_by_mst(
#     *, db_session, employee_mst: str, exclude_employee_id: int = None
# ):
#     """Check if employee exists in the database."""
#     return bool(
#         retrieve_employee_by_mst(
#             db_session=db_session,
#             employee_mst=employee_mst,
#             exclude_employee_id=exclude_employee_id,
#         )
#     )


def validate_create_employee(*, db_session, employee_in: EmployeeCreate):
    if not check_exist_department_by_id(
        db_session=db_session, department_id=employee_in.department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "department")

    if not check_exist_position_by_id(
        db_session=db_session, position_id=employee_in.position_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "position")
    if employee_in.schedule_id is not None and not check_exist_schedule_by_id(
        db_session=db_session, schedule_id=employee_in.schedule_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    if check_exist_employee_by_code(
        db_session=db_session, employee_code=employee_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "employee")

    # if check_exist_employee_by_cccd(
    #     db_session=db_session, employee_cccd=employee_in.cccd
    # ):
    #     raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    # if check_exist_employee_by_mst(db_session=db_session, employee_mst=employee_in.mst):
    #     raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    if check_exist_person_by_cccd(db_session=db_session, cccd=employee_in.cccd):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    if check_exist_person_by_mst(db_session=db_session, mst=employee_in.mst):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    return True


def validate_update_employee(
    *, db_session, employee_id: int, employee_in: EmployeeUpdate
):
    if employee_in.department_id is not None and not check_exist_department_by_id(
        db_session=db_session, department_id=employee_in.department_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "department")

    if employee_in.position_id is not None and not check_exist_position_by_id(
        db_session=db_session, position_id=employee_in.position_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "position")

    if employee_in.schedule_id is not None and not check_exist_schedule_by_id(
        db_session=db_session, schedule_id=employee_in.schedule_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "schedule")

    # if employee_in.cccd and check_exist_employee_by_cccd(
    #     db_session=db_session,
    #     employee_cccd=employee_in.cccd,
    #     exclude_employee_id=employee_id,
    # ):
    #     raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    # if employee_in.mst and check_exist_employee_by_mst(
    #     db_session=db_session,
    #     employee_mst=employee_in.mst,
    #     exclude_employee_id=employee_id,
    # ):
    #     raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    if employee_in.cccd and check_exist_person_by_cccd(
        db_session=db_session,
        cccd=employee_in.cccd,
        exclude_id=employee_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    if employee_in.mst and check_exist_person_by_mst(
        db_session=db_session,
        mst=employee_in.mst,
        exclude_id=employee_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    return True


# GET /employees/{employee_id}
def get_employee_by_id(*, db_session, employee_id: int):
    """Returns a employee based on the given id."""
    if not check_exist_employee_by_id(db_session=db_session, employee_id=employee_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")

    return retrieve_employee_by_id(db_session=db_session, employee_id=employee_id)


# GET /employees
def get_all_employees(*, db_session):
    """Returns all employees."""
    list_employees = retrieve_all_employees(db_session=db_session)
    if not list_employees["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")

    return list_employees


# POST /employees
def create_employee(*, db_session, employee_in: EmployeeCreate):
    """Creates a new employee."""
    if validate_create_employee(db_session=db_session, employee_in=employee_in):
        try:
            employee = add_employee(db_session=db_session, employee_in=employee_in)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))
    return employee


def update_multi_employees_schedule(
    *,
    db_session,
    employee_list_in: EmployeesScheduleUpdate,
    schedule_id: int,
):
    employees = []
    count = 0
    list_id = []
    if employee_list_in.apply_all:
        list_id = [
            employee.id
            for employee in retrieve_all_employees(db_session=db_session)["data"]
        ]
    else:
        list_id = [id for id in employee_list_in.list_emp]

    try:
        for employee_id in list_id:
            if not check_exist_employee_by_id(
                db_session=db_session, employee_id=employee_id
            ):
                raise AppException(ErrorMessages.ResourceNotFound(), "employee")
            try:
                employee_in = EmployeeUpdate(schedule_id=schedule_id)
                employee = modify_employee(
                    db_session=db_session,
                    employee_id=employee_id,
                    employee_in=employee_in,
                )

                employees.append(employee)
                count += 1

            except Exception as e:
                db_session.rollback()
                raise AppException(ErrorMessages.ErrSM99999(), str(e))
            db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))
    employees_update = EmployeesRead(count=count, data=employees)

    return {"schedule_id": schedule_id, "data": employees_update}


# PUT /employees/{employee_id}
def update_employee(*, db_session, employee_id: int, employee_in: EmployeeUpdate):
    """Updates a employee with the given data."""
    if not check_exist_employee_by_id(db_session=db_session, employee_id=employee_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")

    if validate_update_employee(
        db_session=db_session, employee_id=employee_id, employee_in=employee_in
    ):
        try:
            employee = modify_employee(
                db_session=db_session, employee_id=employee_id, employee_in=employee_in
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return employee


# DELETE /employees/{employee_id}
def delete_employee(*, db_session, employee_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_employee_by_id(db_session=db_session, employee_id=employee_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "employee")

    try:
        removed_employee = remove_employee(
            db_session=db_session, employee_id=employee_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return removed_employee


def create_employee_by_xlsx(
    *, db_session, employee_in: EmployeeImport
) -> PayrollEmployee:
    """Creates a new employee."""
    employee = PayrollEmployee(
        **employee_in.model_dump(exclude={"department_code", "position_code"})
    )
    employee_db = retrieve_employee_by_code(
        db_session=db_session, employee_code=employee.code
    )
    if employee_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee already exists",
        )
    if employee_in.department_code:
        department = get_department_by_code(
            db_session=db_session, department_code=employee_in.department_code
        )
        employee.department_id = department.id
    if employee_in.position_code:
        position = get_position_by_code(
            db_session=db_session, position_code=employee_in.position_code
        )
        employee.position_id = position.id
    employee.created_by = "admin"
    db_session.add(employee)
    db_session.commit()
    return employee


def update_employee_by_xlsx(
    *, db_session, employee_db: PayrollEmployee, employee_in: EmployeeImport
) -> PayrollEmployee:
    """Updates a employee with the given data."""

    employee_data = employee_db.dict()
    update_data = employee_in.model_dump(exclude_unset=True)

    for field in employee_data:
        if field in update_data:
            setattr(employee_db, field, update_data[field])
    if employee_in.department_code:
        department = get_department_by_code(
            db_session=db_session, code=employee_in.department_code
        )
        employee_db.department = department
    if employee_in.position_code:
        position = get_position_by_code(
            db_session=db_session, code=employee_in.position_code
        )
        employee_db.position = position

    db_session.commit()
    return employee_db


def upsert_employee(
    db_session, employee_in: EmployeeImport, update_on_exists: bool
) -> PayrollEmployee:
    """Creates or updates an employee based on the code."""
    employee_db = retrieve_employee_by_code(
        db_session=db_session, employee_code=employee_in.code
    )
    if employee_db:
        if not update_on_exists:
            return employee_db
        # Convert EmployeeCreate to EmployeeUpdate
        employee_update = EmployeeImport(**employee_in.model_dump(exclude_unset=True))
        # Update existing employee
        update_employee_by_xlsx(
            db_session=db_session, employee_db=employee_db, employee_in=employee_update
        )
    else:
        # Create new employee
        create_employee_by_xlsx(db_session=db_session, employee_in=employee_in)
    return employee_db


def uploadXLSX(
    *, db_session, file: UploadFile = File(...), update_on_exists: bool = False
):
    data = BytesIO(file.file.read())

    _data = pd.read_excel(data)
    df = pd.DataFrame(
        _data,
        columns=list(IMPORT_EMPLOYEES_EXCEL_MAP.values()),
    )

    # rename columns
    df.dropna(subset=["Code"], inplace=True)

    df = df.rename(columns={v: k for k, v in IMPORT_EMPLOYEES_EXCEL_MAP.items()})
    # convert date columns to datetime
    df = df.astype(DTYPES_MAP)

    date_columns = ["date_of_birth", "cccd_date"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Validate all rows before inserting
    employees_data = []
    errors = []

    for index, row in df.iterrows():
        try:
            if pd.isna(row["code"]):
                log.warn(f"Skipping row {index + 2} due to missing 'Code'")
                continue

            employee_data = row.to_dict()
            print(employee_data)
            for key, value in employee_data.items():
                if value == "nan" or value is pd.NaT:
                    employee_data[key] = None

            print("employee_data", employee_data)

            employee = EmployeeImport.model_validate(employee_data)
            employees_data.append(employee)
            print(employee)

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
    print("AAAAAA")
    # Insert all valid records into the database
    for employee_data in employees_data:
        upsert_employee(
            db_session=db_session,
            employee_in=employee_data,
            update_on_exists=update_on_exists,
        )

    return {"message": "Nhân viên đã được thêm thành công từ tệp Excel"}


def search_employee_by_name(*, db_session, name: str) -> PayrollEmployee:
    employees = search_employees_by_partial_name(db_session=db_session, name=name)
    return employees

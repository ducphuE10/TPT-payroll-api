import logging
from fastapi import HTTPException, status
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

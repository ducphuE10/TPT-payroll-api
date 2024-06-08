from fastapi import APIRouter

from payroll.department.models import (
    DepartmentRead,
    DepartmentCreate,
    DepartmentsRead,
    DepartmentUpdate,
)
from payroll.database.core import DbSession
from payroll.department.service import get_by_id, delete, get, create, update

department_router = APIRouter()


@department_router.get("", response_model=DepartmentsRead)
def retrieve_departments(
    *,
    db_session: DbSession,
):
    return get(db_session=db_session)


@department_router.get("/{id}", response_model=DepartmentRead)
def retrieve_department(*, db_session: DbSession, id: int):
    return get_by_id(db_session=db_session, id=id)


@department_router.post("", response_model=DepartmentRead)
def create_department(*, department_in: DepartmentCreate, db_session: DbSession):
    """Creates a new department."""
    department_in.created_by = "admin"
    department = create(db_session=db_session, department_in=department_in)
    return department


@department_router.put("/{id}", response_model=DepartmentRead)
def update_department(
    *, db_session: DbSession, id: int, department_in: DepartmentUpdate
):
    return update(db_session=db_session, id=id, department_in=department_in)


@department_router.delete("/{id}", response_model=DepartmentRead)
def delete_department(*, db_session: DbSession, id: int):
    return delete(db_session=db_session, id=id)

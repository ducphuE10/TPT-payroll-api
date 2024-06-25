from fastapi import APIRouter

from payroll.departments.schemas import (
    DepartmentRead,
    DepartmentCreate,
    DepartmentsRead,
    DepartmentUpdate,
)
from payroll.database.core import DbSession
from payroll.departments.services import (
    create_department,
    delete_department,
    get_all_department,
    get_department_by_id,
    update_department,
)

department_router = APIRouter()


# GET /departments
@department_router.get("", response_model=DepartmentsRead)
def retrieve_departments(
    *,
    db_session: DbSession,
):
    """Retrieve all departments."""
    return get_all_department(db_session=db_session)


# GET /departments/{department_id}
@department_router.get("/{department_id}", response_model=DepartmentRead)
def retrieve_department(*, db_session: DbSession, department_id: int):
    """Retrieve a department by id."""
    return get_department_by_id(db_session=db_session, department_id=department_id)


# POST /departments
@department_router.post("", response_model=DepartmentRead)
def create(*, department_in: DepartmentCreate, db_session: DbSession):
    """Creates a new department."""
    department_in.created_by = "admin"
    department = create_department(db_session=db_session, department_in=department_in)
    return department


# PUT /departments/{department_id}
@department_router.put("/{department_id}", response_model=DepartmentRead)
def update(
    *, db_session: DbSession, department_id: int, department_in: DepartmentUpdate
):
    """Update a department by id."""
    return update_department(
        db_session=db_session, department_id=department_id, department_in=department_in
    )


# DELETE /departments/{department_id}
@department_router.delete("/{department_id}")
def delete(*, db_session: DbSession, department_id: int):
    """Delete a department by id."""
    return delete_department(db_session=db_session, department_id=department_id)

import logging

from payroll.dependants.repositories import (
    add_dependant,
    modify_dependant,
    remove_dependant,
    retrieve_all_dependants,
    retrieve_dependant_by_code,
    retrieve_dependant_by_id,
    search_dependants_by_partial_name,
    retrieve_all_dependants_by_employee_id,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollDependant
from payroll.dependants.schemas import (
    DependantCreate,
    DependantUpdate,
)
from payroll.utils.functions import (
    check_exist_person_by_mst,
)

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_dependant_by_id(*, db_session, dependant_id: int):
    """Check if dependant exists in the database."""
    return bool(
        retrieve_dependant_by_id(db_session=db_session, dependant_id=dependant_id)
    )


def check_exist_dependant_by_code(*, db_session, dependant_code: str):
    """Check if dependant exists in the database."""
    return bool(
        retrieve_dependant_by_code(db_session=db_session, dependant_code=dependant_code)
    )


def validate_create_dependant(*, db_session, dependant_in: DependantCreate):
    if check_exist_dependant_by_code(
        db_session=db_session, dependant_code=dependant_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "dependant")

    if check_exist_person_by_mst(db_session=db_session, mst=dependant_in.mst):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    return True


def validate_update_dependant(
    *, db_session, dependant_id: int, dependant_in: DependantUpdate
):
    if dependant_in.mst and check_exist_person_by_mst(
        db_session=db_session,
        mst=dependant_in.mst,
        exclude_id=dependant_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")
    return True


# GET /dependants/{dependant_id}
def get_dependant_by_id(*, db_session, dependant_id: int):
    """Returns a dependant based on the given id."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    return retrieve_dependant_by_id(db_session=db_session, dependant_id=dependant_id)


# GET /dependants
def get_all_dependants(*, db_session):
    """Returns all dependants."""
    list_dependants = retrieve_all_dependants(db_session=db_session)
    if not list_dependants["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    return list_dependants


def get_all_dependants_by_employee_id(*, db_session, employee_id: int):
    """Returns all dependants."""
    list_dependants = retrieve_all_dependants_by_employee_id(
        db_session=db_session, employee_id=employee_id
    )
    if not list_dependants["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    return list_dependants


# POST /dependants
def create_dependant(*, db_session, dependant_in: DependantCreate):
    """Creates a new dependant."""
    if validate_create_dependant(db_session=db_session, dependant_in=dependant_in):
        try:
            dependant = add_dependant(db_session=db_session, dependant_in=dependant_in)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return dependant


# PUT /dependants/{dependant_id}
def update_dependant(*, db_session, dependant_id: int, dependant_in: DependantUpdate):
    """Updates a dependant with the given data."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    if validate_update_dependant(
        db_session=db_session, dependant_id=dependant_id, dependant_in=dependant_in
    ):
        try:
            dependant = modify_dependant(
                db_session=db_session,
                dependant_id=dependant_id,
                dependant_in=dependant_in,
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return dependant


# DELETE /dependants/{dependant_id}
def delete_dependant(*, db_session, dependant_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependant")

    try:
        removed_dependant = remove_dependant(
            db_session=db_session, dependant_id=dependant_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return removed_dependant


def search_dependant_by_name(*, db_session, name: str) -> PayrollDependant:
    dependants = search_dependants_by_partial_name(db_session=db_session, name=name)
    return dependants

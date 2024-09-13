import logging

from payroll.dependants.repositories import (
    add_dependant,
    modify_dependant,
    remove_dependant,
    retrieve_all_dependants,
    retrieve_dependant_by_cccd,
    retrieve_dependant_by_code,
    retrieve_dependant_by_id,
    retrieve_dependant_by_mst,
    search_dependants_by_partial_name,
    retrieve_all_dependants_by_employee_id,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollDependentPerson
from payroll.dependants.schemas import (
    DependentPersonCreate,
    DependentPersonUpdate,
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


def check_exist_dependant_by_cccd(
    *, db_session, dependant_cccd: str, exclude_dependant_id: int = None
):
    """Check if dependant exists in the database."""
    return bool(
        retrieve_dependant_by_cccd(
            db_session=db_session,
            dependant_cccd=dependant_cccd,
            exclude_dependant_id=exclude_dependant_id,
        )
    )


def check_exist_dependant_by_mst(
    *, db_session, dependant_mst: str, exclude_dependant_id: int = None
):
    """Check if dependant exists in the database."""
    return bool(
        retrieve_dependant_by_mst(
            db_session=db_session,
            dependant_mst=dependant_mst,
            exclude_dependant_id=exclude_dependant_id,
        )
    )


def validate_create_dependant(*, db_session, dependant_in: DependentPersonCreate):
    if check_exist_dependant_by_code(
        db_session=db_session, dependant_code=dependant_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "dependent person")

    if check_exist_dependant_by_cccd(
        db_session=db_session, dependant_cccd=dependant_in.cccd
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    if check_exist_dependant_by_mst(
        db_session=db_session, dependant_mst=dependant_in.mst
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")

    return True


def validate_update_dependant(
    *, db_session, dependant_id: int, dependant_in: DependentPersonUpdate
):
    if dependant_in.cccd and check_exist_dependant_by_cccd(
        db_session=db_session,
        dependant_cccd=dependant_in.cccd,
        exclude_dependant_id=dependant_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    if dependant_in.mst and check_exist_dependant_by_mst(
        db_session=db_session,
        dependant_mst=dependant_in.mst,
        exclude_dependant_id=dependant_id,
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")

    return True


# GET /dependants/{dependant_id}
def get_dependant_by_id(*, db_session, dependant_id: int):
    """Returns a dependant based on the given id."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    return retrieve_dependant_by_id(db_session=db_session, dependant_id=dependant_id)


# GET /dependants
def get_all_dependants(*, db_session):
    """Returns all dependants."""
    list_dependants = retrieve_all_dependants(db_session=db_session)
    if not list_dependants["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    return list_dependants


def get_all_dependants_by_employee_id(*, db_session, employee_id: int):
    """Returns all dependants."""
    list_dependants = retrieve_all_dependants_by_employee_id(
        db_session=db_session, employee_id=employee_id
    )
    if not list_dependants["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    return list_dependants


# POST /dependants
def create_dependant(*, db_session, dependant_in: DependentPersonCreate):
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
def update_dependant(
    *, db_session, dependant_id: int, dependant_in: DependentPersonUpdate
):
    """Updates a dependant with the given data."""
    if not check_exist_dependant_by_id(
        db_session=db_session, dependant_id=dependant_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

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
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    try:
        removed_dependant = remove_dependant(
            db_session=db_session, dependant_id=dependant_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return removed_dependant


def search_dependant_by_name(*, db_session, name: str) -> PayrollDependentPerson:
    dependants = search_dependants_by_partial_name(db_session=db_session, name=name)
    return dependants

import logging

from payroll.dependent_persons.repositories import (
    add_dependent_person,
    modify_dependent_person,
    remove_dependent_person,
    retrieve_all_dependent_persons,
    retrieve_dependent_person_by_cccd,
    retrieve_dependent_person_by_code,
    retrieve_dependent_person_by_id,
    retrieve_dependent_person_by_mst,
    search_dependent_persons_by_partial_name,
    retrieve_all_dependent_persons_by_employee_id,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages
from payroll.models import PayrollDependentPerson
from payroll.dependent_persons.schemas import (
    DependentPersonCreate,
    DependentPersonUpdate,
)

log = logging.getLogger(__name__)

# create, get, update, delete


def check_exist_dependent_person_by_id(*, db_session, dependent_person_id: int):
    """Check if dependent_person exists in the database."""
    return bool(
        retrieve_dependent_person_by_id(
            db_session=db_session, dependent_person_id=dependent_person_id
        )
    )


def check_exist_dependent_person_by_code(*, db_session, dependent_person_code: str):
    """Check if dependent_person exists in the database."""
    return bool(
        retrieve_dependent_person_by_code(
            db_session=db_session, dependent_person_code=dependent_person_code
        )
    )


def check_exist_dependent_person_by_cccd(
    *, db_session, dependent_person_cccd: str, exclude_dependent_person_id: int = None
):
    """Check if dependent_person exists in the database."""
    return bool(
        retrieve_dependent_person_by_cccd(
            db_session=db_session,
            dependent_person_cccd=dependent_person_cccd,
            exclude_dependent_person_id=exclude_dependent_person_id,
        )
    )


def check_exist_dependent_person_by_mst(
    *, db_session, dependent_person_mst: str, exclude_dependent_person_id: int = None
):
    """Check if dependent_person exists in the database."""
    return bool(
        retrieve_dependent_person_by_mst(
            db_session=db_session,
            dependent_person_mst=dependent_person_mst,
            exclude_dependent_person_id=exclude_dependent_person_id,
        )
    )


def validate_create_dependent_person(
    *, db_session, dependent_person_in: DependentPersonCreate
):
    if check_exist_dependent_person_by_code(
        db_session=db_session, dependent_person_code=dependent_person_in.code
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "dependent person")

    if check_exist_dependent_person_by_cccd(
        db_session=db_session, dependent_person_cccd=dependent_person_in.cccd
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    if check_exist_dependent_person_by_mst(
        db_session=db_session, dependent_person_mst=dependent_person_in.mst
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")

    return True


def validate_update_dependent_person(
    *, db_session, dependent_person_in: DependentPersonUpdate
):
    if dependent_person_in.cccd and check_exist_dependent_person_by_cccd(
        db_session=db_session, dependent_person_cccd=dependent_person_in.cccd
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cccd")

    if dependent_person_in.mst and check_exist_dependent_person_by_mst(
        db_session=db_session, dependent_person_mst=dependent_person_in.mst
    ):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "mst")

    return True


# GET /dependent_persons/{dependent_person_id}
def get_dependent_person_by_id(*, db_session, dependent_person_id: int):
    """Returns a dependent_person based on the given id."""
    if not check_exist_dependent_person_by_id(
        db_session=db_session, dependent_person_id=dependent_person_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    return retrieve_dependent_person_by_id(
        db_session=db_session, dependent_person_id=dependent_person_id
    )


# GET /dependent_persons
def get_all_dependent_persons(*, db_session):
    """Returns all dependent_persons."""
    list_dependent_persons = retrieve_all_dependent_persons(db_session=db_session)
    if not list_dependent_persons["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    return list_dependent_persons


def get_all_dependent_persons_by_employee_id(*, db_session, employee_id: int):
    """Returns all dependent_persons."""
    list_dependent_persons = retrieve_all_dependent_persons_by_employee_id(
        db_session=db_session, employee_id=employee_id
    )
    if not list_dependent_persons["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    return list_dependent_persons


# POST /dependent_persons
def create_dependent_person(*, db_session, dependent_person_in: DependentPersonCreate):
    """Creates a new dependent_person."""
    if validate_create_dependent_person(
        db_session=db_session, dependent_person_in=dependent_person_in
    ):
        try:
            dependent_person = add_dependent_person(
                db_session=db_session, dependent_person_in=dependent_person_in
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return dependent_person


# PUT /dependent_persons/{dependent_person_id}
def update_dependent_person(
    *, db_session, dependent_person_id: int, dependent_person_in: DependentPersonUpdate
):
    """Updates a dependent_person with the given data."""
    if not check_exist_dependent_person_by_id(
        db_session=db_session, dependent_person_id=dependent_person_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    if validate_update_dependent_person(
        db_session=db_session, dependent_person_in=dependent_person_in
    ):
        try:
            dependent_person = modify_dependent_person(
                db_session=db_session,
                dependent_person_id=dependent_person_id,
                dependent_person_in=dependent_person_in,
            )
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return dependent_person


# DELETE /dependent_persons/{dependent_person_id}
def delete_dependent_person(*, db_session, dependent_person_id: int):
    """Deletes a attendance based on the given id."""
    if not check_exist_dependent_person_by_id(
        db_session=db_session, dependent_person_id=dependent_person_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "dependent person")

    try:
        removed_dependent_person = remove_dependent_person(
            db_session=db_session, dependent_person_id=dependent_person_id
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return removed_dependent_person


def search_dependent_person_by_name(*, db_session, name: str) -> PayrollDependentPerson:
    dependent_persons = search_dependent_persons_by_partial_name(
        db_session=db_session, name=name
    )
    return dependent_persons

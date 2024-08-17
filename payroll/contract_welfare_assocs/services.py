from payroll.contract_welfare_assocs.repositories import (
    add_cwassoc,
    modify_cwassoc,
    remove_cwassoc,
    retrieve_all_cwassocs,
    retrieve_cwassoc_by_id,
    retrieve_cwassoc_by_information,
)
from payroll.contract_welfare_assocs.schemas import (
    CWAssocCreate,
    CWAssocUpdate,
    CWAssocBase,
)

# from payroll.employees.repositories import retrieve_employee_by_cwassoc
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages


def check_exist_cwassoc_by_id(*, db_session, cwassoc_id: int):
    """Check if cwassoc exists in the database."""
    return bool(retrieve_cwassoc_by_id(db_session=db_session, cwassoc_id=cwassoc_id))


def check_exist_cwassoc_by_information(*, db_session, cwassoc_in: CWAssocBase):
    """Check if cwassoc exists in the database."""
    return bool(
        retrieve_cwassoc_by_information(db_session=db_session, cwassoc_in=cwassoc_in)
    )


# GET /cwassocs/{cwassoc_id}
def get_cwassoc_by_id(*, db_session, cwassoc_id: int):
    """Returns a cwassoc based on the given id."""
    if not check_exist_cwassoc_by_id(db_session=db_session, cwassoc_id=cwassoc_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "cwassoc")

    return retrieve_cwassoc_by_id(db_session=db_session, cwassoc_id=cwassoc_id)


# GET /cwassocs
def get_all_cwassoc(*, db_session):
    """Returns all cwassocs."""
    cwassocs = retrieve_all_cwassocs(db_session=db_session)
    print(cwassocs)
    if not cwassocs["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "cwassoc")

    return cwassocs


# POST /cwassocs
def create_cwassoc(*, db_session, cwassoc_in: CWAssocCreate):
    """Creates a new cwassoc."""
    if check_exist_cwassoc_by_information(db_session=db_session, cwassoc_in=cwassoc_in):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cwassoc")

    try:
        cwassoc = add_cwassoc(db_session=db_session, cwassoc_in=cwassoc_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return cwassoc


# PUT /cwassocs/{cwassoc_id}
def update_cwassoc(*, db_session, cwassoc_id: int, cwassoc_in: CWAssocUpdate):
    """Updates a cwassoc with the given data."""
    if not check_exist_cwassoc_by_id(db_session=db_session, cwassoc_id=cwassoc_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "cwassoc")

    try:
        cwassoc = modify_cwassoc(
            db_session=db_session,
            cwassoc_id=cwassoc_id,
            cwassoc_in=cwassoc_in,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return cwassoc


# DELETE /cwassocs/{cwassoc_id}
def delete_cwassoc(*, db_session, cwassoc_id: int):
    """Deletes a cwassoc based on the given id."""
    if not check_exist_cwassoc_by_id(db_session=db_session, cwassoc_id=cwassoc_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "cwassoc")

    try:
        cwassoc = remove_cwassoc(db_session=db_session, cwassoc_id=cwassoc_id)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return cwassoc

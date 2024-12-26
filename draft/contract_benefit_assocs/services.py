from typing import List
from app.benefits.services import check_exist_benefit_by_id
from app.contract_benefit_assocs.repositories import (
    add_cbassoc,
    add_cbassoc_with_contract_id,
    modify_cbassoc,
    remove_cbassoc,
    retrieve_all_cbassocs,
    retrieve_cbassoc_by_id,
    retrieve_cbassoc_by_information,
    retrieve_cbassocs_by_contract_id,
)
from app.contract_benefit_assocs.schemas import (
    CBAssocCreate,
    CBAssocUpdate,
    CBAssocBase,
    CBAssocsUpdate,
)

# from payroll.employees.repositories import retrieve_employee_by_cbassoc
from app.exception.app_exception import AppException
from app.exception.error_message import ErrorMessages
from app.utils.models import UpdateStatus


def check_exist_cbassoc_by_id(*, db_session, cbassoc_id: int):
    """Check if cbassoc exists in the database."""
    return bool(retrieve_cbassoc_by_id(db_session=db_session, cbassoc_id=cbassoc_id))


def check_exist_cbassoc_by_information(*, db_session, cbassoc_in: CBAssocBase):
    """Check if cbassoc exists in the database."""
    return bool(
        retrieve_cbassoc_by_information(db_session=db_session, cbassoc_in=cbassoc_in)
    )


# GET /cbassocs/{cbassoc_id}
def get_cbassoc_by_id(*, db_session, cbassoc_id: int):
    """Returns a cbassoc based on the given id."""
    if not check_exist_cbassoc_by_id(db_session=db_session, cbassoc_id=cbassoc_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "cbassoc")

    return retrieve_cbassoc_by_id(db_session=db_session, cbassoc_id=cbassoc_id)


# GET /cbassocs
def get_all_cbassoc(*, db_session):
    """Returns all cbassocs."""
    cbassocs = retrieve_all_cbassocs(db_session=db_session)
    if not cbassocs["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "cbassoc")

    return cbassocs


# POST /cbassocs
def create_cbassoc(*, db_session, cbassoc_in: CBAssocCreate):
    """Creates a new cbassoc."""
    if check_exist_cbassoc_by_information(db_session=db_session, cbassoc_in=cbassoc_in):
        raise AppException(ErrorMessages.ResourceAlreadyExists(), "cbassoc")

    try:
        cbassoc = add_cbassoc(db_session=db_session, cbassoc_in=cbassoc_in)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return cbassoc


def create_multi_cbassocs(
    *, db_session, contract_id: int, cbassoc_list_in: List[CBAssocCreate]
):
    try:
        for cbassoc in cbassoc_list_in:
            if not check_exist_benefit_by_id(
                db_session=db_session, benefit_id=cbassoc.benefit_id
            ):
                raise AppException(ErrorMessages.ResourceNotFound(), "benefit")

            cbassoc = add_cbassoc_with_contract_id(
                db_session=db_session, cbassoc_in=cbassoc, contract_id=contract_id
            )
        db_session.commit()

    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return retrieve_cbassocs_by_contract_id(
        db_session=db_session, contract_id=contract_id
    )


# PUT /cbassocs/{cbassoc_id}
def update_cbassoc(*, db_session, cbassoc_id: int, cbassoc_in: CBAssocUpdate):
    """Updates a cbassoc with the given data."""
    if not check_exist_cbassoc_by_id(db_session=db_session, cbassoc_id=cbassoc_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "cbassoc")

    try:
        cbassoc = modify_cbassoc(
            db_session=db_session,
            cbassoc_id=cbassoc_id,
            cbassoc_in=cbassoc_in,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return cbassoc


def update_multi_cbassocs(
    *,
    db_session,
    cbassoc_list_in: List[CBAssocsUpdate],
    contract_id: int,
):
    """Creates multiple schedule_details"""
    try:
        for cbassoc in cbassoc_list_in:
            if (
                not check_exist_cbassoc_by_id(
                    db_session=db_session, cbassoc_id=cbassoc.id
                )
                and cbassoc.status == UpdateStatus.CREATE
            ):
                cbassoc_create = CBAssocCreate(
                    **cbassoc.model_dump(), contract_id=contract_id, exclude={"status"}
                )
                add_cbassoc(db_session=db_session, cbassoc_in=cbassoc_create)

            elif (
                check_exist_benefit_by_id(
                    db_session=db_session, benefit_id=cbassoc.benefit_id
                )
                and cbassoc.status == UpdateStatus.UPDATE
            ):
                cbassoc_update = CBAssocsUpdate(
                    **cbassoc.model_dump(), exclude={"stastus"}
                )
                cbassoc = modify_cbassoc(
                    db_session=db_session,
                    cbassoc_id=cbassoc.id,
                    cbassoc_in=cbassoc_update,
                )

            elif (
                check_exist_benefit_by_id(
                    db_session=db_session, benefit_id=cbassoc.benefit_id
                )
                and cbassoc.status == UpdateStatus.DELETE
            ):
                cbassoc = delete_cbassoc(db_session=db_session, cbassoc_id=cbassoc.id)

        db_session.commit()

    except AppException as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return retrieve_cbassocs_by_contract_id(
        db_session=db_session, contract_id=contract_id
    )


# DELETE /cbassocs/{cbassoc_id}
def delete_cbassoc(*, db_session, cbassoc_id: int):
    """Deletes a cbassoc based on the given id."""
    if not check_exist_cbassoc_by_id(db_session=db_session, cbassoc_id=cbassoc_id):
        raise AppException(ErrorMessages.ResourceNotFound(), "cbassoc")

    try:
        cbassoc = remove_cbassoc(db_session=db_session, cbassoc_id=cbassoc_id)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return cbassoc

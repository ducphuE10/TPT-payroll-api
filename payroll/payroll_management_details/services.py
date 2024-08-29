from payroll.payroll_management_details.repositories import (
    remove_payroll_management_detail,
    retrieve_all_payroll_management_details,
    retrieve_payroll_management_detail_by_id,
)
from payroll.exception.app_exception import AppException
from payroll.exception.error_message import ErrorMessages


def check_exist_payroll_management_detail_by_id(
    *, db_session, payroll_management_detail_id: int
):
    """Check if payroll_management_detail exists in the database."""
    return bool(
        retrieve_payroll_management_detail_by_id(
            db_session=db_session,
            payroll_management_detail_id=payroll_management_detail_id,
        )
    )


# GET /payroll_management_details/{payroll_management_detail_id}
def get_payroll_management_detail_by_id(
    *, db_session, payroll_management_detail_id: int
):
    """Returns a payroll_management_detail based on the given id."""
    if not check_exist_payroll_management_detail_by_id(
        db_session=db_session, payroll_management_detail_id=payroll_management_detail_id
    ):
        raise AppException(ErrorMessages.ResourceNotFound(), "payroll detail")

    return retrieve_payroll_management_detail_by_id(
        db_session=db_session, payroll_management_detail_id=payroll_management_detail_id
    )


# GET /payroll_management_details
def get_all_payroll_management_details(*, db_session):
    """Returns all payroll_management_details."""
    payroll_management_details = retrieve_all_payroll_management_details(
        db_session=db_session
    )
    if not payroll_management_details["count"]:
        raise AppException(ErrorMessages.ResourceNotFound(), "payroll detail")

    return payroll_management_details


# DELETE /payroll_management_details/{payroll_management_detail_id}
def delete_payroll_management_detail(*, db_session, payroll_management_detail_id: int):
    """Deletes a payroll_management_detail based on the given id."""
    if not check_exist_payroll_management_detail_by_id(
        db_session=db_session, payroll_management_detail_id=payroll_management_detail_id
    ):
        raise AppException(
            ErrorMessages.ResourceNotFound(), "payroll_management_detail"
        )

    try:
        payroll_management_detail = remove_payroll_management_detail(
            db_session=db_session,
            payroll_management_detail_id=payroll_management_detail_id,
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise AppException(ErrorMessages.ErrSM99999(), str(e))

    return payroll_management_detail

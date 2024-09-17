from fastapi import Depends
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from jose.exceptions import JWKError
from payroll.config import settings
import logging
from typing import Annotated
from fastapi.security import APIKeyHeader

from payroll.dependants.repositories import (
    retrieve_dependant_by_cccd,
    retrieve_dependant_by_mst,
)
from payroll.employees.repositories import (
    retrieve_employee_by_cccd,
    retrieve_employee_by_mst,
)

logger = logging.getLogger(__name__)


api_key_header = APIKeyHeader(name="Authorization")
TokenDep = Annotated[str, Depends(api_key_header)]


def get_user_email(authorization, **kwargs):
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        logger.exception(
            f"Malformed authorization header. Scheme: {scheme} Param: {param} Authorization: {authorization}"
        )
        return

    token = authorization.split()[1]

    try:
        data = jwt.decode(token, settings.SECRET_KEY.get_secret_value())
    except (JWKError, JWTError):
        raise Exception("Invalid token")
    return data["email"]


def get_error_message_dict():
    return {
        "SYSTEM_EXCEPTION": {"ERR_SM_99999": "System error, please try again later."},
        "APP_EXCEPTION": {
            "ERR_INVALID_INPUT": "Invalid input data.",
            "ERR_RESOURCE_NOT_FOUND": "Resource not found.",
            "ERR_RESOURCE_CONFLICT": "Resource conflict.",
            "ERR_RESOURCE_ALREADY_EXISTS": "Resource already exists.",
            "ERR_FORBIDDEN_ACTION": "Forbidden action.",
            "ERR_USER_WITH_EMAIL_ALREADY_EXISTS": "User with email already exists.",
            "ERR_INVALID_USERNAME_OR_PASSWORD": "Invalid username or password.",
            "ERR_CANNOT_CREATE_ADMIN_USER": "Cannot create admin user.",
            "ERR_EXIST_DEPEND_OBJECT": "Cannot delete due to related object existing.",
            "ERR_WORK_LEAVE_STATE": "Invalid work or leave state.",
        },
    }


def check_exist_person_by_cccd(
    *,
    db_session,
    cccd: str,
    exclude_id: int = None,
):
    employee = retrieve_employee_by_cccd(
        db_session=db_session,
        employee_cccd=cccd,
        exclude_employee_id=exclude_id,
    )
    dependant = retrieve_dependant_by_cccd(
        db_session=db_session,
        dependant_cccd=cccd,
        exclude_dependant_id=exclude_id,
    )
    return bool(employee or dependant)


def check_exist_person_by_mst(
    *,
    db_session,
    mst: str,
    exclude_id: int = None,
):
    employee = retrieve_employee_by_mst(
        db_session=db_session,
        employee_mst=mst,
        exclude_employee_id=exclude_id,
    )
    dependant = retrieve_dependant_by_mst(
        db_session=db_session,
        dependant_mst=mst,
        exclude_dependant_id=exclude_id,
    )
    return bool(employee or dependant)

from fastapi import Depends
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from jose.exceptions import JWKError
from payroll.config import settings
import logging
from typing import Annotated
from fastapi.security import APIKeyHeader

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

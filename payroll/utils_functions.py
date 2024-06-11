from fastapi import HTTPException, status, Depends
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"msg": "Could not validate credentials"}],
        ) from None
    return data["email"]

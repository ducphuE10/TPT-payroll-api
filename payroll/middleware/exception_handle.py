import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from payroll.exception import AppException, SystemException


log = logging.getLogger(__name__)


async def application_error_handler(
    request: Request, exc: AppException
) -> JSONResponse:
    log.error(f"Application error: {exc.code} - {exc.text}")
    return JSONResponse(
        status_code=500,
        content={"error": exc.code, "message": exc.text},
    )


async def system_error_handler(request: Request, exc: SystemException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": exc.code, "message": exc.text},
    )

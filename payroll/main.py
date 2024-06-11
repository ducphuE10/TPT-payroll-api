from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request


from payroll.exception import AppException, SystemException
from payroll.middleware.db_session import create_db_session
from payroll.middleware.exception_handle import (
    application_error_handler,
    system_error_handler,
)
from .logging import configure_logging
from .api import api_router, router
import logging

log = logging.getLogger(__name__)
configure_logging()

app = FastAPI(prefix="/api/v1", title="Payroll API", version="0.1.0")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    await create_db_session(request, call_next)


app.add_exception_handler(SystemException, system_error_handler)
app.add_exception_handler(AppException, application_error_handler)
# we add all API routes to the Web API framework
app.include_router(api_router)
app.include_router(router)

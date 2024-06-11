import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from payroll.database.core import engine, sessionmaker
from payroll.exception import AppException, SystemException
from payroll.middleware.exception_handle import (
    application_error_handler,
    system_error_handler,
)
from .logging import configure_logging
from .api import api_router, router
import logging

log = logging.getLogger(__name__)
configure_logging()

api_version = os.getenv("API_VERSION", "0.1.0")

app = FastAPI(title="Payroll API", version=api_version)


origins = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        session = sessionmaker(bind=engine)
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        request.state.db.close()

    return response


app.add_exception_handler(SystemException, system_error_handler)
app.add_exception_handler(AppException, application_error_handler)
# we add all API routes to the Web API framework
app.include_router(api_router)
app.include_router(router)

import os
import traceback
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, status

from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from payroll.exceptions import PayrollException
from .logging import configure_logging
from .api import api_router, router
from .database.core import engine
import logging

log = logging.getLogger(__name__)
configure_logging()

api_version_prefix = os.getenv("API_VERSION_PREFIX", "/api/v1")
api_version = os.getenv("API_VERSION", "0.1.0")

app = FastAPI(prefix=api_version_prefix, title="Payroll API", version=api_version)


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


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> StreamingResponse:
        try:
            response = await call_next(request)
        except ValueError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "detail": [
                        {"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}
                    ]
                },
            )
        except PayrollException as e:
            log.exception(e)
            response = JSONResponse(
                status_code=(
                    e.status_code
                    if e.status_code is not None
                    else status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                content={
                    "detail": [{"msg": e.msg, "loc": ["Unknown"], "type": "Unknown"}]
                },
            )
        except Exception as e:
            log.exception("Unexpected exception: %s", e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": [{"msg": str(e), "loc": ["Unknown"], "type": "Unknown"}],
                    "traceback": traceback.format_exc(),
                },
            )

        return response


app.add_middleware(ExceptionMiddleware)

# we add all API routes to the Web API framework
app.include_router(api_router)
app.include_router(router)

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
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": [
                        {"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}
                    ]
                },
            )

        return response


app.add_middleware(ExceptionMiddleware)

# we add all API routes to the Web API framework
app.include_router(api_router)
app.include_router(router)

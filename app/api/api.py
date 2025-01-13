from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from app.auth.service import get_current_user
from app.auth.views import auth_router, user_router
from app.api.routes.companies.controllers import company_router
from app.api.routes.departments.controllers import department_router
from app.api.routes.positions.controllers import position_router
from app.api.routes.employees.controllers import employee_router
from app.api.routes.insurances.controllers import insurance_router
from app.api.routes.contract_histories.controllers import contract_history_router
from app.api.routes.shifts.controllers import shift_router
from app.api.routes.schedules.controllers import schedule_router
from app.api.routes.attendances.controllers import attendance_router
from app.api.routes.overtimes.controllers import overtime_router
from app.api.routes.dependants.controllers import dependant_router
from app.api.routes.payroll_managements.controllers import payroll_management_router

from app.core.config import settings

# WARNING: Don't use this unless you want unauthenticated routes
# authenticated_api_router = APIRouter()


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
router = APIRouter(
    prefix=settings.API_VERSION_PREFIX,
    dependencies=[Depends(get_current_user)],  # Enforce authentication here
)

router.include_router(company_router, prefix="/companies", tags=["companies"])
router.include_router(department_router, prefix="/departments", tags=["departments"])
router.include_router(position_router, prefix="/positions", tags=["positions"])
router.include_router(employee_router, prefix="/employees", tags=["employees"])
router.include_router(insurance_router, prefix="/insurances", tags=["insurances"])
router.include_router(
    contract_history_router, prefix="/contract_histories", tags=["contract_histories"]
)
router.include_router(shift_router, prefix="/shifts", tags=["shifts"])
router.include_router(schedule_router, prefix="/schedules", tags=["schedules"])
router.include_router(attendance_router, prefix="/attendances", tags=["attendances"])
router.include_router(overtime_router, prefix="/overtimes", tags=["overtimes"])
router.include_router(dependant_router, prefix="/dependants", tags=["dependants"])
router.include_router(
    payroll_management_router,
    prefix="/payroll_managements",
    tags=["payroll_managements"],
)
# router.include_router(
#     schedule_detail_router, prefix="/schedule_details", tags=["schedule_details"]
# )
# router.include_router(storage_router, prefix="/storage", tags=["storage"])

# router.include_router(
#     addendum_router,
#     prefix="/addendums",
#     tags=["addendums"],
# )
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(
    router,
)

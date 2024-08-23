from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from payroll.auth.service import get_current_user
from payroll.departments.controllers import department_router
from payroll.positions.controllers import position_router
from payroll.contract_types.controllers import contracttype_router
from payroll.employees.controllers import employee_router
from payroll.taxes.controllers import tax_router
from payroll.insurances.controllers import insurance_router
from payroll.contracts.controllers import contract_router
from payroll.attendances.controllers import attendance_router
from payroll.shifts.controllers import shift_router
from payroll.schedules.controllers import schedule_router
from payroll.schedule_details.controllers import schedule_detail_router
from payroll.overtimes.controllers import overtime_router
from payroll.overtime_schedules.controllers import overtime_schedule_router

# from payroll.attendances_management.test3 import import_router
from payroll.config import settings

# WARNING: Don't use this unless you want unauthenticated routes
authenticated_api_router = APIRouter()


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
router = APIRouter(prefix=settings.API_VERSION_PREFIX)

# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
# authenticated_api_router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(department_router, prefix="/departments", tags=["departments"])
router.include_router(position_router, prefix="/positions", tags=["positions"])
router.include_router(employee_router, prefix="/employees", tags=["employees"])
router.include_router(
    contracttype_router, prefix="/contract-types", tags=["contract-types"]
)
router.include_router(tax_router, prefix="/taxes", tags=["taxes"])
router.include_router(insurance_router, prefix="/insurances", tags=["insurances"])
router.include_router(contract_router, prefix="/contracts", tags=["contracts"])
router.include_router(attendance_router, prefix="/attendances", tags=["attendances"])
router.include_router(shift_router, prefix="/shifts", tags=["shifts"])
router.include_router(schedule_router, prefix="/schedules", tags=["schedules"])
router.include_router(
    schedule_detail_router, prefix="/schedule_details", tags=["schedule_details"]
)
router.include_router(overtime_router, prefix="/overtimes", tags=["overtimes"])
router.include_router(
    overtime_schedule_router, prefix="/overtime_schedules", tags=["overtime_schedules"]
)
# router.include_router(import_router, prefix="/import_router", tags=["import_router"])

api_router.include_router(
    authenticated_api_router,
    dependencies=[Depends(get_current_user)],
)

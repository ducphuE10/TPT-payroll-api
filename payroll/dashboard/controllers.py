from fastapi import APIRouter
from payroll.dashboard.services import dashboard_handler

from payroll.database.core import DbSession


dashboard_router = APIRouter()


# GET /departments
@dashboard_router.get("")
def dashboard(*, db_session: DbSession, month: int, year: int):
    """Retrieve all departments."""
    return dashboard_handler(db_session=db_session, month=month, year=year)

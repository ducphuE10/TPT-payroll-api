import logging
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from payroll.config import settings
from .core import Base

from payroll.auth.models import PayrollUser, Role, UserRegister  # noqa
from payroll.models import PayrollDepartment  # noqa
from payroll.models import PayrollPosition  # noqa
from payroll.models import PayrollContractType  # noqa
from payroll.models import PayrollEmployee  # noqa
from payroll.models import PayrollAttendance  # noqa
from payroll.auth.service import get_or_create

log = logging.getLogger(__name__)


def init_database(engine):
    """Initializes the database."""
    if not database_exists(str(settings.SQLALCHEMY_DATABASE_URI)):
        create_database(str(settings.SQLALCHEMY_DATABASE_URI))

    Base.metadata.create_all(engine)

    # Create the default admin user
    admin_user = UserRegister(
        email=settings.SUPERUSER,
        name="Admin",
        role=Role.ADMIN,
        password=settings.SUPERUSER_PASSWORD,
    )

    with Session(engine) as session:
        get_or_create(
            db_session=session,
            user_in=admin_user,
        )

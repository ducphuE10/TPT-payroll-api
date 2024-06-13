"""create employees table

Revision ID: 6efa3f2d2783
Revises: 10be4216259b
Create Date: 2024-06-13 16:02:08.976558

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum

from payroll.utils.models import Gender, Nationality


# revision identifiers, used by Alembic.
revision: str = "6efa3f2d2783"
down_revision: Union[str, None] = "10be4216259b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("code", sa.String(length=10), nullable=False, unique=True),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", Enum(Gender), nullable=False),
        sa.Column("nationality", Enum(Nationality), nullable=True),
        sa.Column("ethnic", sa.String(length=10), nullable=True),
        sa.Column("religion", sa.String(length=30), nullable=True),
        sa.Column("cccd", sa.String(length=30), nullable=False, unique=True),
        sa.Column("cccd_date", sa.Date(), nullable=True),
        sa.Column("cccd_place", sa.String(length=255), nullable=True),
        sa.Column("domicile", sa.String(length=255), nullable=True),
        sa.Column("permanent_addr", sa.String(length=255), nullable=True),
        sa.Column("temp_addr", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("academic_level", sa.String(length=30), nullable=True),
        sa.Column("bank_account", sa.String(length=30), nullable=True),
        sa.Column("bank_holder_name", sa.String(length=30), nullable=True),
        sa.Column("bank_name", sa.String(length=30), nullable=True),
        sa.Column("mst", sa.String(length=30), nullable=False, unique=True),
        sa.Column("kcb_number", sa.String(length=30), nullable=True),
        sa.Column("hospital_info", sa.String(length=255), nullable=True),
        sa.Column("start_work", sa.Date(), nullable=True),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column(
            "department_id",
            sa.Integer(),
            sa.ForeignKey("departments.id"),
            nullable=False,
        ),
        sa.Column(
            "position_id", sa.Integer(), sa.ForeignKey("positions.id"), nullable=False
        ),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("cv", sa.LargeBinary(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("employees")
    op.execute("DROP TYPE gender")
    op.execute("DROP TYPE nationality")
    pass

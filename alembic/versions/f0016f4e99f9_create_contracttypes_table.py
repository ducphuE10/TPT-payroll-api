"""create contracttypes table

Revision ID: f0016f4e99f9
Revises:
Create Date: 2024-06-13 14:17:01.498717

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from payroll.utils.models import InsurancePolicy, TaxPolicy
from sqlalchemy import Enum

# revision identifiers, used by Alembic.
revision: str = "f0016f4e99f9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contracttypes",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("code", sa.String(length=10), nullable=False, unique=True),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("number_of_months", sa.Integer(), nullable=False),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("is_probation", sa.Boolean(), nullable=False),
        sa.Column("tax_policy", Enum(TaxPolicy), nullable=False),
        sa.Column("insurance_policy", Enum(InsurancePolicy), nullable=False),
        sa.Column("template", sa.LargeBinary(), nullable=True),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )
    pass


def downgrade() -> None:
    op.drop_table("contracttypes")
    op.execute("DROP TYPE tax_policy")
    op.execute("DROP TYPE insurance_policy")
    pass

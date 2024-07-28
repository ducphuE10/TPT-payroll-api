"""init database

Revision ID: f9d0ff5c02a9
Revises:
Create Date: 2024-07-26 22:16:25.272007

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f9d0ff5c02a9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "insurance_policies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column(
            "based_on",
            sa.Enum(
                "BasicSalary", "TotalSalary", "CustomByEmployee", name="insurancetype"
            ),
            nullable=False,
        ),
        sa.Column("company_percentage", sa.Float(), nullable=False),
        sa.Column("employee_percentage", sa.Float(), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "positions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "shifts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("standard_work_hours", sa.Float(), nullable=False),
        sa.Column("checkin", sa.Time(), nullable=False),
        sa.Column("earliest_checkin", sa.Time(), nullable=False),
        sa.Column("latest_checkin", sa.Time(), nullable=False),
        sa.Column("checkout", sa.Time(), nullable=False),
        sa.Column("earliest_checkout", sa.Time(), nullable=False),
        sa.Column("latest_checkout", sa.Time(), nullable=False),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "tax_policies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column(
            "tax_type", sa.Enum("Progressive", "Fixed", name="taxtype"), nullable=False
        ),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("percentage", sa.Float(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "contracttypes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("number_of_months", sa.Integer(), nullable=False),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("is_probation", sa.Boolean(), nullable=False),
        sa.Column("tax_policy_id", sa.Integer(), nullable=False),
        sa.Column("insurance_policy_id", sa.Integer(), nullable=False),
        sa.Column("template", sa.LargeBinary(), nullable=True),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["insurance_policy_id"],
            ["insurance_policies.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tax_policy_id"],
            ["tax_policies.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("gender", sa.Enum("Male", "Female", name="gender"), nullable=False),
        sa.Column(
            "nationality", sa.Enum("VN", "JP", name="nationality"), nullable=True
        ),
        sa.Column("ethnic", sa.String(length=10), nullable=True),
        sa.Column("religion", sa.String(length=30), nullable=True),
        sa.Column("cccd", sa.String(length=30), nullable=False),
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
        sa.Column("mst", sa.String(length=30), nullable=False),
        sa.Column("kcb_number", sa.String(length=30), nullable=True),
        sa.Column("hospital_info", sa.String(length=255), nullable=True),
        sa.Column("start_work", sa.Date(), nullable=True),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("position_id", sa.Integer(), nullable=False),
        sa.Column("schedule_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("cv", sa.LargeBinary(), nullable=True),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.ForeignKeyConstraint(
            ["position_id"],
            ["positions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedules.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cccd"),
        sa.UniqueConstraint("code"),
        sa.UniqueConstraint("mst"),
    )
    op.create_table(
        "schedule_details",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("schedule_id", sa.Integer(), nullable=False),
        sa.Column("shift_id", sa.Integer(), nullable=False),
        sa.Column(
            "day",
            sa.Enum("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", name="day"),
            nullable=False,
        ),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedules.id"],
        ),
        sa.ForeignKeyConstraint(
            ["shift_id"],
            ["shifts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "schedule_id", "shift_id", "day", name="uq_schedule_shift_day"
        ),
    )
    op.create_table(
        "attendances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("check_time", sa.Time(), nullable=False),
        sa.Column("day_attendance", sa.Date(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contracts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "INACTIVE", "PENDING", "DELETED", name="status"),
            nullable=False,
        ),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("type_code", sa.String(length=10), nullable=False),
        sa.Column("ct_date", sa.Date(), nullable=False),
        sa.Column("ct_code", sa.String(length=30), nullable=False),
        sa.Column("employee_code", sa.String(length=10), nullable=False),
        sa.Column("signed_date", sa.Date(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("active_from", sa.Date(), nullable=False),
        sa.Column(
            "payment_method",
            sa.Enum("CASH", "BANK", name="paymentmethod"),
            nullable=False,
        ),
        sa.Column("attachments", sa.String(length=255), nullable=True),
        sa.Column("salary", sa.Float(), nullable=False),
        sa.Column("basic_salary", sa.Float(), nullable=False),
        sa.Column("created_by", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["employee_code"],
            ["employees.code"],
        ),
        sa.ForeignKeyConstraint(
            ["type_code"],
            ["contracttypes.code"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("contracts")
    op.drop_table("attendances")
    op.drop_table("schedule_details")
    op.drop_table("employees")
    op.drop_table("contracttypes")
    op.drop_table("tax_policies")
    op.drop_table("shifts")
    op.drop_table("schedules")
    op.drop_table("positions")
    op.drop_table("insurance_policies")
    op.drop_table("departments")
    op.execute("DROP TYPE insurancetype")
    op.execute("DROP TYPE taxtype")
    op.execute("DROP TYPE gender")
    op.execute("DROP TYPE nationality")
    op.execute("DROP TYPE day")
    op.execute("DROP TYPE status")
    op.execute("DROP TYPE paymentmethod")
    # ### end Alembic commands ###

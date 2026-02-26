"""initial schema

Revision ID: 20260225_01
Revises:
Create Date: 2026-02-25 22:20:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260225_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = postgresql.ENUM("admin", "loan_officer", "customer", name="user_role", create_type=False)
    loan_status = postgresql.ENUM("pending", "approved", "rejected", "disbursed", "closed", name="loan_status", create_type=False)
    payment_status = postgresql.ENUM("completed", "pending", name="payment_status", create_type=False)

    user_role.create(op.get_bind(), checkfirst=True)
    loan_status.create(op.get_bind(), checkfirst=True)
    payment_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("role", user_role, nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "loan_products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("interest_rate", sa.Numeric(5, 2), nullable=False),
        sa.Column("max_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("tenure_months", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
    )
    op.create_index("ix_loan_products_id", "loan_products", ["id"])

    op.create_table(
        "loan_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("loan_products.id"), nullable=False),
        sa.Column("requested_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("approved_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", loan_status, nullable=False),
        sa.Column("processed_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
    )
    op.create_index("ix_loan_applications_id", "loan_applications", ["id"])

    op.create_table(
        "repayments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("loan_application_id", sa.Integer(), sa.ForeignKey("loan_applications.id"), nullable=False),
        sa.Column("amount_paid", sa.Numeric(12, 2), nullable=False),
        sa.Column("payment_date", sa.Date(), nullable=False),
        sa.Column("payment_status", payment_status, nullable=False),
    )
    op.create_index("ix_repayments_id", "repayments", ["id"])


def downgrade() -> None:
    op.drop_index("ix_repayments_id", table_name="repayments")
    op.drop_table("repayments")

    op.drop_index("ix_loan_applications_id", table_name="loan_applications")
    op.drop_table("loan_applications")

    op.drop_index("ix_loan_products_id", table_name="loan_products")
    op.drop_table("loan_products")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")

    payment_status = postgresql.ENUM("completed", "pending", name="payment_status")
    loan_status = postgresql.ENUM("pending", "approved", "rejected", "disbursed", "closed", name="loan_status")
    user_role = postgresql.ENUM("admin", "loan_officer", "customer", name="user_role")

    payment_status.drop(op.get_bind(), checkfirst=True)
    loan_status.drop(op.get_bind(), checkfirst=True)
    user_role.drop(op.get_bind(), checkfirst=True)

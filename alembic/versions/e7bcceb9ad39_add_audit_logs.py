"""add audit logs

Revision ID: e7bcceb9ad39
Revises: 8a7167c52830
Create Date: 2026-09-05
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e7bcceb9ad39"
down_revision: Union[str, None] = "8a7167c52830"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    audit_action = sa.Enum(
        "REGISTERED",
        "LOGIN_SUCCEEDED",
        "LOGIN_FAILED",
        "LOGOUT",
        "SESSION_CREATED",
        "SESSION_REFRESHED",
        "SESSION_REVOKED",
        "SESSION_EXPIRED",
        "UPLOAD_CREATED",
        "UPLOAD_DELETED",
        "ANALYSIS_REQUESTED",
        "ANALYSIS_STARTED",
        "ANALYSIS_COMPLETED",
        "ANALYSIS_FAILED",
        "AI_RESULT_GENERATED",
        "ACCOUNT_UPDATED",
        "ACCOUNT_DELETED",
        "ACCESS_DENIED",
        name="audit_action",
    )

    audit_resource_type = sa.Enum(
        "USER",
        "SESSION",
        "UPLOAD",
        "ANALYSIS",
        name="audit_resource_type",
    )

    audit_action.create(op.get_bind(), checkfirst=True)
    audit_resource_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "audit_logs",
        sa.Column("actor_user_id", sa.UUID(), nullable=True),
        sa.Column(
            "action",
            audit_action,
            nullable=False,
        ),
        sa.Column(
            "resource_type",
            audit_resource_type,
            nullable=False,
        ),
        sa.Column("resource_id", sa.UUID(), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["actor_user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_audit_logs_actor_user_id",
        "audit_logs",
        ["actor_user_id"],
        unique=False,
    )

    op.create_index(
        "ix_audit_logs_resource_id",
        "audit_logs",
        ["resource_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_audit_logs_resource_id",
        table_name="audit_logs",
    )

    op.drop_index(
        "ix_audit_logs_actor_user_id",
        table_name="audit_logs",
    )

    op.drop_table("audit_logs")

    sa.Enum(
        name="audit_resource_type",
    ).drop(op.get_bind(), checkfirst=True)

    sa.Enum(
        name="audit_action",
    ).drop(op.get_bind(), checkfirst=True)
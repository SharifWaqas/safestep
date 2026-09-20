"""create initial schema and add safe risk level"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c4b6c8e1d4ca"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    risk_level = sa.Enum(
        "LOW",
        "MEDIUM",
        "HIGH",
        "VERY_HIGH",
        name="risk_level",
    )

    risk_factor = sa.Enum(
        "URGENCY_LANGUAGE",
        "THREAT_LANGUAGE",
        "CREDENTIAL_REQUEST",
        "FINANCIAL_REQUEST",
        "SUSPICIOUS_LINK",
        "SUSPICIOUS_DOMAIN",
        "BRAND_IMPERSONATION",
        "UNKNOWN_SENDER",
        "LOGIN_FORM",
        "PAYMENT_REQUEST",
        "REWARD_LANGUAGE",
        "UNREALISTIC_PRICE",
        name="risk_factor",
    )

    analysis_status = sa.Enum(
        "PENDING",
        "PROCESSING",
        "COMPLETED",
        "FAILED",
        name="analysis_status",
    )

    risk_level.create(bind, checkfirst=True)
    risk_factor.create(bind, checkfirst=True)
    analysis_status.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("full_name", sa.String(length=50), nullable=False),
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "sessions",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("refresh_token_hash", sa.Text(), nullable=False),
        sa.Column(
            "ip_address",
            postgresql.INET(),
            nullable=True,
        ),
        sa.Column(
            "device_info",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
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
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "uploads",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("storage_path", sa.Text(), nullable=False),
        sa.Column("file_name", sa.Text(), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.Text(), nullable=False),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
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
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "analyses",
        sa.Column("upload_id", sa.UUID(), nullable=False),
        sa.Column(
            "status",
            analysis_status,
            nullable=False,
            server_default="PENDING",
        ),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
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
            ["upload_id"],
            ["uploads.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "ai_results",
        sa.Column("analysis_id", sa.UUID(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("guidance", sa.Text(), nullable=False),
        sa.Column("reassurance", sa.Text(), nullable=False),
        sa.Column(
            "risk_level",
            risk_level,
            nullable=False,
        ),
        sa.Column(
            "confidence",
            sa.Numeric(precision=4, scale=3),
            nullable=False,
        ),
        sa.Column(
            "model_name",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column(
            "prompt_tokens",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "completion_tokens",
            sa.Integer(),
            nullable=True,
        ),
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
            ["analysis_id"],
            ["analyses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "analysis_id",
            name="uq_ai_results_analysis_id",
        ),
    )

    op.create_table(
        "risk_scores",
        sa.Column("analysis_id", sa.UUID(), nullable=False),
        sa.Column(
            "risk_factor",
            risk_factor,
            nullable=False,
        ),
        sa.Column(
            "score",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
        ),
        sa.Column(
            "explanation",
            sa.Text(),
            nullable=False,
        ),
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
            ["analysis_id"],
            ["analyses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute(
        "ALTER TYPE risk_level ADD VALUE 'SAFE' BEFORE 'LOW';"
    )


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_table("risk_scores")
    op.drop_table("ai_results")
    op.drop_table("analyses")
    op.drop_table("sessions")
    op.drop_table("uploads")
    op.drop_table("users")

    sa.Enum(name="analysis_status").drop(
        bind,
        checkfirst=True,
    )
    sa.Enum(name="risk_factor").drop(
        bind,
        checkfirst=True,
    )
    sa.Enum(name="risk_level").drop(
        bind,
        checkfirst=True,
    )
"""initial schema"""
from alembic import op
import sqlalchemy as sa
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("workflows", sa.Column("workflow_id", sa.String(64), primary_key=True), sa.Column("request_id", sa.String(64), nullable=False, unique=True), sa.Column("trace_id", sa.String(64), nullable=False), sa.Column("scenario", sa.String(64), nullable=False), sa.Column("state", sa.String(32), nullable=False), sa.Column("decision", sa.String(32), nullable=True), sa.Column("payload_json", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("approvals", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("workflow_id", sa.String(64), nullable=False, index=True), sa.Column("approval_id", sa.String(64), nullable=False, unique=True), sa.Column("role", sa.String(64), nullable=False), sa.Column("approver_id", sa.String(64), nullable=False), sa.Column("decision", sa.String(32), nullable=False), sa.Column("comment", sa.Text(), nullable=False), sa.Column("evidence_json", sa.Text(), nullable=False), sa.Column("request_version", sa.Integer(), nullable=False), sa.Column("candidate_version", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("audit_events", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("event_id", sa.String(64), nullable=False, unique=True), sa.Column("workflow_id", sa.String(64), nullable=True, index=True), sa.Column("trace_id", sa.String(64), nullable=False, index=True), sa.Column("event_type", sa.String(100), nullable=False), sa.Column("payload_json", sa.Text(), nullable=False), sa.Column("previous_hash", sa.String(64), nullable=False), sa.Column("event_hash", sa.String(64), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("kill_switches", sa.Column("name", sa.String(80), primary_key=True), sa.Column("enabled", sa.Boolean(), nullable=False), sa.Column("reason", sa.Text(), nullable=False), sa.Column("updated_by", sa.String(80), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))

def downgrade() -> None:
    op.drop_table("kill_switches")
    op.drop_table("audit_events")
    op.drop_table("approvals")
    op.drop_table("workflows")

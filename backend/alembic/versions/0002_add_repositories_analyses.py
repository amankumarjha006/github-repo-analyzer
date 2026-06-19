"""add repositories and analyses tables

Revision ID: 0002
Revises: e240a112beeb
Create Date: 2026-06-19 11:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = 'e240a112beeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create repositories table
    op.create_table(
        'repositories',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('github_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('owner', sa.String(length=255), nullable=False),
        sa.Column('github_url', sa.String(length=512), nullable=False),
        sa.Column('description', sa.String(length=1024), nullable=True),
        sa.Column('stars_count', sa.Integer(), nullable=False),
        sa.Column('forks_count', sa.Integer(), nullable=False),
        sa.Column('open_issues_count', sa.Integer(), nullable=False),
        # Missing columns added here
        sa.Column('full_name', sa.String(length=300), nullable=False),
        sa.Column('primary_language', sa.String(length=100), nullable=True),
        sa.Column('watchers_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('size_kb', sa.Integer(), nullable=True),
        sa.Column('is_private', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_fork', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('default_branch', sa.String(length=100), nullable=False, server_default='main'),
        sa.Column('license_name', sa.String(length=100), nullable=True),
        sa.Column('homepage_url', sa.Text(), nullable=True),
        sa.Column('last_pushed_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_on_github', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('last_fetched_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('topics', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('github_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # Indexes for repositories
    op.create_index('idx_repos_github_id', 'repositories', ['github_id'])
    op.create_index('idx_repos_full_name', 'repositories', ['full_name'])
    op.create_index(op.f('ix_repositories_user_id'), 'repositories', ['user_id'], unique=False)

    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('repo_id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('error_message', sa.String(length=1024), nullable=True),
        # AI & Metrics columns added here
        sa.Column('progress', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('current_step', sa.String(length=100), nullable=True),
        sa.Column('tech_stack', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('folder_structure', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('architecture_summary', sa.Text(), nullable=True),
        sa.Column('project_type', sa.String(length=100), nullable=True),
        sa.Column('quality_score', sa.Integer(), nullable=True),
        sa.Column('security_score', sa.Integer(), nullable=True),
        sa.Column('documentation_score', sa.Integer(), nullable=True),
        sa.Column('complexity_score', sa.Integer(), nullable=True),
        sa.Column('files_analyzed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_files', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('lines_of_code', sa.Integer(), nullable=True),
        sa.Column('embedding_status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('embedding_chunks', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('started_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('completed_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['repo_id'], ['repositories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # Indexes for analyses
    op.create_index('ix_analyses_repo_id', 'analyses', ['repo_id'], unique=False)
    op.create_index(op.f('ix_analyses_status'), 'analyses', ['status'], unique=False)
    op.create_index(op.f('ix_analyses_user_id'), 'analyses', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop analyses table & indexes first (dependent)
    op.drop_index(op.f('ix_analyses_user_id'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_status'), table_name='analyses')
    op.drop_index('ix_analyses_repo_id', table_name='analyses')
    op.drop_table('analyses')

    # Drop repositories table & indexes
    op.drop_index(op.f('ix_repositories_user_id'), table_name='repositories')
    op.drop_index('idx_repos_full_name', table_name='repositories')
    op.drop_index('idx_repos_github_id', table_name='repositories')
    op.drop_table('repositories')

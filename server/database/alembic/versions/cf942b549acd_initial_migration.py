"""initial_migration

Revision ID: cf942b549acd
Revises: 
Create Date: 2023-11-06 23:45:50.862972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Integer

# revision identifiers, used by Alembic.
revision: str = 'cf942b549acd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'docify_users',
        sa.Column('id', sa.String(100), primary_key=True, index=True),
        sa.Column('username', sa.String(50)),
        sa.Column('email', sa.String(100)),
        sa.Column('img_url', sa.String(200)),
        sa.Column('credits', sa.Integer),
    )
    op.create_table(
        'docify_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(100), sa.ForeignKey('docify_users.id')),
        sa.Column('filename', sa.String(100)),
        sa.Column('file_download_link', sa.String(200)),
        sa.Column('gen_time', sa.DateTime)
    )


def downgrade() -> None:
    pass

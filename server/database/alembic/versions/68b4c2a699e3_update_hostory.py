"""update_hostory

Revision ID: 68b4c2a699e3
Revises: cf942b549acd
Create Date: 2023-11-22 00:14:29.029337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68b4c2a699e3'
down_revision: Union[str, None] = 'cf942b549acd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'docify_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(100), sa.ForeignKey('docify_users.id')),
        sa.Column('filename', sa.String(100)),
        # sa.Column('file_download_link', sa.String(200)),
        sa.Column('gen_time', sa.DateTime)
    )


def downgrade() -> None:
    pass

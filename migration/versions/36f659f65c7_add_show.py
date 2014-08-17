"""add show

Revision ID: 36f659f65c7
Revises: None
Create Date: 2013-08-25 21:26:14.813041

"""

# revision identifiers, used by Alembic.
revision = '36f659f65c7'
down_revision = '212bfc51b4ed'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('like',
                  sa.Column('username', sa.VARCHAR(255),
                  server_default='', nullable=False, index=True))
    op.add_column('follow',
                  sa.Column('username', sa.VARCHAR(255),
                  server_default='', nullable=False, index=True))


def downgrade():
    op.drop_column('like', 'username')
    op.drop_column('follow', 'username')

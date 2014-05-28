"""add like author

Revision ID: 4fd4921279ab
Revises: 2ccbe42daecb
Create Date: 2013-10-08 22:03:07.186066

"""

# revision identifiers, used by Alembic.
revision = '4fd4921279ab'
down_revision = '2ccbe42daecb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('like',
                  sa.Column('media_username', sa.VARCHAR(255),
                  server_default='', nullable=False, index=True))


def downgrade():
    op.drop_column('like', 'media_username')

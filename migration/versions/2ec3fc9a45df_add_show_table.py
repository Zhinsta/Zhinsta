"""add show table

Revision ID: 2ec3fc9a45df
Revises: 36f659f65c7
Create Date: 2013-09-01 20:23:06.089159

"""

# revision identifiers, used by Alembic.
revision = '2ec3fc9a45df'
down_revision = '36f659f65c7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('show',
                    sa.Column('mid', sa.VARCHAR(128), primary_key=True),
                    sa.Column('pic', sa.VARCHAR(255), index=True,
                              nullable=False),
                    sa.Column('user_pic', sa.VARCHAR(255), index=True,
                              nullable=False),
                    sa.Column('ukey', sa.VARCHAR(128), index=True,
                              nullable=False),
                    sa.Column('username', sa.VARCHAR(255), index=True,
                              nullable=False),
                    sa.Column('date_created', sa.DateTime(), index=True,
                              nullable=False),
                    sa.Column('showable', sa.Integer(), index=True,
                              nullable=False, server_default='0'))


def downgrade():
    op.drop_table('show')

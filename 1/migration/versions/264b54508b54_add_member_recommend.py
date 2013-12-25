"""add member recommend

Revision ID: 264b54508b54
Revises: 4fd4921279ab
Create Date: 2013-12-25 21:07:23.800655

"""

# revision identifiers, used by Alembic.
revision = '264b54508b54'
down_revision = '4fd4921279ab'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('recommend',
                    sa.Column('ukey', sa.VARCHAR(128), primary_key=True),
                    sa.Column('pic', sa.VARCHAR(255), nullable=False),
                    sa.Column('username', sa.VARCHAR(255), index=True,
                              nullable=False),
                    sa.Column('order', sa.Integer(), index=True,
                              nullable=False))


def downgrade():
    op.drop_table('recommend')

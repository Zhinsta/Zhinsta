"""add admin table

Revision ID: 1c694f620b6
Revises: 37da297d7473
Create Date: 2014-06-23 17:03:19.469727

"""

# revision identifiers, used by Alembic.
revision = '1c694f620b6'
down_revision = '37da297d7473'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'admin',
        sa.Column('ukey', sa.VARCHAR(128), primary_key=True),
        sa.Column('date_created', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('admin')

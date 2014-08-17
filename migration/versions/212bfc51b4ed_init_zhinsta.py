"""init zhinsta

Revision ID: 212bfc51b4ed
Revises: 1c694f620b6
Create Date: 2014-08-17 14:28:48.553830

"""

# revision identifiers, used by Alembic.
revision = '212bfc51b4ed'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user',
        sa.Column('ukey', sa.VARCHAR(128), primary_key=True),
        sa.Column('access_token', sa.VARCHAR(255)),
        sa.Column('username', sa.VARCHAR(255)),
        sa.Column('pic', sa.VARCHAR(255)),
        sa.Column('date_created', sa.DateTime(), nullable=False))

    op.create_table(
        'follow',
        sa.Column('ukey', sa.VARCHAR(128), primary_key=True),
        sa.Column('follow_ukey', sa.VARCHAR(128), primary_key=True),
        sa.Column('date_created', sa.DateTime(), nullable=False))

    op.create_table(
        'like',
        sa.Column('ukey', sa.VARCHAR(128), primary_key=True),
        sa.Column('media', sa.VARCHAR(128), index=True),
        sa.Column('date_created', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('user')
    op.drop_table('follow')
    op.drop_table('like')

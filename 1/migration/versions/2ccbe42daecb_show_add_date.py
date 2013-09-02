"""show add date

Revision ID: 2ccbe42daecb
Revises: 2ec3fc9a45df
Create Date: 2013-09-02 21:16:12.153337

"""

# revision identifiers, used by Alembic.
revision = '2ccbe42daecb'
down_revision = '2ec3fc9a45df'

import time

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


def upgrade():
    op.add_column('show',
                  sa.Column('date_tagged', sa.DateTime(), nullable=False,
                            server_default=func.now(), index=True))
    op.add_column('show',
                  sa.Column('hour_tagged', sa.Integer(),
                            nullable=False, index=True,
                            server_default=str(int(time.time()/7200))))


def downgrade():
    op.drop_column('show', 'date_tagged')
    op.drop_column('show', 'hour_tagged')

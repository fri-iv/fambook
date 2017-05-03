"""notes_add_column_archived

Revision ID: 1a99baefe668
Revises: c6fe6ef54105
Create Date: 2017-05-03 22:28:42.101173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a99baefe668'
down_revision = 'c6fe6ef54105'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('notes', sa.Column('archived', sa.Boolean, server_default='False'))


def downgrade():
    op.drop_column('notes', 'archived')

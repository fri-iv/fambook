"""users_add_column_sid_field

Revision ID: 37d176b5129e
Revises: 62b61563143f
Create Date: 2017-04-30 22:27:09.760688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37d176b5129e'
down_revision = '62b61563143f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('sessions', sa.Column('sid', sa.String))
    op.add_column('users', sa.Column('name', sa.String))
    op.drop_column('users', 'email')
    op.drop_column('users', 'password')


def downgrade():
    op.drop_column('sessions', 'sid')

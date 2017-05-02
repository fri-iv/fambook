"""users_add_column_fb_uid

Revision ID: c6fe6ef54105
Revises: 37d176b5129e
Create Date: 2017-05-01 02:26:42.560146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6fe6ef54105'
down_revision = '37d176b5129e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('fb_uid', sa.String))


def downgrade():
    op.drop_column('users', 'fb_uid')

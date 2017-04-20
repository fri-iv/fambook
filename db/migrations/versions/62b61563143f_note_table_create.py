"""note_table_create

Revision ID: 62b61563143f
Revises: 91b808511bf8
Create Date: 2017-04-09 19:13:28.870388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62b61563143f'
down_revision = '91b808511bf8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=True),
        sa.Column('status', sa.Boolean, server_default='False'),
        sa.Column('created_at', sa.DateTime, server_default='now()')
    )
    op.create_table(
        'notes_users_m2m',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('note_id', sa.Integer, sa.ForeignKey('notes.id', ondelete='CASCADE'), nullable=False)
    )
    op.create_table(
        'notes_changes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('note_id', sa.Integer, sa.ForeignKey('notes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('action', sa.String, nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default='now()')
    )
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('status', sa.Boolean, server_default='False'),
        sa.Column('note_id', sa.Integer, sa.ForeignKey('notes.id', ondelete='CASCADE'), nullable=False)
    )


def downgrade():
    op.drop_table('items')
    op.drop_table('notes_changes')
    op.drop_table('notes_users_m2m')
    op.drop_table('notes')

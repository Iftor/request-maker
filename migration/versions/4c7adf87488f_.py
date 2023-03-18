"""empty message

Revision ID: 4c7adf87488f
Revises: 
Create Date: 2023-03-18 18:16:15.529903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c7adf87488f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('queue_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uri', sa.String(), nullable=True),
    sa.Column('method', sa.String(length=6), nullable=False),
    sa.Column('params', sa.String(), nullable=True),
    sa.Column('headers', sa.String(), nullable=True),
    sa.Column('processed', sa.Boolean(), server_default='0', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('queue_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_code', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('queue_request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['queue_request_id'], ['queue_requests.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('queue_responses')
    op.drop_table('queue_requests')
    # ### end Alembic commands ###

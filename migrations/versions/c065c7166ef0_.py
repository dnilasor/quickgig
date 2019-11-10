"""empty message

Revision ID: c065c7166ef0
Revises: 1f5feeca29ac
Create Date: 2019-11-09 20:02:05.590722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c065c7166ef0'
down_revision = '1f5feeca29ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_neighborhood_name'), 'neighborhood', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_neighborhood_name'), table_name='neighborhood')
    # ### end Alembic commands ###
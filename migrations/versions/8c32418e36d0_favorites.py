"""favorites

Revision ID: 8c32418e36d0
Revises: 3c1982b4e176
Create Date: 2019-10-22 13:03:50.214973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c32418e36d0'
down_revision = '3c1982b4e176'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('favoriter_id', sa.Integer(), nullable=True),
    sa.Column('favorited_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorited_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['favoriter_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    # ### end Alembic commands ###

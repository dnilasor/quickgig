"""add language to gigs

Revision ID: 0c4425d6ac65
Revises: 378e7158fcf6
Create Date: 2019-10-23 10:24:07.268368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c4425d6ac65'
down_revision = '378e7158fcf6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gig', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gig', 'language')
    # ### end Alembic commands ###

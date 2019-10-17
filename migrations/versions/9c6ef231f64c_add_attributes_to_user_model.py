"""add attributes to user model

Revision ID: 9c6ef231f64c
Revises: fb2c7254a5fe
Create Date: 2019-10-17 12:06:40.115189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c6ef231f64c'
down_revision = 'fb2c7254a5fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('first_name', sa.String(length=40), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=40), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
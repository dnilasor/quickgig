"""empty message

Revision ID: b3c5bb1954ee
Revises: 
Create Date: 2019-11-29 20:32:14.837883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c5bb1954ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gigtype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gigtype_name'), 'gigtype', ['name'], unique=True)
    op.create_table('neighborhood',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_neighborhood_name'), 'neighborhood', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('first_name', sa.String(length=40), nullable=True),
    sa.Column('last_name', sa.String(length=40), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('favoriters',
    sa.Column('favoriter_id', sa.Integer(), nullable=True),
    sa.Column('favorited_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorited_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['favoriter_id'], ['user.id'], )
    )
    op.create_table('gig',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('detail', sa.String(length=4000), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(length=5), nullable=True),
    sa.Column('neighborhood_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['neighborhood_id'], ['neighborhood.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['gigtype.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gig_timestamp'), 'gig', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gig_timestamp'), table_name='gig')
    op.drop_table('gig')
    op.drop_table('favoriters')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_neighborhood_name'), table_name='neighborhood')
    op.drop_table('neighborhood')
    op.drop_index(op.f('ix_gigtype_name'), table_name='gigtype')
    op.drop_table('gigtype')
    # ### end Alembic commands ###

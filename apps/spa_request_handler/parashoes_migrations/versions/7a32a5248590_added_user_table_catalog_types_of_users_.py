"""Added user table, catalog types of users and mant-to-many table for them

Revision ID: 7a32a5248590
Revises: 9efba819b4d4
Create Date: 2016-08-27 23:16:50.525322

"""

# revision identifiers, used by Alembic.
revision = '7a32a5248590'
down_revision = '9efba819b4d4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute("create sequence user_id_seq start with 1 increment by 1")
    op.execute("create sequence catalog_user_type_id_seq start with 1 increment by 1")
    op.execute("create sequence users_types_id_seq start with 1 increment by 1")
    op.create_table('catalog_user_type',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('catalog_user_type_id_seq'::regclass)"), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_catalog_user_type_id'), 'catalog_user_type', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('user_id_seq'::regclass)"), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('firstname', sa.Text(), nullable=True),
    sa.Column('lastname', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_login_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_types',
    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('users_types_id_seq'::regclass)"), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['catalog_user_type.id'], onupdate='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_users_types_id', 'users_types', ['user_id', 'type_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.schema.DropSequence(sa.Sequence("user_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("catalog_user_type_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("users_types_id_seq")))
    op.drop_index('idx_users_types_id', table_name='users_types')
    op.drop_table('users_types')
    op.drop_table('user')
    op.drop_index(op.f('ix_catalog_user_type_id'), table_name='catalog_user_type')
    op.drop_table('catalog_user_type')
    ### end Alembic commands ###
"""empty message

Revision ID: ae8bf1753348
Revises: f229bb7e2d52
Create Date: 2016-05-05 09:38:08.541000

"""

# revision identifiers, used by Alembic.
revision = 'ae8bf1753348'
down_revision = 'f229bb7e2d52'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('todos', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('member_since', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todo_list_description'), 'todo_list', ['description'], unique=False)
    op.create_index(op.f('ix_todo_list_timestamp'), 'todo_list', ['timestamp'], unique=False)
    op.create_index(op.f('ix_todo_list_todos'), 'todo_list', ['todos'], unique=False)
    op.drop_table('roles')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'name')
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'role_id')
    op.drop_column('users', 'about_me')
    op.drop_column('users', 'location')
    op.drop_column('users', 'last_seen')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', sa.DATETIME(), nullable=True))
    op.add_column('users', sa.Column('location', sa.VARCHAR(length=64), nullable=True))
    op.add_column('users', sa.Column('about_me', sa.TEXT(), nullable=True))
    op.add_column('users', sa.Column('role_id', sa.INTEGER(), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.DATETIME(), nullable=True))
    op.add_column('users', sa.Column('name', sa.VARCHAR(length=64), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('default', sa.BOOLEAN(), nullable=True),
    sa.Column('permissions', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_index(op.f('ix_todo_list_todos'), table_name='todo_list')
    op.drop_index(op.f('ix_todo_list_timestamp'), table_name='todo_list')
    op.drop_index(op.f('ix_todo_list_description'), table_name='todo_list')
    op.drop_table('todo_list')
    ### end Alembic commands ###

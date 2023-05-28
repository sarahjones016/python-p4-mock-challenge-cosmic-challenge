"""create tables

Revision ID: e64db6490f60
Revises: b336f187f918
Create Date: 2023-05-26 11:10:45.403146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e64db6490f60'
down_revision = 'b336f187f918'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('missions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('scientist_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_missions_scientist_id_scientists'), 'scientists', ['scientist_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_missions_planet_id_planets'), 'planets', ['planet_id'], ['id'])

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scientists', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('missions', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_missions_planet_id_planets'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_missions_scientist_id_scientists'), type_='foreignkey')
        batch_op.drop_column('planet_id')
        batch_op.drop_column('scientist_id')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('name')

    # ### end Alembic commands ###

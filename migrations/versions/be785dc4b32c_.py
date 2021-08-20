"""empty message

Revision ID: be785dc4b32c
Revises: acf6d4073216
Create Date: 2021-08-20 12:59:36.195886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be785dc4b32c'
down_revision = 'acf6d4073216'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_status', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hatching_pet', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('pet_personality', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_status', schema=None) as batch_op:
        batch_op.drop_column('pet_personality')
        batch_op.drop_column('hatching_pet')

    # ### end Alembic commands ###

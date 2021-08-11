"""empty message

Revision ID: 6af26d4f8df3
Revises: bc4603fcfebc
Create Date: 2021-08-11 23:25:20.909463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6af26d4f8df3'
down_revision = 'bc4603fcfebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_status', schema=None) as batch_op:
        batch_op.drop_column('petCount')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_status', schema=None) as batch_op:
        batch_op.add_column(sa.Column('petCount', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###

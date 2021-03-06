"""empty message

Revision ID: a595f505f7fa
Revises: 87588dbbdd09
Create Date: 2021-08-16 23:15:34.824348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a595f505f7fa'
down_revision = '87588dbbdd09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sneeze_game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('player2_hp', sa.Integer(), nullable=True))
        batch_op.drop_column('person2_hp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sneeze_game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('person2_hp', sa.INTEGER(), nullable=True))
        batch_op.drop_column('player2_hp')

    # ### end Alembic commands ###

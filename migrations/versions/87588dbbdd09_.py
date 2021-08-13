"""empty message

Revision ID: 87588dbbdd09
Revises: 75f1196a4639
Create Date: 2021-08-13 13:18:18.397745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87588dbbdd09'
down_revision = '75f1196a4639'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=128), nullable=False))

    # ### end Alembic commands ###
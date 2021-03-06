"""empty message

Revision ID: 0d08a8c9bd5d
Revises: 0bbf05a89ab4
Create Date: 2021-08-21 17:31:56.332194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d08a8c9bd5d'
down_revision = '0bbf05a89ab4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('growing_pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('experience', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('academic', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('growing_pet', schema=None) as batch_op:
        batch_op.drop_column('academic')
        batch_op.drop_column('experience')

    # ### end Alembic commands ###

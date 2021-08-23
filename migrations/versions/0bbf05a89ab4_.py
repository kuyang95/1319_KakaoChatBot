"""empty message

Revision ID: 0bbf05a89ab4
Revises: 0f07780d133b
Create Date: 2021-08-21 17:15:33.963595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bbf05a89ab4'
down_revision = '0f07780d133b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('growing_pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('strength', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('intellect', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('shild', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('health', sa.Integer(), nullable=True))
        batch_op.drop_column('stat_shild')
        batch_op.drop_column('stat_health')
        batch_op.drop_column('stat_intellect')
        batch_op.drop_column('stat_strength')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('growing_pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stat_strength', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('stat_intellect', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('stat_health', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('stat_shild', sa.INTEGER(), nullable=False))
        batch_op.drop_column('health')
        batch_op.drop_column('shild')
        batch_op.drop_column('intellect')
        batch_op.drop_column('strength')

    # ### end Alembic commands ###
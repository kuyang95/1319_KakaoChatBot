"""empty message

Revision ID: 87b3fb2e049b
Revises: e595180e3e2b
Create Date: 2021-08-21 16:16:14.830798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87b3fb2e049b'
down_revision = 'e595180e3e2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_pet_book')
    with op.batch_alter_table('pet_book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('strength', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('intellect', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('shild', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('health', sa.Integer(), nullable=False))
        batch_op.drop_column('stat_health')
        batch_op.drop_column('stat_shild')
        batch_op.drop_column('stat_intellect')
        batch_op.drop_column('stat_strength')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet_book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stat_strength', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('stat_intellect', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('stat_shild', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('stat_health', sa.INTEGER(), nullable=False))
        batch_op.drop_column('health')
        batch_op.drop_column('shild')
        batch_op.drop_column('intellect')
        batch_op.drop_column('strength')

    op.create_table('_alembic_tmp_pet_book',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('img', sa.VARCHAR(length=200), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('element', sa.VARCHAR(length=20), nullable=False),
    sa.Column('rare', sa.VARCHAR(length=20), nullable=False),
    sa.Column('food', sa.VARCHAR(length=50), nullable=True),
    sa.Column('descript', sa.VARCHAR(length=200), nullable=True),
    sa.Column('p_type', sa.VARCHAR(length=20), nullable=True),
    sa.Column('strength', sa.INTEGER(), nullable=False),
    sa.Column('intellect', sa.INTEGER(), nullable=False),
    sa.Column('shild', sa.INTEGER(), nullable=False),
    sa.Column('health', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_pet_book')
    )
    # ### end Alembic commands ###

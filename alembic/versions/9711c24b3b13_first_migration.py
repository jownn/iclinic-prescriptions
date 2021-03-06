"""First migration

Revision ID: 9711c24b3b13
Revises: 
Create Date: 2022-01-25 23:02:39.880872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9711c24b3b13'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prescription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clinic_id', sa.Integer(), nullable=True),
    sa.Column('physician_id', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('metric_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prescription_id'), 'prescription', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_prescription_id'), table_name='prescription')
    op.drop_table('prescription')
    # ### end Alembic commands ###

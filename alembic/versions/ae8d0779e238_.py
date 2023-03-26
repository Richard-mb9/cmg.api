"""empty message

Revision ID: ae8d0779e238
Revises: ee09966d93bc
Create Date: 2023-02-02 12:00:41.180858

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ae8d0779e238'
down_revision = 'ee09966d93bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoices_items')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoices_items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('invoice_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], name='invoices_items_invoice_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='invoices_items_pkey')
    )
    # ### end Alembic commands ###

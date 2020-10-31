"""users and historical data tables

Revision ID: 98eeb9219296
Revises: 
Create Date: 2020-10-27 02:00:03.581809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98eeb9219296'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('country')
    )
    op.create_table('historical_prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('price_close', sa.Float(), nullable=False),
    sa.Column('price_open', sa.Float(), nullable=True),
    sa.Column('price_high', sa.Float(), nullable=True),
    sa.Column('price_low', sa.Float(), nullable=True),
    sa.Column('volume', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('industries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('industry_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('industry_name')
    )
    op.create_table('peers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=False),
    sa.Column('peer_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ticker')
    )
    op.create_table('sectors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sector_name', sa.String(), nullable=False),
    sa.Column('industry_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sector_name')
    )
    op.create_table('stocks_attributes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stock_name', sa.String(), nullable=False),
    sa.Column('ticker', sa.String(), nullable=False),
    sa.Column('stock_exchange_name', sa.String(), nullable=False),
    sa.Column('sector_id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('stock_name'),
    sa.UniqueConstraint('ticker')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.drop_table('user')
    op.drop_table('stocks_attributes')
    op.drop_table('sectors')
    op.drop_table('peers')
    op.drop_table('industries')
    op.drop_table('historical_prices')
    op.drop_table('countries')
    # ### end Alembic commands ###

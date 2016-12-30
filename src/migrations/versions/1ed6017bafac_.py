"""empty message

Revision ID: 1ed6017bafac
Revises: f8ad33c1e9c3
Create Date: 2016-12-23 05:10:18.645830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ed6017bafac'
down_revision = 'f8ad33c1e9c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###

"""del column has_sale

Revision ID: c17af7adc6f2
Revises: 40eb9785f3d6
Create Date: 2024-07-26 16:48:50.748669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c17af7adc6f2'
down_revision: Union[str, None] = '40eb9785f3d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'has_sale')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('has_sale', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
